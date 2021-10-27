import cv2
import numpy as np
 
class Detection(object):
 
    THRESHOLD = 1500
 
    def __init__(self, image):
        self.previous_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
 
    def get_active_cell(self, image):
        # obtain motion between previous and current image
        current_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        delta = cv2.absdiff(self.previous_gray, current_gray)
        threshold_image = cv2.threshold(delta, 25, 255, cv2.THRESH_BINARY)[1]
 
        # debug
##        cv2.imshow('OpenCV Detection', current_gray)
        cv2.waitKey(10)
 
        # store current image
        self.previous_gray = current_gray
 
        # set cell width
        height, width = threshold_image.shape[:2]
        cell_width = width/7
 
        # store motion level for each cell
        cells = np.array([0, 0, 0, 0, 0, 0, 0])
        cells[0] = cv2.countNonZero(threshold_image[0:height, 0:cell_width])
        cells[1] = cv2.countNonZero(threshold_image[0:height, cell_width:cell_width*2])
        cells[2] = cv2.countNonZero(threshold_image[0:height, cell_width*2:cell_width*3])
        cells[3] = cv2.countNonZero(threshold_image[0:height, cell_width*3:cell_width*4])
        cells[4] = cv2.countNonZero(threshold_image[0:height, cell_width*4:cell_width*5])
        cells[5] = cv2.countNonZero(threshold_image[0:height, cell_width*5:cell_width*6])
        cells[6] = cv2.countNonZero(threshold_image[0:height, cell_width*6:width])
 
        # obtain the most active cell
        top_cell =  np.argmax(cells)
 
        # return the most active cell, if threshold met
        if(cells[top_cell] >= self.THRESHOLD):
            return top_cell
        else:
            return None
