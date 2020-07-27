#!/usr/bin/env python

import rospy
import std_msgs.msg
from sensor_msgs.msg import NavSatFix


def subs():
    rospy.init_node('subs', anonymous=True)
    rospy.Subscriber("GPS", NavSatFix, gpsCallback)
    rospy.spin()

def gpsCallback(data):
    gps = NavSatFix()
    gps.header.seq = data.header.seq
    gps.header.stamp = data.header.stamp
    if (gps.header.stamp.secs % 10 != 2):
        gps.header.frame_id = "gps2_Link"
        gps.status=data.status
        gps.latitude = data.latitude
        gps.longitude = data.longitude
        gps.altitude = data.altitude
        gps.position_covariance = data.position_covariance
        gps.position_covariance_type = data.position_covariance_type
        pub = rospy.Publisher('/gps_filtered', NavSatFix, queue_size=10)
        rate = rospy.Rate(5) # Hz
        pub.publish(gps)
        rate.sleep()  
    else:
        gps.header.frame_id = "false_Link"
        gps.status=data.status
        gps.latitude = 0
        gps.longitude = 0
        gps.altitude = 0
        gps.position_covariance = data.position_covariance
        gps.position_covariance_type = data.position_covariance_type
        
    

if __name__ == '__main__':
    try:
        subs()
    except rospy.ROSInterruptException:
        pass
  
