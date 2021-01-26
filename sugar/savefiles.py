"""Save files."""
#Django
from django.core.files.uploadedfile import InMemoryUploadedFile

# Models
from detections.models import Detection, Note

# Math libs
import numpy as np
import matplotlib.pyplot as plt  # Plot images

# My apps
from .clouster import cloustering
from .folders import ifExist, ifFolder
from PIL import Image

# Others
import os
from io import BytesIO


def SaveVI(vi, N=None, color_map='RdYlGn', vi_path=None):
    """Save or plot vegetation index image."""
    ifExist(path_file=vi_path,request_file=None)

    if N is None:
        # Guardar imagen simple de indice de vegetacion
        plt.figure(figsize=(16.92,12.72), dpi=100)
        plt.imshow(vi, cmap=color_map)
        plt.axis("off")
        plt.savefig(vi_path, dpi=100, bbox_inches='tight', pad_inches=0)
    else:
        # Obtener las escalas de colores
        cmap = plt.get_cmap(color_map, N)
        # Segmentacion por cloustering
        img,vmin,vmax = cloustering(vi,N)
        # Guardar imagen cloustering de indice de vegetacion
        plt.figure(figsize=(16.92,12.72), dpi=100)
        plt.imshow(img, cmap=cmap,vmin=vmin, vmax=vmax)
        plt.axis("off")
        plt.savefig(vi_path, dpi=100, bbox_inches='tight', pad_inches=0)


def SaveFile(request_file, user):
    """Save bands images in temp file."""
    if 'RGB' in request_file.name:
        name = 'RGB_temp.JPG'
    elif 'NIR' in request_file.name:
        name = 'NIR_temp.TIF'
    elif 'RED' in request_file.name:
        name = 'RED_temp.TIF'
    else:
        name = 'Other_temp.JPG'

    path = os.getcwd()
    path_folder = path + '/media/temp/bands/' + str(user) + '/'
    path_file =  path_folder + name

    ifFolder(path_folder)
    ifExist(path_file=path_file, request_file=request_file)


def SaveDetection(request,user,profile,detection_name,status,note_name,note_text):
    """Save detection in DB."""
    #https://stackoverflow.com/questions/35581356/save-matplotlib-plot-image-into-django-model/35633462
    #https://stackoverflow.com/questions/3723220/how-do-you-convert-a-pil-image-to-a-django-file

    # Paths
    path_picture = 'media/temp/bands/'+str(request.user.username)+'/RGB_temp.JPG'
    path_picture_ndvi ='media/temp/results/'+str(request.user.username)+'/NDVI.jpg'
    path_picture_savi ='media/temp/results/'+str(request.user.username)+'/SAVI.jpg'
    path_picture_evi2 ='media/temp/results/'+str(request.user.username)+'/EVI2.jpg'

    picture_name = 'RGB.jpg'
    picture_ndvi_name = 'NDVI.jpg'
    picture_savi_name = 'SAVI.jpg'
    picture_evi2_name = 'EVI2.jpg'

    path_pictures = [path_picture,path_picture_ndvi,path_picture_savi,path_picture_evi2]
    picture_names = [picture_name,picture_ndvi_name,picture_savi_name,picture_evi2_name]
    picture_files = []

    for path,name in zip(path_pictures,picture_names):
        picture_file = Image.open(path)
        tempfile_io = BytesIO()
        picture_file.save(tempfile_io, format='JPEG')
        picture_file = InMemoryUploadedFile(tempfile_io, None, name,'image/jpeg',tempfile_io.tell, None)
        picture_files.append(picture_file)

    detection_instance = Detection(
        user=user,
        profile=profile,
        name=detection_name,
        satatus_of_field=status,
        )

    detection_instance.picture.save(picture_name, picture_files[0])
    detection_instance.picture_ndvi.save(picture_ndvi_name, picture_files[1])
    detection_instance.picture_savi.save(picture_savi_name, picture_files[2])
    detection_instance.picture_evi2.save(picture_evi2_name, picture_files[3])
    detection_instance.save()

    if note_name:
        note_instance = Note(
            note_detection=detection_instance,
            name=note_name,
            user=user,
            text=note_text,
        )
        note_instance.save()

    return True
