import time
import os
from pathlib import Path
import numpy as np
import shutil
import piexif
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS

def copy_targets(people_in_picture_array,people_directory):
    print("Now copying images with people from the target directory to the people directory within the program folder")
    for x in people_in_picture_array:
        print(x)
        print("Copying " + str(x) + "to people directory")
        shutil.copy(x, people_directory)

#Below function is not used this time until more testing
def add_metadata_tag(image_path):
    """Add 'People' as a keyword in the image metadata."""
    try:
        image = Image.open(image_path)
        exif_data = piexif.load(image.info.get("exif", b"")) if "exif" in image.info else {}

        if "Exif" not in exif_data:
            exif_data["Exif"] = {}

        existing_comment = exif_data["Exif"].get(piexif.ExifIFD.UserComment, b"").decode("utf-16", errors="ignore").strip()

        if "People" not in existing_comment:
            new_comment = (existing_comment + " People").strip()
            exif_data["Exif"][piexif.ExifIFD.UserComment] = new_comment.encode("utf-16")
            exif_bytes = piexif.dump(exif_data)
            image.save(image_path, exif=exif_bytes)
            
    except Exception as e:
        print(f"Error updating metadata for {image_path}: {e}")

def getImageClasses(class2check):
    yolov8_classes = {0: 'person', 1: 'bicycle', 2: 'car', 3: 'motorcycle', 4: 'airplane', 5: 'bus', 6: 'train', 7: 'truck', 8: 'boat', 9: 'traffic light', 10: 'fire hydrant', 11: 'stop sign', 12: 'parking meter', 13: 'bench', 14: 'bird', 15: 'cat', 16: 'dog', 17: 'horse', 18: 'sheep', 19: 'cow', 20: 'elephant', 21: 'bear', 22: 'zebra', 23: 'giraffe', 24: 'backpack', 25: 'umbrella', 26: 'handbag', 27: 'tie', 28: 'suitcase', 29: 'frisbee', 30: 'skis', 31: 'snowboard', 32: 'sports ball', 33: 'kite', 34: 'baseball bat', 35: 'baseball glove', 36: 'skateboard', 37: 'surfboard', 38: 'tennis racket', 39: 'bottle', 40: 'wine glass', 41: 'cup', 42: 'fork', 43: 'knife', 44: 'spoon', 45: 'bowl', 46: 'banana', 47: 'apple', 48: 'sandwich', 49: 'orange', 50: 'broccoli', 51: 'carrot', 52: 'hot dog', 53: 'pizza', 54: 'donut', 55: 'cake', 56: 'chair', 57: 'couch', 58: 'potted plant', 59: 'bed', 60: 'dining table', 61: 'toilet', 62: 'tv', 63: 'laptop', 64: 'mouse', 65: 'remote', 66: 'keyboard', 67: 'cell phone', 68: 'microwave', 69: 'oven', 70: 'toaster', 71: 'sink', 72: 'refrigerator', 73: 'book', 74: 'clock', 75: 'vase', 76: 'scissors', 77: 'teddy bear', 78: 'hair drier', 79: 'toothbrush'}
    return yolov8_classes[class2check]