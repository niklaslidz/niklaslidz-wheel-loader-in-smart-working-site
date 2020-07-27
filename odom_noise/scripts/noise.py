#! /usr/bin/env python

import rospy

from math import *

import numpy as np

from nav_msgs.msg import Odometry

import tf
from geometry_msgs.msg import Point, Pose, Quaternion, Twist, Vector3
 

last_odom = None

pose = [0.0,0.0,0.0]

a1 = 0.0

a2 = 0.0

a3 = 0.0

a4 = 0.0

base_frame = ""

 

# a callback for Gazebo odometry data

def callback(data):

    global last_odom

    global base_frame

    global pose

    global a1

    global a2

    global a3

    global a4
    current_time = rospy.Time.now()

 

    if(last_odom == None):

        last_odom = data

        pose[0] = data.pose.pose.position.x

        pose[1] = data.pose.pose.position.y

        q = [ data.pose.pose.orientation.x,

                data.pose.pose.orientation.y,

                data.pose.pose.orientation.z,

                data.pose.pose.orientation.w ]

        (r, p, y) = tf.transformations.euler_from_quaternion(q)

        pose[2] = y

    else:

        # calculate new odometry pose using the motion model

        dx = data.pose.pose.position.x - last_odom.pose.pose.position.x

        dy = data.pose.pose.position.y - last_odom.pose.pose.position.y

        trans = sqrt(dx*dx + dy*dy)

        q = [ last_odom.pose.pose.orientation.x,

                last_odom.pose.pose.orientation.y,

                last_odom.pose.pose.orientation.z,

                last_odom.pose.pose.orientation.w ]

        (r,p, theta1) = tf.transformations.euler_from_quaternion(q)

        q = [ data.pose.pose.orientation.x,

                data.pose.pose.orientation.y,

                data.pose.pose.orientation.z,

                data.pose.pose.orientation.w ]

        (r,p, theta2) = tf.transformations.euler_from_quaternion(q)

        rot1 = atan2(dy, dx) - theta1

        rot2 = theta2-theta1-rot1

 

        sd_rot1 = a1*abs(rot1) + a2*trans

        sd_rot2 = a1*abs(rot2) + a2*trans

        sd_trans = a3*trans + a4*(abs(rot1) + abs(rot2))

 

        trans +=  np.random.normal(0,sd_trans*sd_trans)

        rot1 += np.random.normal(0, sd_rot1*sd_rot1)

        rot2 += np.random.normal(0, sd_rot2*sd_rot2)

 

        pose[0] += trans*cos(theta1+rot1)

        pose[1] += trans*sin(theta1+rot1)

        pose[2] = theta1 + rot1 + rot2
        

        odom = Odometry()
        odom.header.stamp = current_time
        odom.header.frame_id = "odom"
        odom_quat = tf.transformations.quaternion_from_euler(0, 0, pose[2])
        odom.pose.pose = Pose(Point(pose[0], pose[1], 0), Quaternion(*odom_quat))
        odom.child_frame_id = "base_link"
        odom.twist.twist = Twist(Vector3(0.0, 0.0, 0), Vector3(0, 0, 0))
        odom_pub.publish(odom)
        last_time = current_time

        last_odom = data

 

    # publish the tf

    br = tf.TransformBroadcaster()

    # br.sendTransform((pose[0], pose[1], 0),

    #                  tf.transformations.quaternion_from_euler(0, 0, pose[2]),

    #                  data.header.stamp,

    #                  base_frame,

    #                  "odom")


if __name__ == '__main__':

    rospy.init_node('noisy_odometry', anonymous=True)

    rospy.logwarn("alpha1 is set to default")

    a1 = 15.0*pi/180.0

    # alpha 2 is degree/m

    a2 = 15.0*pi/180.0

    rospy.logwarn("alpha2 is set to default")

    # alpha 3 is m/meter

    a3 = 0.2

    rospy.logwarn("alpha3 is set to default")

    # alpha 4 is m/degree

    a4 = 0.01

    rospy.logwarn("alpha4 is set to default")

    # get odom topic


    odom_topic = "/odom"

    # get base frame

    base_frame = "/base_link"

 

    rospy.Subscriber(odom_topic, Odometry, callback)
    odom_pub = rospy.Publisher("odom_noise", Odometry, queue_size=50)
 

    rospy.spin()