# niklaslidz-wheel-loader-in-smart-working-site
## 1.Run the Wheel loader
Open  niklaslidz-wheel-loader-in-smart-working-site/loader/launch/   
```bash
 roslaunch  loader gazebo.launch
 ```
 ## 2.Run the Controller to move the wheel loader
 Open niklaslidz-wheel-loader-in-smart-working-site/loader_cont/launch/
 ```bash
 roslaunch  loader_cont loader_control.launch
 ```
 ## 2.Run the plotter
 Open  niklaslidz-wheel-loader-in-smart-working-site/loader/launch/ 
 ```bash
 roslaunch  loader plot.launch
 roslaunch  loader plot_2.launch
 ```
 run two nodes to plot different sensor sonfiguration (EKF 1 IMU 1 GPS ) and (UKF 1IMU 2 GPS)
