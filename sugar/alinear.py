import cv2
from .procesar import ProyectividadOpenCV

def merge(rgb, gre, nir, red, reg, path, width = 1280, height = 960):
    img_RGB = cv2.imread(rgb, 0)
    img_GRE = cv2.imread(gre, 0)
    img_NIR = cv2.imread(nir, 0)
    img_RED = cv2.imread(red, 0)
    img_REG = cv2.imread(red, 0)

    sugar_merge = ProyectividadOpenCV()

    stb_RGB, stb_GRE, stb_NIR, stb_RED, stb_REG = sugar_merge.img_alignment_sequoia(img_RGB, img_GRE, img_NIR, img_RED, img_REG, width, height)

    merged_fix_stb = cv2.merge((stb_REG, stb_GRE, stb_RED, stb_NIR))

    cv2.imwrite(path, merged_fix_stb)
