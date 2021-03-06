# Wheel loader in smart working site
## 1.Run the Wheel loader
Open  niklaslidz-wheel-loader-in-smart-working-site/loader/launch/   
```bash
 roslaunch  loader gazebo.launch
 ```
 
 ![image](https://github.com/niklaslidz/niklaslidz-wheel-loader-in-smart-working-site/blob/master/img/img_gazebo.png)
 ## 2.Run the Controller to move the wheel loader
 Open niklaslidz-wheel-loader-in-smart-working-site/loader_cont/launch/
 ```bash
 roslaunch  loader_cont loader_control.launch
 ```
 Moving around:  
 w : **forward**      
 a : **left turn**  
 s : **backward**  
 d : **right turn**  
 x : **stop the wheel loader**  
 c : **stop turning**  
   
CTRL-C to quit
 
 
 ## 3.Run the plotter
 Open  niklaslidz-wheel-loader-in-smart-working-site/loader/launch/ 
 ```bash
 roslaunch  loader plot.launch
 roslaunch  loader plot_2.launch
 ```
 run two nodes to plot different sensor sonfiguration (EKF 1 IMU 1 GPS ) and (UKF 1IMU 2 GPS)

 ## 4.Saved maps
the different maps will be saved in   
niklaslidz-wheel-loader-in-smart-working-site/mapper/  
niklaslidz-wheel-loader-in-smart-working-site/mapper_2/  
niklaslidz-wheel-loader-in-smart-working-site/mapper_slope  
niklaslidz-wheel-loader-in-smart-working-site/mapper_slope_2  

change the path to save the maps in    
**niklaslidz-wheel-loader-in-smart-working-site/mapper/src/map_mapper.py /  
niklaslidz-wheel-loader-in-smart-working-site/mapper_2/src/map_mapper_2.py /  
niklaslidz-wheel-loader-in-smart-working-site/mapper_slope/src/map_mapper_slope.py /  
niklaslidz-wheel-loader-in-smart-working-site/mapper_slope_2/src/map_mapper_slope_2.py /**
folder  
 ```bash
self.mapper.SaveMap('/home/hanke/catkin_ws/src/mapper/solution_map.jpg')
 ```
 
  ## 5.Results 
![image](https://github.com/niklaslidz/niklaslidz-wheel-loader-in-smart-working-site/blob/master/plot_video.gif) 
 
 ## 6. Principle
 ### (1)Localization with [Robot_localization](http://wiki.ros.org/robot_localization)
 <div align=center><img width="400" src="https://github.com/niklaslidz/niklaslidz-wheel-loader-in-smart-working-site/blob/master/img/overall%20architecture%20of%20the%20localization%20scheme.png"/></div> 
 
 ### (2)Real time plotter
<center class="half">
 <img src="https://github.com/niklaslidz/niklaslidz-wheel-loader-in-smart-working-site/blob/master/img/0001.jpg" width="400"/><img src="https://github.com/niklaslidz/niklaslidz-wheel-loader-in-smart-working-site/blob/master/img/one_layers_page-0001.jpg" width="400"/>
</center>
