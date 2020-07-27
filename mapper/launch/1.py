from math import *
import numpy as np
import cv2

map_size = (80, 120) #control the move area
draw_scale = 4
map = -np.ones(map_size).astype(int)
drawn_map = np.zeros((320, 480, 3))
map_colors = [[0, 0, 255], [255, 255, 255], [255, 0, 0],
             [255, 0, 255], [255, 255, 0], [0, 255, 255]]   #why not RGB?   #1:red 2:white  3:blue 4:purple 5:green 6:yellow choose color from defined colors above

filename = 'savedImage.jpg'

def GroundtruthMap():
    for i in range (0,80):
        for j in range (0,120):
            if j < 105 and i <16:
                pt1 = (int(draw_scale*j), int(draw_scale*i))
                pt2 = (int(draw_scale*(j+ 1)), int(draw_scale*(i + 1)))
                color = map_colors[map[i,j] + 5]  
                cv2.rectangle(drawn_map, pt1, pt2, color, -1) #pt1 pt2 left upper corner and right corner -1 fill the rectangle
            
            elif j >= 105 and i < 70:
                pt1 = (int(draw_scale*j), int(draw_scale*i))
                pt2 = (int(draw_scale*(j+ 1)), int(draw_scale*(i + 1)))
                color = map_colors[map[i,j] + 3]  
                cv2.rectangle(drawn_map, pt1, pt2, color, -1) #pt1 pt2 left upper corner and right corner -1 fill the rectangle
            
            elif j < 15 and 16 <= i < 70:
                pt1 = (int(draw_scale*j), int(draw_scale*i))
                pt2 = (int(draw_scale*(j+ 1)), int(draw_scale*(i + 1)))
                color = map_colors[map[i,j] + 6]  
                cv2.rectangle(drawn_map, pt1, pt2, color, -1) #pt1 pt2 left upper corner and right corner -1 fill the rectangle
             
            elif 15 <= j < 25 and 42 <= i < 60:
                pt1 = (int(draw_scale*j), int(draw_scale*i))
                pt2 = (int(draw_scale*(j+ 1)), int(draw_scale*(i + 1)))
                color = map_colors[map[i,j] + 6]  
                cv2.rectangle(drawn_map, pt1, pt2, color, -1) #pt1 pt2 left upper corner and right corner -1 fill the rectangle

            elif 15 <= j < 95 and 60 <= i < 70:
                pt1 = (int(draw_scale*j), int(draw_scale*i))
                pt2 = (int(draw_scale*(j+ 1)), int(draw_scale*(i + 1)))
                color = map_colors[map[i,j] + 6]  
                cv2.rectangle(drawn_map, pt1, pt2, color, -1) #pt1 pt2 left upper corner and right corner -1 fill the rectangle

            elif 95 <= j < 105 and  16 <= i < 70:
                pt1 = (int(draw_scale*j), int(draw_scale*i))
                pt2 = (int(draw_scale*(j+ 1)), int(draw_scale*(i + 1)))
                color = map_colors[map[i,j] + 6]  
                cv2.rectangle(drawn_map, pt1, pt2, color, -1) #pt1 pt2 left upper corner and right corner -1 fill the rectangle
                        
            elif 70 <= i:
                pt1 = (int(draw_scale*j), int(draw_scale*i))
                pt2 = (int(draw_scale*(j+ 1)), int(draw_scale*(i + 1)))
                color = map_colors[map[i,j] + 2]  
                cv2.rectangle(drawn_map, pt1, pt2, color, -1) #pt1 pt2 left upper corner and right corner -1 fill the rectangle

            else:
                pt1 = (int(draw_scale*j), int(draw_scale*i))
                pt2 = (int(draw_scale*(j+ 1)), int(draw_scale*(i + 1)))
                color = map_colors[map[i,j] + 1]  
                cv2.rectangle(drawn_map, pt1, pt2, color, -1) #pt1 pt2 left upper corner and right corner -1 fill the rectangle
    img = np.copy(drawn_map)


            
        #rotated = np.rot90(img, 1) # rotate image CCW
    cv2.imshow('Map', img)
    cv2.waitKey(5)

    
def SaveMap():
    img = np.copy(drawn_map)
    cv2.imwrite(filename, img)


if __name__ == "__main__":
    GroundtruthMap()
    SaveMap()


