from math import *
import numpy as np
import cv2

class MapDrawer:
    """
    A class for incrementally updating the displayed image of the generated map,
    and saving the image to file.  The map must be an occupancy grid of shape
    (80, 120).
    """

    def __init__(self, start_pos):
        """
        Creates a new MapDrawer object that can be used for visualizing and
        saving your map. Requires the initial position on the map of the robot,
        `start_pos`, for later
        """
        self.map_size = (80, 120) #control the move area
        self.draw_scale = 4
        self.bot_scale = 4 #radius
        self.map = -np.ones(self.map_size).astype(int)
        self.drawn_map = np.zeros((320, 480, 3))
        self.map_colors = [[0, 0, 255], [255, 255, 255], [255, 0, 0],
                           [255, 0, 255], [255, 255, 0], [0, 255, 255]]
        self.start_pos = np.array(start_pos) * self.draw_scale
        self.start_pos = (int(self.start_pos[1]), int(self.start_pos[0]))

    def UpdateMapDisplay(self, new_map, position, real_position):
        for ii in np.ndindex(self.map_size):
            if self.map[ii] == int(new_map[ii]):
                continue
            if 40 > real_position[1] >= 15 and 42 > real_position[0] >= 16:
                self.map[ii] = int(new_map[ii])
                pt1 = (int(self.draw_scale*ii[1]), int(self.draw_scale*ii[0]))
                pt2 = (int(self.draw_scale*(ii[1]+ 1)), int(self.draw_scale*(ii[0] + 1)))
                color = self.map_colors[self.map[ii] + 0]  
                cv2.rectangle(self.drawn_map, pt1, pt2, color, -1) #pt1 pt2 left upper corner and right corner -1 fill the rectangle
            elif 95 > real_position[1] >= 40 and 30 > real_position[0] >= 16: 
                self.map[ii] = int(new_map[ii])
                pt1 = (int(self.draw_scale*ii[1]), int(self.draw_scale*ii[0]))
                pt2 = (int(self.draw_scale*(ii[1]+ 1)), int(self.draw_scale*(ii[0] + 1)))
                color = self.map_colors[self.map[ii] + 0]  
                cv2.rectangle(self.drawn_map, pt1, pt2, color, -1) #pt1 pt2 left upper corner and right corner -1 fill the rectangle
            
            elif 40 > real_position[1] >= 25 and 60 > real_position[0] >= 42: 
                self.map[ii] = int(new_map[ii])
                pt1 = (int(self.draw_scale*ii[1]), int(self.draw_scale*ii[0]))
                pt2 = (int(self.draw_scale*(ii[1]+ 1)), int(self.draw_scale*(ii[0] + 1)))
                color = self.map_colors[self.map[ii] + 0]  
                cv2.rectangle(self.drawn_map, pt1, pt2, color, -1) #pt1 pt2 left upper corner and right corner -1 fill the rectangle
                        
            elif 95 > real_position[1] >= 40 and 60 > real_position[0] >= 50:  
                self.map[ii] = int(new_map[ii])
                pt1 = (int(self.draw_scale*ii[1]), int(self.draw_scale*ii[0]))
                pt2 = (int(self.draw_scale*(ii[1]+ 1)), int(self.draw_scale*(ii[0] + 1)))
                color = self.map_colors[self.map[ii] + 0]  
                cv2.rectangle(self.drawn_map, pt1, pt2, color, -1) #pt1 pt2 left upper corner and right corner -1 fill the rectangle
            
            elif 95 > real_position[1] >= 70 and 50 > real_position[0] >= 30:  
                self.map[ii] = int(new_map[ii])
                pt1 = (int(self.draw_scale*ii[1]), int(self.draw_scale*ii[0]))
                pt2 = (int(self.draw_scale*(ii[1]+ 1)), int(self.draw_scale*(ii[0] + 1)))
                color = self.map_colors[self.map[ii] + 0]  
                cv2.rectangle(self.drawn_map, pt1, pt2, color, -1) #pt1 pt2 left upper corner and right corner -1 fill the rectangle
            else:
                self.map[ii] = int(new_map[ii])
                pt1 = (int(self.draw_scale*ii[1]), int(self.draw_scale*ii[0]))
                pt2 = (int(self.draw_scale*(ii[1]+ 1)), int(self.draw_scale*(ii[0] + 1)))
                color = self.map_colors[self.map[ii] + 4]  
                cv2.rectangle(self.drawn_map, pt1, pt2, color, -1) #pt1 pt2 left upper corner and right corner -1 fill the rectangle
        img = np.copy(self.drawn_map)

        current_pos = np.array(position) * self.draw_scale
        current_pos = (int(current_pos[1]), int(current_pos[0]))
        cv2.circle(img, self.start_pos, self.bot_scale, [0, 1, 0], -1)
        cv2.circle(img, current_pos, self.bot_scale, [0, 0, 1], -1)

            
        cv2.imshow('solution_map', img)
        cv2.waitKey(5)
        cv2.imwrite('/home/hanke/catkin_ws/src/mapper_slope_2/solution_map_slope.jpg', img)
    def SaveMap(self, filename):
        """
        Saves the stored map to file `filename`, with the initial position of
        the robot, passed in the constructor, and the current position of the
        robot, `position`, included on the map.
        """
        img = np.copy(self.drawn_map)

        cv2.imwrite(filename, img)


if __name__ == '__main__':
    import time

    start_pos = (40, 60)
    mapper = MapDrawer(start_pos)
    my_map = -np.ones((80, 120))

    # Sending first image twice as the first image drawn does not fully render
    mapper.UpdateMapDisplay(my_map, start_pos)
    mapper.UpdateMapDisplay(my_map, start_pos)
    time.sleep(3)

    my_map[start_pos[0], start_pos[1]] = 0
    my_map[start_pos[0]-1, start_pos[1]] = 0
    my_map[start_pos[0]-1, start_pos[1]-1] = 0
    my_map[start_pos[0], start_pos[1]-1] = 0

    mapper.UpdateMapDisplay(my_map, start_pos)
    time.sleep(3)

    
