"""Vegetation indeces calculation."""

# Math libs
import cv2
import numpy as np

def NDVI(RED, NIR):
    """Calculate NDVI."""
    # NDVI calculation
    ndvi=np.where(
        (NIR+RED)==0,
        0,
        (NIR-RED)/(NIR+RED)  # NDVI equation
    )
    vmin, vmax = np.nanpercentile(ndvi, (1,99))  # 1-99% contrast stretch
    return ndvi

def SAVI(RED,NIR):
    """Calculate SAVI."""
    # SAVI calculaltion
    L = 0.5 # adjustment to ground
    savi=np.where(
        (NIR+RED)==0,
        0,
        ( ( (NIR-RED)/(NIR+RED+L) ) * (1+L) )  # SAVI equation
      )
    vmin, vmax = np.nanpercentile(savi, (1,99))  # 1-99% contrast stretch
    return savi

def EVI2(RED,NIR):
    """Calculate EVI2."""
    # EVI calculation
    evi2=np.where(
        (NIR+RED)==0,
        0,
        2.5*(NIR-RED)/(NIR+2.4*RED+1) # EVI2 equiation
      )
    vmin, vmax = np.nanpercentile(evi2, (1,99))  # 1-99% contrast stretch
    return evi2

def Calulate_VIS(RED,NIR):
    """Calculate vegetacion index."""

    ndvi = NDVI(RED,NIR)
    savi = SAVI(RED,NIR)
    evi2 = EVI2(RED,NIR)

    return ndvi,savi,evi2


def Reflectance(mask,green):
    width,height = mask.shape
    img = cv2.imread(green,0)
    img = cv2.resize(img, (height, width), interpolation=cv2.INTER_LINEAR)
    norm_img = np.zeros((img.shape))
    final_img = cv2.normalize(img,  norm_img, 0, 50, cv2.NORM_MINMAX)

    refl = 0
    cnt = 0
    for x in range(width):
      for y in range(height):
        if mask[x][y] != 0:
          refl += final_img[x][y]
          cnt += 1

    water_stress = ((refl/cnt)-1)
    if water_stress >= 15:
        water_stress_percent = 92.3
    elif water_stress <= 10:
        water_stress_percent = 77.7
    else:
        water_stress_percent = (water_stress*92.3)/15

    if water_stress_percent == 92.3:
        state = 'good'
    elif water_stress_percent <= 80:
        state = 'danger'
    else:
        state = 'warning'

    return state, water_stress_percent, water_stress
