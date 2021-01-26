"""Vegetation indeces calculation."""

# Math libs
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
