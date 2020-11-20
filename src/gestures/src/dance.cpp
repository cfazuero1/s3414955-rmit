#include "ros/ros.h"
#include "std_msgs/String.h"
#include "sensor_msgs/Joy.h"
#include "geometry_msgs/Twist.h"
#include "trajectory_msgs/JointTrajectory.h"
#include "trajectory_msgs/JointTrajectoryPoint.h"

#include <cstdlib>
#include <unistd.h>
#include <ctime>
#include <string.h>

float randfloat(float M, float N){
    return M + (rand() / ( RAND_MAX / (N-M) ) ) ;  
}

int main(int argc, char** argv){
	int i, j;

	srand(time(NULL));

	ros::init(argc, argv, "dance");
	ros::NodeHandle n;

	ros::Publisher joint_messages_head = n.advertise<trajectory_msgs::JointTrajectory>("head_controller/command", 10);
	ros::Publisher joint_messages_torso = n.advertise<trajectory_msgs::JointTrajectory>("torso_controller/command", 10);
	ros::Publisher joint_messages_larm = n.advertise<trajectory_msgs::JointTrajectory>("left_arm_controller/command", 10);
	ros::Publisher joint_messages_rarm = n.advertise<trajectory_msgs::JointTrajectory>("right_arm_controller/command", 10);
	ros::Publisher joint_messages_lhand = n.advertise<trajectory_msgs::JointTrajectory>("left_hand_controller/command", 10);
	ros::Publisher joint_messages_rhand = n.advertise<trajectory_msgs::JointTrajectory>("right_hand_controller/command", 10);

	std::vector<trajectory_msgs::JointTrajectory> trajs; //traj_head, traj_torso, traj_larm, traj_rarm, traj_lhand, traj_rhand;
	trajectory_msgs::JointTrajectory trajtmp;
	std::string sections[] = {"head", "torso", "left_arm", "right_arm", "left_hand", "right_hand"};
	float tempo;
	if(argc > 1) tempo = strtof(argv[0], NULL);
	else tempo = 2.0;//defined as seconds per pose; loop rate = 1/tempo?

	std::vector<std::string> jnames;
	int numsects = sizeof(sections)/sizeof(sections[0]);
	for(i=0; i<numsects; i++){
		ros::param::get("/"+sections[i]+"_controller/joints", jnames);
		trajtmp.joint_names.clear();
		for(j=0; j<jnames.size(); j++){
			trajtmp.joint_names.push_back(jnames[j]);
		}
		trajtmp.points.resize(1);
		trajtmp.points[0].positions.resize(jnames.size());
		trajtmp.points[0].time_from_start = ros::Duration(tempo);

		trajs.push_back(trajtmp);
	}

	ros::Rate looprate(1/tempo);
	ros::Duration pausetime(tempo);

	while(ros::ok()){
		//for each section
		for(i=0; i<numsects; i++){
			//for each joint in the section
			for(j=0; j<trajs[i].joint_names.size(); j++){
				//set positions to random
				trajs[i].points[0].positions[j] = randfloat(-2.0, 2.0);
			}
		}
		//publish each section
		trajs[0].header.stamp = ros::Time::now();
		joint_messages_head.publish(trajs[0]);
		trajs[1].header.stamp = ros::Time::now();
		joint_messages_torso.publish(trajs[1]);
		trajs[2].header.stamp = ros::Time::now();
		joint_messages_larm.publish(trajs[2]);
		trajs[3].header.stamp = ros::Time::now();
		joint_messages_rarm.publish(trajs[3]);
		trajs[4].header.stamp = ros::Time::now();
		joint_messages_lhand.publish(trajs[4]);
		trajs[5].header.stamp = ros::Time::now();
		joint_messages_rhand.publish(trajs[5]);

		looprate.sleep();
	}
/*	armtester.joint_names.push_back("arm_right_1_joint");
	armtester.joint_names.push_back("arm_right_2_joint");
	armtester.joint_names.push_back("arm_right_3_joint");
	armtester.joint_names.push_back("arm_right_4_joint");
	armtester.joint_names.push_back("arm_right_5_joint");
	armtester.joint_names.push_back("arm_right_6_joint");
	armtester.joint_names.push_back("arm_right_7_joint");

	armtester.points.resize(1);

	int posno = 0;

	armtester.points[0].positions.resize(7);
	for(i=0; i<7; i++){
		armtester.points[posno].positions[i] = 0.0;
	}
*/
/*	armtester.points[posno].positions.resize(7);
	armtester.points[posno].positions[0] = 1.3721;
	armtester.points[posno].positions[1] = 1.3812;
	armtester.points[posno].positions[2] = 0.0594;
	armtester.points[posno].positions[3] = 2.0973;
	armtester.points[posno].positions[4] = 1.5739;
	armtester.points[posno].positions[5] = -0.7774;
	armtester.points[posno].positions[6] = 0.0;
	armtester.points[posno].time_from_start = ros::Duration(5.0);

	while(ros::ok()){
//	for(i=0;i<2;i++){
		armtester.header.stamp = ros::Time::now();
		joint_messages.publish(armtester);
		ROS_INFO("Published okay");
		sleep(5);
	}
*/
	return 0;
}

