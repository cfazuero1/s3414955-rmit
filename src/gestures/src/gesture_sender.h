#ifndef __GESTURE_SENDER_INCL__
#define __GESTURE_SENDER_INCL__

#include <ros/ros.h> //is it reasonable to assume this will be included already? I mean it's guarded so this won't matter, but still...
#include <actionlib/client/simple_action_client.h>
#include <actionlib/client/terminal_state.h>
#include <play_motion_msgs/PlayMotionAction.h>

class GestureSender{
	private:
		actionlib::SimpleActionClient<play_motion_msgs::PlayMotionAction> cli_;
		play_motion_msgs::PlayMotionGoal goal_;
		play_motion_msgs::PlayMotionResult result_;

	public:

	GestureSender():
		cli_("play_motion", true){ //note for the future: this seems to be the only valid way to initialize the client in a class
		//Any other method tries to take the declaration above as a constructor and fails
		ROS_INFO("Gesture sender created.");
		this->cli_.waitForServer();
		ROS_INFO("Server response received.");
	}

	~GestureSender(void){}

//Do some overloads: send_motion calls send_timeout_motion with time 0.0 which calls send_motion_free then waits for result
	void send_motion_free(std::string name){ //Just fire off the command, don't bother waiting for a result
		goal_.motion_name = name;
		goal_.skip_planning = true;
ROS_INFO("Actually executing motion: %s", name.c_str());
		this->cli_.sendGoal(goal_);
ROS_INFO("Goal sent.");
	}

	play_motion_msgs::PlayMotionResultConstPtr send_motion_timeout(std::string name, float waittime){
		ROS_INFO("motion received: %s, timeout %f", name.c_str(), waittime);
		send_motion_free(name);
		this->cli_.waitForResult(ros::Duration(waittime));
ROS_INFO("Wait complete, sending result.");
		play_motion_msgs::PlayMotionResultConstPtr res = cli_.getResult();
		return res; 
	}

	play_motion_msgs::PlayMotionResultConstPtr send_motion(std::string name){
		ROS_INFO("no timeout motion received: %s", name.c_str());
		return send_motion_timeout(name, 0.0);
	}


	void quitIt(){
		if(this->cli_.getState() == actionlib::SimpleClientGoalState::ACTIVE){
			ROS_INFO("Cancelling current goal");
			this->cli_.cancelAllGoals();
			while(this->cli_.getState() != actionlib::SimpleClientGoalState::PREEMPTED){}
		}
		//trying to check the state doesn't actually seem to help. As far as I can tell, play_motion is just fucked
	}

	bool running(){
		return (this->cli_.getState() == actionlib::SimpleClientGoalState::ACTIVE);
	}
};

#endif
