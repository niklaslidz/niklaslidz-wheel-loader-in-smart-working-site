#!/usr/bin/env python

# import ROS and math modules
import rospy
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from sensor_msgs.msg import Image
from std_msgs.msg import Empty
from math import *
import numpy as np
import random


from tf.transformations import euler_from_quaternion
from geometry_msgs.msg import (Point, PointStamped, PoseWithCovarianceStamped, Quaternion, Twist)


#Import mapping class as MapDrawer
from map_util_slope import MapDrawer

# open cv for displaying depth image
import cv2
from cv_bridge import CvBridge, CvBridgeError


class Mapper:


    def __init__(self):
        # Initialize node
        rospy.init_node('Mapper', 'time', anonymous=False)  #name node

        # Postion and orientation variables of truck
        self.position = None
        self.orientation = None
        self.start_mapping = False

        # Create map array
        #different surface resistance --> different color(value)
        self.map = -np.ones((80, 120))

        #create mapper object from MapDrawer class and mark starting point of truck
        self.mapper = MapDrawer((40, 60))
       

        # tell user how to stop plot
        rospy.loginfo("To stop plot CTRL + C")

        # What function to call when you ctrl + c    
        rospy.on_shutdown(self.shutdown)

        # Use a CvBridge to convert ROS image type to CV Image (Mat)
        self.bridge = CvBridge()
       
       
        # Subscribe to UKF topic to get pose data
        rospy.Subscriber('/ukf/odometry/filtered/1imu_2gps', Odometry, self.process_ukf)
        # Subscribe to get ground_truth pose data
        rospy.Subscriber('/ground_truth/state', Odometry, self.process_ground_truth)
        
        # Use 8 HZ. NOTE: Higher frequencies break the map image
        self.rate = rospy.Rate(10)
        
        # Wait for position data to be ready
        now = rospy.Time.now()
        while rospy.Time.now() - now < rospy.Duration(1) or self.position is None:
            pass

        # Don't start mapping until your position data is valid
        self.start_mapping = True

        
    def run(self):
        """
        Run (Mapper) until Ctrl+C is pressed
        :return: None
        """
        
        # as long as you haven't ctrl + c keeping doing...
        while not rospy.is_shutdown():

            # update map
            self.mapper.UpdateMapDisplay(self.map, self.WorldPositionToMap(self.position), self.WorldPositionToMap(self.real_position))
            # wait for 0.125 seconds (8 HZ) and publish again
            self.rate.sleep()

    def WorldPositionToMap(self, position):
        map_scale = 1
        if position == None:
            return (0,0)
        else:
            x_steps = position[0] / map_scale
            y_steps = position[1] / map_scale
            return (x_steps + 40, y_steps + 60) 

    def process_ukf(self, data):
        """
        Updates the current position of the robot and marks any cells under the
        robot as Empty.
        :param data: Raw message data from the UKF
        :return: None
        """
        # Save the position and orientation
        pos = data.pose.pose.position
        self.position = (pos.x, pos.y)
        quat = data.pose.pose.orientation
        list_quat = [quat.x, quat.y, quat.z, quat.w]
        self.orientation = euler_from_quaternion(list_quat)[-1]

        # Extract the relevant covariances (uncertainties).
        # Note that these are uncertainty on the robot VELOCITY, not position
        cov = np.reshape(np.array(data.pose.covariance), (6, 6))
        x_var = cov[0, 0]
        y_var = cov[1, 1]
        rot_var = cov[5, 5]



        # continuously update the path traced by the truck 
        if self.start_mapping:
            map_pos = self.WorldPositionToMap(self.position)
            self.map[int(map_pos[0] - 0.5):int(map_pos[0] + 0.5)+1, int(map_pos[1] - 0.5):int(map_pos[1] + 0.5)+1] = 0

    def process_ground_truth(self, data):

        # Save the position and orientation
        pos2 = data.pose.pose.position
        self.real_position = (pos2.x, pos2.y)
        quat2 = data.pose.pose.orientation
        list_quat2 = [quat2.x, quat2.y, quat2.z, quat2.w]
        self.orientation2 = euler_from_quaternion(list_quat2)[-1]

        # Extract the relevant covariances (uncertainties).
        # Note that these are uncertainty on the robot VELOCITY, not position
        cov2 = np.reshape(np.array(data.pose.covariance), (6, 6))
        x_var2 = cov2[0, 0]
        y_var2 = cov2[1, 1]
        rot_var2 = cov2[5, 5]

        # diplay position and orientation of truck
        #rospy.loginfo({"position": self.real_position})
        #rospy.loginfo({"orientation": self.orientation2})

        
    def shutdown(self):
        """
        Pre-shutdown routine. Stops the robot before rospy.shutdown 
        :return: None
        """
        # save map
        rospy.loginfo("Saving Map")
        self.mapper.SaveMap('/home/hanke/catkin_ws/src/mapper_slope/solution_map_slope.jpg')
        

        # stop truck
        rospy.loginfo("Stop truck")
        # a default Twist has linear.x of 0 and angular.z of 0.  So it'll stop truck
        
        # sleep just makes sure truck receives the stop command prior to shutting down the script
        rospy.sleep(5)


if __name__ == '__main__':
    try:
        mapper = Mapper()
        mapper.run()
    except Exception, err:
        rospy.loginfo("Mapper node terminated.")
        print err
