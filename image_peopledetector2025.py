
###############################################################################
#                                                                             #
# IMAGE Tagging v2.0.0                                                        #
#                                                                             #
# Description: Scans a folder that is specified as a command and sees if      #
# if they contain people using AI-based detection. If people                  #
# are detected, the script copies the image to a directory called people in   #
# in the programs working directory.                                          #
#                                                                             #
# Features: - Recursively searches for image files                            #
#           - Uses AI-based people detection                                  #
#           - Uses yolov8n                                                    #
#           - Copies images with people to a seperate directory               #
#                                                                             #
# Created by: Arjun Sundram                                                   #
# Updated on: 2025-03-18                                                      #
###############################################################################

import time
import os
from pathlib import Path
from progressbar import *
from ultralytics import YOLO
import cv2
import numpy as np
from functions import *
import sys
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS

start_time = time.time()
picture_array = []
#change PICTURE_DIRECTORY to change default location, use word 'default' for default location
PICTURE_DIRECTORY = 'C:\\Users\\arjun\\OneDrive\\Desktop\\Pics\\TEST'
people_directory = 'people'
current_working_directory = os.getcwd()
IMAGE_EXTENSIONS = [".jpg", ".jpeg", ".png", ".tiff", ".webp", ".heic"]

x = input('Enter directory to analyze, use word '"default"' for default location:')
if (x=="default"):
    PICTURE_DIRECTORY = PICTURE_DIRECTORY
else:
    PICTURE_DIRECTORY = x

directory = os.fsencode(PICTURE_DIRECTORY)
MODEL_PATH = YOLO("yolov8n.pt")
people_in_picture_array = []

try:
    for x in IMAGE_EXTENSIONS:
        print(x)
        pathlist = Path(PICTURE_DIRECTORY).rglob(f'*{x}')
        for path in pathlist:    
            path_in_str = str(path)
            picture_array.append(path_in_str)
            print(path)
except:
    print("An exception occurred, you might not have entered a proper directory")
    print("This is what you entered: " + PICTURE_DIRECTORY)

if(len(picture_array) == 0):
    print("An exception occurred, you might not have entered a proper directory")    
    print("This is what you entered: " + PICTURE_DIRECTORY)
    print("There are no images in the directory specified, exiting now")
    sys.exit()


errors = 0
detection_count = 0


for target in picture_array:    
    try:
        results = MODEL_PATH(target, conf=0.50, classes=[0,5])
        #change confidence values up or down depending on if it's too easy or too hard to detect people
        print("❤️❤️❤️ " + str(results[0].boxes.data))
        print("🍔🍔🍔 " + str(results[0].probs))
        print("🍔🍔🍔 " + str(results[0].boxes.xyxy))
        boxes = results[0].boxes.xyxy

        if len(boxes) > 0:
            print("PERSON WAS DETECTED")
            people_in_picture_array.append(target)
            detection_count += 1  

            # Draw bounding box on image
            x1, y1, x2, y2 = map(int, boxes[0])  
            #img = cv2.rectangle(target, (x1, y1), (x2, y2), (255, 0, 0), 2)
        else:
            print(f"No detections found in {target}")
    except:
        print("An exception occurred")
        errors = errors + 1
    
copy_people(people_in_picture_array,people_directory)


print("There were a total of " + str(len(picture_array)) + " pictures that were analyzed")        
print("There were " + str(errors) + " Errors Found")
print("There were " + str(detection_count) + " people detected")
print("--- %s seconds ---" % (time.time() - start_time))

