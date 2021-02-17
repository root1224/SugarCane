"""Main apps sugarcane."""
# Models
from detections.models import Detection, Note

# Others
import os
import rasterio
from rasterio.plot import reshape_as_raster, reshape_as_image

# My apps
from .VI import Calulate_VIS, Reflectance
from .folders import ifFolder, rgb2gray
from .savefiles import SaveVI
from .Otsu import CalculateOtsu, PutMask
from .procesar import ProyectividadOpenCV


def CalculateVi(user, mosaic):
    """Calculate VIs."""
    # Paths
    path = os.getcwd()
    path_bands = path + '/media/temp/bands/' + str(user) + '/'
    path_resul = path + '/media/temp/results/' + str(user) + '/'
    ifFolder(path_resul)

    # Bands paths
    rgb_path = path_bands + 'RGB_temp.JPG'
    red_path = path_bands + 'RED_temp.TIF'
    nir_path = path_bands + 'NIR_temp.TIF'
    green_path = path_bands + 'GRE_temp.TIF'
    reg_path = path_bands + 'REG_temp.TIF'

    # Vi paths
    path_ndvi = path_resul + 'NDVI.jpg'
    path_savi = path_resul + 'SAVI.jpg'
    path_evi2 = path_resul + 'EVI2.jpg'
    path_gray = path_resul + 'EVI2_gray.jpg'
    path_without = path_resul + 'WITHOUT.jpg'

    # Bands
    sugar_procesar = ProyectividadOpenCV()
    "Se envían las URL y se obtienen los índices NDVI y una imagen adecuada para visualizar"
    if mosaic is False:
        vis = sugar_procesar.vis_calculation(red_path, nir_path,width=1280, height=960)
    else:
        vis = sugar_procesar.vis_calculation_orthomosaic(red_path, nir_path,width=1280, height=960)

    ndvi = vis['ndvi'][0]
    savi = vis['savi'][0]
    evi2 = vis['evi2'][0]

    path_vis = [path_ndvi,path_savi,path_evi2]
    vis = [ndvi,savi,evi2]

    # Export VI image
    for vi,path in zip(vis,path_vis):
        SaveVI(
            vi=vi,
            vi_path=path
        )

    # Save gray Vi
    SaveVI(
        vi=evi2,
        color_map='gray',
        vi_path=path_gray
    )

    # Make Otsu
    mask_path,th2=CalculateOtsu(
        folder=path_resul,
        file=path_gray,
    )

    PutMask(
        mask=mask_path,
        image=path_evi2,
        mask_otsu=th2,
        path_save=path_without,
    )

    state,water_stress_percent,water_stress = Reflectance(th2,green_path)

    return state,water_stress_percent,water_stress


def MakeCloustering(user,number,path_detection):
    """Make cloustering."""
    # Paths
    path = os.getcwd()
    path_clouster = path + '/media/temp/clouster/' + str(user) + '/'
    clouster_vi = path_clouster + 'clouster_done.jpg'

    picture_path = path + '/media' + path_detection

    # Values of plot_vi
    rgb2gray(picture_path,path_clouster,clouster_vi) # Img a convertir, path en donde se guarda

    vi = rasterio.open(clouster_vi).read()  # Vegetation index
    n_clouster = number       # Clouster number

    # Export VI image
    SaveVI(
        vi = reshape_as_image(vi),
        N = n_clouster,
        vi_path = clouster_vi
    )
