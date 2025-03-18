import time
import os
from pathlib import Path
import numpy as np
import shutil
import piexif
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS

def copy_people(people_in_picture_array,people_directory):
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