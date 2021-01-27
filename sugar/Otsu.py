"""Calcule Otsu segmentation."""
# Math libs
import numpy as np
import matplotlib.pyplot as plt  # Plot images
import cv2
from PIL import Image


def CalculateOtsu(folder,file):
    # Open VI_TIFF image
    image = Image.open(file).convert('L')
    image.save(file)

    # Read VI image
    img = cv2.imread(file,cv2.IMREAD_UNCHANGED)

    # Otsu's thresholding
    ret2,th2 = cv2.threshold(img,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)

    # Save mask image
    mask = th2
    mask_path = folder+'mask.TIF'

    plt.figure(figsize=(16.92,12.72), dpi=100) #figsize=(16.92,12.72), dpi=100
    plt.imshow(mask, cmap='gray') # vmin=vminn, vmax=vmaxn
    plt.axis("off")
    plt.savefig(mask_path, dpi=100, bbox_inches='tight', pad_inches=0)
    return mask_path,th2

def PutMask(mask,image,mask_otsu,path_save):
    # Open VI color and mask
    map_traits = Image.open(image)
    mask_image = Image.open(mask).convert('L')

    mask = mask_otsu / 255
    mask = mask.astype(np.uint8)

    # Get red, blue, green
    red, green, blue = map_traits.split()

    # Bands with mask
    red_m, green_m, blue_m = [red*mask, green*mask, blue*mask]

    # Join bands
    out = Image.merge(mode='RGB', bands=(Image.fromarray(red_m), Image.fromarray(green_m), Image.fromarray(blue_m) ))
    out.save(path_save, format='JPEG')
