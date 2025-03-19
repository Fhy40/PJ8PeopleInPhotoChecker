
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
from ultralytics import YOLO
import cv2
import numpy as np
from FileTag_Functions import *
import sys
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS

start_time = time.time()
picture_array = []
#change PICTURE_DIRECTORY to change default location, use word 'default' for default location
PICTURE_DIRECTORY = 'E:\\TEST'
TARGET_DIRECTORY = 'output'
DEBUG_MODE = 1
#Change DEBUG_MODE to 0 to stop printing debug information to the console
current_working_directory = os.getcwd()
CONF_VALUE = 0.50
IMAGE_CLASSES = [0]
IMAGE_EXTENSIONS = [".jpg", ".jpeg", ".png", ".tiff", ".webp", ".heic"]
gonogo = 0


DRIVE = input(r"Enter the Drive to scan for images e.g. E or C: ").strip()
print(DRIVE + ": Drive selected")
directory = input('Enter directory to analyze, use word '"default"' for default location:')
if (directory=="default"):
    PICTURE_DIRECTORY = PICTURE_DIRECTORY
else:
    PICTURE_DIRECTORY = DRIVE + ":\\" + directory

TARGET_DRIVE = input(r"Enter the Drive to output images to e.g. E or C: ").strip()
target_directory = input('Enter directory to output pictures to: ')
if (target_directory=="default"):
    TARGET_DIRECTORY = TARGET_DIRECTORY
else:
    TARGET_DIRECTORY = TARGET_DRIVE + ":\\" + target_directory


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
            
except:
    print("An exception occurred, you might not have entered a proper directory")
    print("This is what you entered: " + PICTURE_DIRECTORY)

if(len(picture_array) == 0):
    print("An exception occurred, you might not have entered a proper directory")    
    print("This is what you entered: " + PICTURE_DIRECTORY)
    print("There are no images in the directory specified, exiting now")
    sys.exit()
while gonogo == 0:
    print("Current Directory Selected " + str(PICTURE_DIRECTORY))
    print("Current Image Extensions to Scan " + str(IMAGE_EXTENSIONS))
    print("Current Detection Classes to Searh in Images " + str(IMAGE_CLASSES) + " which is " + str(getImageClasses(IMAGE_CLASSES[0])))
    print("Current Detection Confidence Value is " + str(CONF_VALUE))
    print("-------------------------------------------------------------------")
    print('Would you like to continue with the parameters above? type yes to continue')
    print('type classes to get a list of avaliable classes, type exit to stop the program')
    finalcheck = input('Type your command here: ')

    if(finalcheck == "yes"):
        print("Thank you, the program will run now with the parameters specified")
        gonogo = 1
    elif(finalcheck == "classes"):
        print(MODEL_PATH.names)
        print("")        
    elif(finalcheck == "exit"):
        print("Exiting in 5 seconds")
        time.sleep(5)
        sys.exit()
    else:
        print("You did not specify a valid command, exiting now")
        sys.exit()


errors = 0
detection_count = 0
for target in picture_array:    
    try:
        results = MODEL_PATH(target, conf=CONF_VALUE, classes=IMAGE_CLASSES)
        #change confidence values up or down depending on if it's too easy or too hard to detect people
        if(DEBUG_MODE == 1):
            print("❤️❤️❤️ " + str(results[0].boxes.data))
            print("🍔🍔🍔 " + str(results[0].probs))
            print("🍔🍔🍔 " + str(results[0].boxes.xyxy))
        boxes = results[0].boxes.xyxy

        if len(boxes) > 0:
            if(DEBUG_MODE == 1):
                print("PERSON WAS DETECTED")
            people_in_picture_array.append(target)
            detection_count += 1  

            # Draw bounding box on image
            x1, y1, x2, y2 = map(int, boxes[0])  
            #img = cv2.rectangle(target, (x1, y1), (x2, y2), (255, 0, 0), 2)
        else:
            if(DEBUG_MODE == 1):
                print(f"No detections found in {target}")
    except:
        print("An exception occurred")
        errors = errors + 1
    
copy_targets(people_in_picture_array,TARGET_DIRECTORY)

print("----------------------------------------------------------------------------------")
print("There were a total of " + str(len(picture_array)) + " pictures that were analyzed")        
print("There were " + str(errors) + " Errors Found")
print("There were " + str(detection_count) + " people detected")
print("--- %s seconds ---" % (time.time() - start_time))

