"""Create folders."""
#Django
from django.core.files.storage import FileSystemStorage

# Others
import os
from PIL import Image
import cv2


def ifExist(path_file, request_file, mosaic=None):
    """Check if exists a folder."""
    # https://docs.djangoproject.com/en/3.1/ref/files/storage/
    fs = FileSystemStorage()
    if fs.exists(path_file):
        fs.delete(path_file)

    if request_file:
        file = fs.save(path_file, request_file)  #request_file.name
    # the fileurl variable now contains the url to the file. This can be used to serve the file when needed.
    # fileurl = fs.url(file)

    if not mosaic is None:
        if mosaic is True and 'RGB_temp.TIF' in path_file:
            outfile = path_file[:-3] + "JPG"
            ima = Image.open(path_file)
            ima.convert("RGB").save(outfile, "JPEG", quality=100)

        elif mosaic is False and 'RGB_temp.JPG' in path_file:
            img = Image.open(path_file)
            img = img.rotate(180) # 90, -90, 180, ...
            img.save(path_file) # to override your old file


def ifFolder(path):
    """Check if folder exists."""
    if not os.path.exists(path):
        try:
            os.mkdir(path)
        except OSError:
            print ("Creation of the directory %s failed" % path)

def rgb2gray(img,path,img_path):
    if not os.path.exists(path):
        try:
            os.mkdir(path)
        except OSError:
            print ("Creation of the directory %s failed" % path)
    img = Image.open(img).convert('L')
    img.save(img_path)
