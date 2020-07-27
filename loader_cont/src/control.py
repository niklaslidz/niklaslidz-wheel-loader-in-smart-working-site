#!/usr/bin/env python

import math
import rospy
import os 
import sys  
import tty, termios  
import roslib; roslib.load_manifest('teleop_twist_keyboard')
from std_msgs.msg import Float64

pub_j1 = rospy.Publisher('/loader/joint1_velocity_controller/command', Float64, queue_size= 10)
pub_j2 = rospy.Publisher('/loader/joint2_velocity_controller/command', Float64, queue_size=10)
pub_j3 = rospy.Publisher('/loader/joint3_velocity_controller/command', Float64, queue_size= 10)
pub_j4 = rospy.Publisher('/loader/joint4_velocity_controller/command', Float64, queue_size=10)
pub_j5 = rospy.Publisher('/loader/joint5_velocity_controller/command', Float64, queue_size=10)

def print_usage(self):
    msg = """
Reading from the keyboard  and Publishing to Twist!
use WASD keys to control the wheel loader
---------------------------
Moving around:
        w : forward    
        a : left
        s : back   
        d : right
        x : stop
        c : stop turn
   

CTRL-C to quit
"""
    self.loginfo(msg)

def loginfo(self, str):
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.settings)
    print(str)
    tty.setraw(sys.stdin.fileno())

def mover():
    rospy.init_node('pub_control')
    rate = rospy.Rate(30)
      
    while not rospy.is_shutdown():  
        fd = sys.stdin.fileno()  #standard input
        old_settings = termios.tcgetattr(fd)   
        old_settings[3] = old_settings[3] & ~termios.ICANON & ~termios.ECHO  
        try :  
            tty.setraw( fd )  #read a single character from the user
            ch = sys.stdin.read( 1 )  
        finally :  
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

        if ch == 'w':    
            pub_j1.publish(5)
            pub_j2.publish(5)
            pub_j3.publish(5)
            pub_j4.publish(5)
        elif ch == 's':
            pub_j1.publish(-5)
            pub_j2.publish(-5)
            pub_j3.publish(-5)
            pub_j4.publish(-5)
        elif ch == 'a':
            pub_j5.publish(80000.0)

        elif ch == 'd':
            pub_j5.publish(-80000.0)

        elif ch == 'c':
            pub_j5.publish(0)

        elif ch == 'x':
            pub_j1.publish(0)
            pub_j2.publish(0)
            pub_j3.publish(0)
            pub_j4.publish(0)
        rate.sleep()
        ##stop_loader(); if want loader stop when not press keyboard

def stop_loader():
    pub_j1.publish(0)
    pub_j2.publish(0)
    pub_j3.publish(0)
    pub_j4.publish(0)

if __name__ == '__main__':
    try:
        mover()
        self.print_usage()
    except rospy.ROSInterruptException:
        pass
