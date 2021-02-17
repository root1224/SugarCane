import cv2
import numpy as np
import rasterio

class ProyectividadOpenCV():
    """
    Esta es una clase para solucionar problemas con homografias
    """
    # Atributos de la clase
    error_reproyeccion = 4

    # --------------------------------------------------------------------------
    def __init__(self):
        """Inicializador del objeto miembro de la clase"""
    # --------------------------------------------------------------------------
    def estabilizador_imagen(self, imagen_base, imagen_a_estabilizar, radio=0.75, error_reproyeccion=4.0,
                             coincidencias=False):
        """Esta clase devuelve una secuencia de imágenes tomadas de la cámara estabilizada con respecto a la primera imagen"""

        # Se obtienen los puntos deinterés

        (kpsBase, featuresBase) = self.obtener_puntos_interes(imagen_base)
        (kpsAdicional, featuresAdicional) = self.obtener_puntos_interes(imagen_a_estabilizar)
        # Se buscan las coincidencias

        M = self.encontrar_coincidencias(imagen_base, imagen_a_estabilizar, kpsBase, kpsAdicional, featuresBase,
                                         featuresAdicional, radio)

        if M is None:
            print("pocas coincidencias")
            return None

        if len(M) > 4:
            # construct the two sets of points

            #            M2 = cv2.getPerspectiveTransform(ptsA,ptsB)
            (H, status) = self.encontrar_H_RANSAC_Estable(M, kpsBase, kpsAdicional, error_reproyeccion)
            estabilizada = cv2.warpPerspective(imagen_base, H, (imagen_base.shape[1], imagen_base.shape[0]))
            return estabilizada
        print("sin coincidencias")
        return None

    def img_alignment_sequoia(self, img_RGB, img_GRE, img_base_NIR, img_RED, img_REG, width, height):
        """This class takes the five images given by Sequoia Camera and makes a photogrammetric
        alignment. Returns four images (GRE, NIR, RED, REG) aligned with the RGB image"""

        # Se valida que si estén todas las variables en el argumento

        # width, height = img_SIZE

        # Se redimencionan todas las imagenes al mismo tamaño especificado en image_SIZE

        b_RGB = cv2.resize(img_RGB, (width, height), interpolation=cv2.INTER_LINEAR)
        b_GRE = cv2.resize(img_GRE, (width, height), interpolation=cv2.INTER_LINEAR)
        base_NIR = cv2.resize(img_base_NIR, (width, height), interpolation=cv2.INTER_LINEAR)
        b_RED = cv2.resize(img_RED, (width, height), interpolation=cv2.INTER_LINEAR)
        b_REG = cv2.resize(img_REG, (width, height), interpolation=cv2.INTER_LINEAR)

        # Se estabilizan todas las imágenes con respecto a la imagen base

        stb_GRE = self.estabilizador_imagen(b_GRE, base_NIR)
        stb_RGB = self.estabilizador_imagen(b_RGB, base_NIR)
        stb_RED = self.estabilizador_imagen(b_RED, base_NIR)
        stb_REG = self.estabilizador_imagen(b_REG, base_NIR)

        return stb_RGB, stb_GRE, base_NIR, stb_RED, stb_REG

    # --------------------------------------------------------------------------
    def obtener_puntos_interes(self, imagen):
        """Se obtienen los puntos de interes cn SIFT"""

        descriptor = cv2.xfeatures2d.SIFT_create()
        (kps, features) = descriptor.detectAndCompute(imagen, None)

        return kps, features

    # --------------------------------------------------------------------------
    def encontrar_coincidencias(self, img1, img2, kpsA, kpsB, featuresA, featuresB, ratio):
        """Metodo para estimar la homografia"""

        matcher = cv2.DescriptorMatcher_create("BruteForce")
        rawMatches = matcher.knnMatch(featuresA, featuresB, 2)
        matches = []
        #
        #        # loop over the raw matches
        for m in rawMatches:
            #            # ensure the distance is within a certain ratio of each
            #            # other (i.e. Lowe's ratio test)
            if len(m) == 2 and m[0].distance < m[1].distance * ratio:
                matches.append((m[0].trainIdx, m[0].queryIdx))

        #        print (matches)
        return matches

    # --------------------------------------------------------------------------
    def encontrar_H_RANSAC(self, matches, kpsA, kpsB, reprojThresh):
        """Metodo para aplicar una H a una imagen y obtener la proyectividad"""

        if len(matches) > 4:
            # construct the two sets of points
            ptsA = np.float32([kpsA[i].pt for (_, i) in matches])
            ptsB = np.float32([kpsB[i].pt for (i, _) in matches])

            # compute the homography between the two sets of points
            (H, status) = cv2.findHomography(ptsA, ptsB, cv2.RANSAC, reprojThresh)

            # return the matches along with the homograpy matrix
            # and status of each matched point
            return (H, status)

        # otherwise, no homograpy could be computed
        return None

    # --------------------------------------------------------------------------
    def encontrar_H_RANSAC_Estable(self, matches, kpsA, kpsB, reprojThresh):
        """Metodo para aplicar una H a una imagen y obtener la proyectividad"""

        if len(matches) > 4:
            # construct the two sets of points
            ptsA = np.float32([kpsA[i].pt for (_, i) in matches])
            ptsB = np.float32([kpsB[i].pt for (i, _) in matches])

            # compute the homography between the two sets of points
            (H, status) = cv2.findHomography(ptsA, ptsB, cv2.RANSAC, reprojThresh)

            return (H, status)

        return None

    # --------------------------
    def vis_calculation(self, url_img_RED="ejemplos/example_2/img_RED.TIF",
                         url_img_NIR="ejemplos/example_2/img_NIR.TIF", width=1280, height=960, L=0.5):
        "En esta clase se calcula el índice NDVI a partir de un par de imágenes entregadas en el argumento"

        "Se leen las imágenes"
        img_RED = cv2.imread(url_img_RED, 0)
        stb_NIR = cv2.imread(url_img_NIR, 0)

        img_RED = cv2.resize(img_RED, (width, height), interpolation=cv2.INTER_LINEAR)
        stb_NIR = cv2.resize(stb_NIR, (width, height), interpolation=cv2.INTER_LINEAR)

        "Se alinean as imágenes y se utiliza la imagen roja como imagen base"

        stb_RED = self.estabilizador_imagen(img_RED, stb_NIR)

        "Se convierten las imágenes en arreglos trabajables con numpy y matplotlib"
        red = np.array(stb_RED, dtype=float)
        nir = np.array(stb_NIR, dtype=float)

        "Se verifican y corrigen las divisiones por cero"
        check = np.logical_and(red > 1, nir > 1)

        "Se calcula el índice ndvi"
        ndvi = np.where(check, (nir - red) / (nir + red), 0)
        ndvi_index = ndvi

        "Se calcula el índice savi"
        savi = np.where(check, ((nir - red) / (nir + red + L) * (1+L) ), 0)
        savi_index = savi

        "Se calcula el índice evi2"
        evi2 = np.where(check, 2.5*(nir - red) / (nir + 2.4 * red + 1), 0)
        evi2_index = evi2

        "Se verifica que todos los valores queden sobre cero de NDVI"
        if ndvi.min() < 0:
            ndvi = ndvi + (ndvi.min() * -1)
        ndvi = (ndvi * 255) / ndvi.max()
        ndvi = ndvi.round()
        ndvi_image = np.array(ndvi, dtype=np.uint8)

        "Se verifica que todos los valores queden sobre cero de SAVI"
        if savi.min() < 0:
            savi = savi + (savi.min() * -1)
        savi = (savi * 255) / savi.max()
        savi = savi.round()
        savi_image = np.array(savi, dtype=np.uint8)

        "Se verifica que todos los valores queden sobre cero de EVI2"
        if evi2.min() < 0:
            evi2 = evi2 + (evi2.min() * -1)
        evi2 = (evi2 * 255) / evi2.max()
        evi2 = evi2.round()
        evi2_image = np.array(evi2, dtype=np.uint8)

        vis = {
            'ndvi' : [ndvi_index, ndvi_image],
            'savi' : [savi_index, savi_image],
            'evi2' : [evi2_index, evi2_image]
          }

        return vis

        # --------------------------
    def vis_calculation_orthomosaic(self, url_img_RED="ejemplos/example_2/img_RED.TIF",
                         url_img_NIR="ejemplos/example_2/img_NIR.TIF", width=725, height=1081, L=0.5):
        "En esta clase se calcula el índice NDVI a partir de un par de imágenes entregadas en el argumento"

        "Se leen las imágenes"
        img_RED = rasterio.open(url_img_RED).read(1)
        img_NIR = rasterio.open(url_img_NIR).read(1)


        img_RED = cv2.resize(img_RED, (width, height), interpolation=cv2.INTER_LINEAR)
        img_NIR = cv2.resize(img_NIR, (width, height), interpolation=cv2.INTER_LINEAR)

        "Se alinean as imágenes y se utiliza la imagen roja como imagen base"

        #stb_RED = self.estabilizador_imagen(img_RED, img_NIR)

        "Se convierten las imágenes en arreglos trabajables con numpy y matplotlib"
        red = np.array(img_RED, dtype=float)
        nir = np.array(img_NIR, dtype=float)

        "Se verifican y corrigen las divisiones por cero"
        check = np.logical_and(red > 1, nir > 1)

        "Se calcula el índice ndvi"
        ndvi = np.where(check, (nir - red) / (nir + red), 0)
        ndvi_index = ndvi

        "Se calcula el índice savi"
        savi = np.where(check, ((nir - red) / (nir + red + L) * (1+L) ), 0)
        savi_index = savi

        "Se calcula el índice evi2"
        evi2 = np.where(check, 2.5*(nir - red) / (nir + 2.4 * red + 1), 0)
        evi2_index = evi2

        "Se verifica que todos los valores queden sobre cero de NDVI"
        if ndvi.min() < 0:
            ndvi = ndvi + (ndvi.min() * -1)
        ndvi = (ndvi * 255) / ndvi.max()
        ndvi = ndvi.round()
        ndvi_image = np.array(ndvi, dtype=np.uint8)

        "Se verifica que todos los valores queden sobre cero de SAVI"
        if savi.min() < 0:
            savi = savi + (savi.min() * -1)
        savi = (savi * 255) / savi.max()
        savi = savi.round()
        savi_image = np.array(savi, dtype=np.uint8)

        "Se verifica que todos los valores queden sobre cero de EVI2"
        if evi2.min() < 0:
            evi2 = evi2 + (evi2.min() * -1)
        evi2 = (evi2 * 255) / evi2.max()
        evi2 = evi2.round()
        evi2_image = np.array(evi2, dtype=np.uint8)

        vis = {
            'ndvi' : [ndvi_index, ndvi_image],
            'savi' : [savi_index, savi_image],
            'evi2' : [evi2_index, evi2_image]
          }

        return vis
