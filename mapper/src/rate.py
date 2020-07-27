

# past this to measure the rate of execution

# put this in the init section
# measure freq
        self.last_time = rospy.Time.now()


# put this in the function to probe
if (rospy.Time.now() - self.last_time).nsecs != 0:
                rospy.loginfo({"freq":10**9/(rospy.Time.now() - self.last_time).nsecs})
                self.last_time = rospy.Time.now()