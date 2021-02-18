"""Save files."""
#Django
from django.core.files.uploadedfile import InMemoryUploadedFile

# Models
from detections.models import Detection, Note

# Math libs
import numpy as np
import matplotlib.pyplot as plt  # Plot images
import matplotlib as mpl
# My apps
from .clouster import cloustering
from .folders import ifExist, ifFolder
from PIL import Image

# Others
import os
from io import BytesIO

def semaforo(vmin,vmax,cmap,N):
  # Normalizer
  norm = mpl.colors.Normalize(vmin=vmin, vmax=vmax)
  # creating ScalarMappable
  sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
  sm.set_array([])
  return sm


def SaveVI(vi, N=None, color_map='RdYlGn', vi_path=None, mosaic=False):
    """Save or plot vegetation index image."""
    ifExist(path_file=vi_path,request_file=None)
    vmin, vmax = np.nanpercentile(vi, (1,99))
    # Inicializar la figura
    if N is None:
        fig = plt.figure()
        # Guardar imagen simple de indice de vegetacion a escala de grises
        if mosaic is True:
            plt.figure(figsize=(9,25), dpi=100)
        else:
            plt.figure(figsize=(16.92,12.72), dpi=100)

        if 'NDVI_4_mask.jpg' in vi_path:
            plt.imshow(vi, cmap=color_map, vmin=vmin, vmax=vmax)
        else:
            plt.imshow(vi, cmap=color_map, vmin=np.min(vi), vmax=np.max(vi))
        plt.axis("off")
        plt.savefig(vi_path, bbox_inches='tight', pad_inches=0)

    else:
        # Obtener las escalas de colores
        cmap = plt.get_cmap(color_map, N)
        #Segmentacion por cloustering
        img,vmin,vmax = cloustering(vi,N)

        fig, ax = plt.subplots()
        fig.set_size_inches(22.94, 33.94)
        cax = fig.add_axes([0.14, 0.32, 0.01, 0.15])  # si esta en vertial (x,y, ancho, alto)
        # Guardar imagen cloustering de indice de vegetacion a color
        im = ax.imshow(img, cmap=cmap,vmin=vmin, vmax=vmax)
        fig.colorbar(semaforo(vmin,vmax,cmap,N), cax=cax, orientation='vertical',)
        ax.axis("off")
        fig.savefig(vi_path, bbox_inches='tight', pad_inches=0)


def SaveFile(request_file, user):
    """Save bands images in temp file."""
    mosaic = False
    if 'Orthomosaic' in request_file.name:
        mosaic = True

    if 'RGB' in request_file.name:
        if mosaic is True:
            name = 'RGB_temp.TIF'
        else:
            name = 'RGB_temp.JPG'
    elif 'NIR' in request_file.name:
        name = 'NIR_temp.TIF'
    elif 'RED' in request_file.name:
        name = 'RED_temp.TIF'
    elif 'REG' in request_file.name:
        name = 'REG_temp.TIF'
    elif 'GRE' in request_file.name:
        name = 'GRE_temp.TIF'
    else:
        name = 'Other_temp.JPG'

    path = os.getcwd()
    path_folder = path + '/media/temp/bands/' + str(user) + '/'
    path_file =  path_folder + name


    ifFolder(path_folder)
    ifExist(path_file=path_file, request_file=request_file, mosaic=mosaic)


    return mosaic

def SaveDetection(request,user,profile,detection_name,status,water_stress,water_stress_percent,note_name,note_text,mosaic):
    """Save detection in DB."""
    #https://stackoverflow.com/questions/35581356/save-matplotlib-plot-image-into-django-model/35633462
    #https://stackoverflow.com/questions/3723220/how-do-you-convert-a-pil-image-to-a-django-file

    # Paths
    if mosaic is True:
        path_picture = 'media/temp/bands/'+str(request.user.username)+'/RGB_temp.JPG'
    else:
        path_picture = 'media/temp/bands/'+str(request.user.username)+'/RGB_temp.JPG'
    path_picture_ndvi ='media/temp/results/'+str(request.user.username)+'/NDVI.jpg'
    path_picture_savi ='media/temp/results/'+str(request.user.username)+'/SAVI.jpg'
    path_picture_evi2 ='media/temp/results/'+str(request.user.username)+'/EVI2.jpg'
    path_picture_without = 'media/temp/results/'+str(request.user.username)+'/WITHOUT.jpg'

    picture_name = 'RGB.jpg'
    picture_ndvi_name = 'NDVI.jpg'
    picture_savi_name = 'SAVI.jpg'
    picture_evi2_name = 'EVI2.jpg'
    picture_without_name = 'WITHOUT.jpg'

    path_pictures = [path_picture,path_picture_ndvi,path_picture_savi,path_picture_evi2,path_picture_without]
    picture_names = [picture_name,picture_ndvi_name,picture_savi_name,picture_evi2_name,picture_without_name]
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
        water_stress=water_stress,
        water_stress_percent=water_stress_percent,
        satatus_of_field=status,
        )

    detection_instance.picture.save(picture_name, picture_files[0])
    detection_instance.picture_ndvi.save(picture_ndvi_name, picture_files[1])
    detection_instance.picture_savi.save(picture_savi_name, picture_files[2])
    detection_instance.picture_evi2.save(picture_evi2_name, picture_files[3])
    detection_instance.picture_without.save(picture_without_name, picture_files[4])
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
