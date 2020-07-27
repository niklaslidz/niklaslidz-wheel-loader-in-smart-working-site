# Odometry_noise

### Odom_noise node

With this ROS node all relevant data from Odometry source added with noise and published into ROS under '/odom_noise' topic name. 


#### How to install?
clone the folder '*Odom_noise node*' into your `catkin_ws/src folder` 
and run in the top folder the catkin_make command 

#### How to run? 
In the launch folder of the repository`odom_noise.launch` file starts the node.

#### Steps to run for odom_noise

+ Clone the package into your workspace and run the catkin_make command in the top folder.
+ Make sure `scripts/odom_noise.py` is executable.
+ Find `odom_noise.launch` in launch folder. It runs the following node:
    + **odom_noise**
        + **Publications**:
             + /odom_noise [nav_msgs/Odometry]
             + /rosout [rosgraph_msgs/Log]
             + /tf *[tf2_msgs/TFMessage]*
        + **Subscriptions**: 
             + /odom [unknown type]
