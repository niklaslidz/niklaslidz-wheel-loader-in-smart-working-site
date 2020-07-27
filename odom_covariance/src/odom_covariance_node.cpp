#include <ros/ros.h>
#include <nav_msgs/Odometry.h>

ros::Publisher odom_pub;

double posX, posY, posZ, rotX, rotY, rotZ;

void odomCallback(const nav_msgs::Odometry::ConstPtr& msg)
{
	nav_msgs::Odometry odom;
	odom.child_frame_id = msg->child_frame_id;
    odom.header = msg->header;
    odom.header.frame_id = "base_link";          // the tracked robot frame
    odom.pose = msg->pose;
    odom.twist = msg->twist;

    odom.pose.covariance.elems[0]  = posX;
    odom.pose.covariance.elems[7]  = posY;
    odom.pose.covariance.elems[14] = posZ;
    odom.pose.covariance.elems[21] = rotX;
    odom.pose.covariance.elems[28] = rotY;
    odom.pose.covariance.elems[35] = rotZ;
    odom.twist.covariance = odom.pose.covariance;

    odom_pub.publish(odom);


}

int main(int argc, char **argv)
{
	ros::init(argc, argv, "odom_covariance_node");
	ros::NodeHandle n;

	std::string global_name, relative_name, default_param;

	ros::param::param("~posX", posX, 0.1);
	ros::param::param("~posY", posY, 0.1);
	ros::param::param("~posZ", posZ, 99999.0);
	ros::param::param("~rotX", rotX, 99999.0);
	ros::param::param("~rotY", rotY, 99999.0);
	ros::param::param("~rotZ", rotZ, 0.1);

	ros::Subscriber sub = n.subscribe("inputOdom", 1, odomCallback);
	odom_pub = n.advertise<nav_msgs::Odometry>("outputOdom", 1);
	ros::spin();
	return 0;
}
