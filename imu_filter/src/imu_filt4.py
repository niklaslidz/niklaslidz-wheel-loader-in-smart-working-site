#!/usr/bin/env python

import rospy
import std_msgs.msg
from sensor_msgs.msg import Imu


def subs():
    rospy.init_node('subs', anonymous=True)
    rospy.Subscriber("imu", Imu, imuCallback)
    rospy.spin()

def imuCallback(data):
    imu = Imu()
    imu.header.seq = data.header.seq
    imu.header.stamp = rospy.Time.now()
    imu.header.frame_id = "imu4_Link"
    imu.orientation.x = data.orientation.x
    imu.orientation.y = data.orientation.y
    imu.orientation.z = data.orientation.z
    imu.orientation.w = data.orientation.w
    imu.orientation_covariance = data.orientation_covariance
    imu.angular_velocity.x = data.angular_velocity.x
    imu.angular_velocity.y = data.angular_velocity.y
    imu.angular_velocity.z = data.angular_velocity.z
    imu.angular_velocity_covariance = data.angular_velocity_covariance
    imu.linear_acceleration.x = 0
    imu.linear_acceleration.y = 0
    imu.linear_acceleration.z = 9.81
    imu.linear_acceleration_covariance = data.linear_acceleration_covariance
    pub = rospy.Publisher('/imu_filtered', Imu, queue_size=1)
    rate = rospy.Rate(100) # Hz
    pub.publish(imu)
    rate.sleep()

if __name__ == '__main__':
    try:
        subs()
    except rospy.ROSInterruptException:
        pass
  
