#!/usr/bin/env python
import rospy
import tf
from math import *
import numpy as np
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Point, Pose, Quaternion, Twist, Vector3


# Declare last_odom and values you want to multiply with original values
last_odom = None
pose = [0.0,0.0,0.0]

#adjustment parameters showing how important noise in each transformation could affect the motion, they represent the change in: degree/degree, degree/meter, meter/meter and meter/degree respectively.
a1 = 0.1
a2 = 0.2
a3 = 0.0
a4 = 0.0

pose[0] =0.0
pose[1] =0.0
pose[2] =0.0
# base_link frame to be published
base_frame = "base_link"


 # odom topic callback function
def odomcallback(data):
	global last_odom
	# rospy.loginfo("data %s",data.pose.pose)
	if(last_odom == None):
		last_odom = data
		pose[0] = data.pose.pose.position.x
		pose[1] = data.pose.pose.position.y
		q = [ data.pose.pose.orientation.x,
				data.pose.pose.orientation.y,
				data.pose.pose.orientation.z,
				data.pose.pose.orientation.w ]

				# Quaternion to Euler conversion
		(r, p, y) = tf.transformations.euler_from_quaternion(q)
		pose[2] = y
	else:
		dx = data.pose.pose.position.x - last_odom.pose.pose.position.x
		dy = data.pose.pose.position.y - last_odom.pose.pose.position.y

		trans = sqrt(dx*dx + dy*dy)#a relative translation 
		q = [ last_odom.pose.pose.orientation.x,
				last_odom.pose.pose.orientation.y,
				last_odom.pose.pose.orientation.z,
				last_odom.pose.pose.orientation.w ]
		(r,p, theta1) = tf.transformations.euler_from_quaternion(q)

		q = [ data.pose.pose.orientation.x,
				data.pose.pose.orientation.y,
				data.pose.pose.orientation.z,
				data.pose.pose.orientation.w ]

				# Quaternion to Euler conversion
		(r,p, theta2) = tf.transformations.euler_from_quaternion(q)

		rot1 = atan2(dy, dx) - theta1 #a first rotation
		rot2 = theta2-theta1-rot1  #a second rotation

                #standard deviation for each transformation noise:
		sd_rot1 = a1*abs(rot1) + a2*trans
		sd_rot2 = a1*abs(rot2) + a2*trans
		sd_trans = a3*trans + a4*(abs(rot1) + abs(rot2))
            
                # random normal distribution function with mean and standard deviation, we can add a noise to each transformation as follow:
		trans +=  np.random.normal(0,sd_trans*sd_trans)
		rot1 += np.random.normal(0, sd_rot1*sd_rot1)
		rot2 += np.random.normal(0, sd_rot2*sd_rot2)
                
                # With the added noises, the new position of the robot can be calculated as:
		pose[0] += trans*cos(theta1+rot1)
		pose[1] += trans*sin(theta1+rot1)
		pose[2] = theta1 + rot1 + rot2
		last_odom = data



# Odom topic subscriber
def odom_subscriber():
	rospy.Subscriber("odom",Odometry,odomcallback)

	

# Noisy Odom Publisher
def noise_odom_publisher():
	pub= rospy.Publisher('odom_noise',Odometry,queue_size=50)
	odom_broadcaster=tf.TransformBroadcaster()
	rate=rospy.Rate(50)

	while not rospy.is_shutdown():
		current_time=rospy.Time.now()
		x 	= pose[0]
		y 	= pose[1]
		th  = pose[2]
		vx 	= 0.1
		vy 	= -0.1
		vth = 0.1

		odom_quat = tf.transformations.quaternion_from_euler(0,0,th)
		odom=Odometry()

		odom.header.stamp =current_time
		odom.header.frame_id ="odom"

		odom.pose.pose = Pose(Point(x,y,0),Quaternion(*odom_quat))

		odom.child_frame_id ="base_link"
		odom.twist.twist=Twist(Vector3(vx,vy,0),Vector3(0,0,vth))
		pub.publish(odom)
		last_time=current_time
		rate.sleep()		


if __name__== '__main__':

	# Initializing the node
	rospy.init_node('odom_noise')	

	odom_subscriber()

	noise_odom_publisher()
	
	rospy.spin()
