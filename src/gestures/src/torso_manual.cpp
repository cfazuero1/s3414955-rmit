#include "ros/ros.h"
#include "std_msgs/String.h"
#include "sensor_msgs/Joy.h"
#include "geometry_msgs/Twist.h"
#include "trajectory_msgs/JointTrajectory.h"
#include "trajectory_msgs/JointTrajectoryPoint.h"
#include "gesture_sender.h"

sensor_msgs::Joy joyin;

void joyFeed(const sensor_msgs::Joy& feed){
	float stickh = feed.axes[3];
	float stickv = feed.axes[4];
	float ltrig = feed.axes[2];
	float rtrig = feed.axes[5];
ROS_INFO("Joystick input received:\n{%f, %f}\t%f\t%f", stickh, stickv, ltrig, rtrig);
	joyin = feed;
}

class Jointholder{
	public:
		trajectory_msgs::JointTrajectory joints_head;
		trajectory_msgs::JointTrajectory joints_leftarm;
		trajectory_msgs::JointTrajectory joints_lefthand;
		trajectory_msgs::JointTrajectory joints_rightarm;
		trajectory_msgs::JointTrajectory joints_righthand;
		trajectory_msgs::JointTrajectory joints_torso;

	//there might be a way to automatically fetch the number of joints in each; system parameter <body part>_controller/joints is a list of the joints for each controller...
	
	//initializing: for each joint
		//push_back names
		//resize points to 1
		// resize positions (and velocities/acceleration/effort) to no. of joints
		//set points[0].time_from_start
	Jointholder(int pubrate){
		std::vector<std::string> jointnames;
		int numjoints, i;
		float pubdur = 1.0/pubrate;

		ros::param::get("/head_controller/joints", jointnames);
		numjoints = jointnames.size();
		for(i=0; i<numjoints;i++){
			joints_head.joint_names.push_back(jointnames[i]);
		}
		joints_head.points.resize(1);
		joints_head.points[0].positions.resize(numjoints);
		joints_head.points[0].velocities.resize(numjoints);
		joints_head.points[0].accelerations.resize(numjoints);
		joints_head.points[0].effort.resize(numjoints);
		joints_head.points[0].time_from_start = ros::Duration(pubdur);

		ros::param::get("/left_arm_controller/joints", jointnames);
		numjoints = jointnames.size();
		for(i=0; i<numjoints;i++){
			joints_leftarm.joint_names.push_back(jointnames[i]);
		}
		joints_leftarm.points.resize(1);
		joints_leftarm.points[0].positions.resize(numjoints);
		joints_leftarm.points[0].velocities.resize(numjoints);
		joints_leftarm.points[0].accelerations.resize(numjoints);
		joints_leftarm.points[0].effort.resize(numjoints);
		joints_leftarm.points[0].time_from_start = ros::Duration(pubdur);
		//this automated approach still needs to be tested
	}
		//ugh, arms have 7 joints apiece
};

int main(int argc, char** argv){
	int i = 0;

	ros::init(argc, argv, "torso_control");
	ros::NodeHandle n;

	//Publishers needed for each body section to be controlled. Ideally these'll be wrapped up in a class in the future
	//Sections: head, torso, left arm, right arm, left hand, right hand
	ros::Publisher comm_torso = n.advertise<trajectory_msgs::JointTrajectory>("torso_controller/command", 1);
	ros::Publisher comm_larm = n.advertise<trajectory_msgs::JointTrajectory>("left_arm_controller/command", 1);
	ros::Publisher comm_rarm = n.advertise<trajectory_msgs::JointTrajectory>("right_arm_controller/command", 1);

	//Capture gamepad input, kindly sorted by ROS
	ros::Subscriber inp = n.subscribe("joy", 500, joyFeed);
	sleep(3); //make sure the topic is being read
	trajectory_msgs::JointTrajectory traj_torso;
	trajectory_msgs::JointTrajectory traj_larm;
	trajectory_msgs::JointTrajectory traj_rarm;

	traj_torso.joint_names.push_back("torso_1_joint");
	traj_torso.joint_names.push_back("torso_2_joint");
	traj_torso.points.resize(1);
	traj_torso.points[0].positions.resize(2);
	traj_torso.points[0].time_from_start = ros::Duration(0.2);

	traj_larm.joint_names.push_back("arm_left_1_joint");
	traj_larm.joint_names.push_back("arm_left_2_joint");
	traj_larm.joint_names.push_back("arm_left_3_joint");
	traj_larm.joint_names.push_back("arm_left_4_joint");
	traj_larm.joint_names.push_back("arm_left_5_joint");
	traj_larm.joint_names.push_back("arm_left_6_joint");
	traj_larm.joint_names.push_back("arm_left_7_joint");
	traj_larm.points.resize(1);
	traj_larm.points[0].positions.resize(7);
	traj_larm.points[0].time_from_start = ros::Duration(0.2);

	traj_rarm.joint_names.push_back("arm_right_1_joint");
	traj_rarm.joint_names.push_back("arm_right_2_joint");
	traj_rarm.joint_names.push_back("arm_right_3_joint");
	traj_rarm.joint_names.push_back("arm_right_4_joint");
	traj_rarm.joint_names.push_back("arm_right_5_joint");
	traj_rarm.joint_names.push_back("arm_right_6_joint");
	traj_rarm.joint_names.push_back("arm_right_7_joint");
	traj_rarm.points.resize(1);
	traj_rarm.points[0].positions.resize(7);
	traj_rarm.points[0].time_from_start = ros::Duration(0.2);

	ros::Rate loop_rate(5);

	GestureSender g;
	std::vector<std::string> gests;
	//gestures are added in button order:
	//X, O, square, triangle, L1, R1, Select, Start, Home, L3, R3
	gests.push_back("home");
	gests.push_back("power_pose");
	gests.push_back("chop");
	gests.push_back("strong_arms");

	while(ros::ok()){
		ros::spinOnce(); //get latest joypad input
		for(i=0; i<gests.size(); i++){
			if(joyin.buttons[i]){
				g.send_motion(gests[i]);
			}
		}

		traj_torso.points[0].positions[0] = (joyin.axes[3]) * 3.0; //right stick for torso
		traj_torso.points[0].positions[1] = (joyin.axes[4]) * 3.0;

		traj_larm.points[0].positions[0] = (joyin.axes[2]); //shoulder
		traj_larm.points[0].positions[1] = 0.1; //shoulder needs to stick out a bit, otherwise it collides with the body
		traj_larm.points[0].positions[3] = (joyin.axes[2]); //elbow

		traj_rarm.points[0].positions[0] = (joyin.axes[5]); //shoulder
		traj_rarm.points[0].positions[1] = 0.1; //shoulder needs to stick out a bit, otherwise it collides with the body
		traj_rarm.points[0].positions[3] = (joyin.axes[5]); //elbow

		traj_torso.header.stamp = ros::Time::now();
		comm_torso.publish(traj_torso);
		traj_larm.header.stamp = ros::Time::now();
		comm_larm.publish(traj_larm);
		traj_rarm.header.stamp = ros::Time::now();
		comm_rarm.publish(traj_rarm);

		loop_rate.sleep();
	}

	return 0;
}
