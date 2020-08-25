# script to import solution image and display it on an open cv window for 5 seconds

import cv2

img = cv2.imread('solution_map.jpg', 1)
cv2.imshow('image',img)
cv2.waitKey(5000)
cv2.destroyAllWindows()
exit()