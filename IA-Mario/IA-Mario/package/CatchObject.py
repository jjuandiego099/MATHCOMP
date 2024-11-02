import cv2 as cv
import numpy as np
from package.Rectangle import Rectangle

class CatchObject:

     def __init__(self, color_bgr, name, needle_img_path, scale_percent):
         self.line_color = color_bgr
         self.name = name
         self.method = cv.TM_CCOEFF_NORMED
         #self.method = cv.TM_SQDIFF_NORMED
         self.needle_img = cv.imread(needle_img_path, cv.IMREAD_COLOR)
         self.needle_w = self.needle_img.shape[1]  # Collim width
         self.needle_h = self.needle_img.shape[0]  # Collim heigth

         self.scale_percent = scale_percent  # %
         self.needle_width_resized = int(self.needle_img.shape[1] * self.scale_percent / 100)
         self.needle_height_resized = int(self.needle_img.shape[0] * self.scale_percent / 100)
         self.dim = (self.needle_width_resized, self.needle_height_resized)
         self.need_img_resized = cv.resize(self.needle_img, self.dim, interpolation=cv.INTER_AREA)

     def findPosition(self, haystack_img, threshold=0.5):
        """
        Donada una imatge, retorna les posicions de l'objecte.
        :param haystack_img: Imatge on es vol cercar
        :param threshold: Percentatge acceptat
        :return: Llista de objecte Rectangle.
        """

        # Si la imatge on volem cercar l'objecte és més petita que la del propi objecte. Retornam directament.
        if haystack_img.shape[0] <= self.needle_w or haystack_img.shape[1] <= self.needle_h:
            return []

        result = cv.matchTemplate(haystack_img, self.needle_img, self.method)

        locations = np.where(result >= threshold)
        #locations = np.where(result <= threshold)

        locations = list(zip(*locations[::-1])) # list(): convert an iterator to list
                                                # zip():  returns an iterator of tuples based on the iterable objects.
                                                # The * operator can be used in conjunction with zip() to unzip the list
                                                # [::-1]: Sintaxis iterable[inicio:fin:paso] Devuelve una lista al revés


        # Cream la llista dels rectangles [pos_x, pos_y, width, height]
        rectangles = []
        for loc in locations:
            rect = [int(loc[0]), int (loc[1]), self.needle_w, self.needle_h]
            rectangles.append(rect)

        # Agrupam els rectangles en un. Ja que un mateix objecte pot estar més d'una vegada rectangulat.
        rectangles, weights = cv.groupRectangles(rectangles, groupThreshold=1,
                                                 eps=0.5)   # El darrer paràmetre ens diu com de aprop estan els
                                                            # rectangles que volem agrupar

        if len(rectangles) > 10:
            rectangles = rectangles[:10]

        rectangle_object = []
        for (x, y, w, h) in rectangles:
            rectangle_object.append(Rectangle(x, y, w, h, self.line_color, self.name))

        return rectangle_object

     def findPosition_reduce(self, haystack_img, threshold=0.5):
         """
         Donada una imatge, retorna les posicions de l'objecte. Internament duu a terme una reducció de la imatge
         de cerca per tal d'aconseguir major rendiment de l'algoritme.
         :param haystack_img: Imatge on es vol cercar
         :param threshold: Percentatge acceptat
         :return: Llista de objecte Rectangle.
         """
         haystack_width = haystack_img.shape[1] * self.scale_percent / 100
         haystack_height = haystack_img.shape[0] * self.scale_percent / 100
         haystack_dim = (int(haystack_width), int(haystack_height))

         # Redimensionam la imatge
         haystack_resized = cv.resize(haystack_img, haystack_dim, interpolation=cv.INTER_AREA)

         # Si la imatge on volem cercar l'objecte és més petita que la del propi objecte. Retornam directament
         if haystack_width <= self.needle_width_resized or haystack_height <= self.needle_height_resized:
             return []

         result = cv.matchTemplate(haystack_resized, self.need_img_resized, self.method)

         locations = np.where(result >= threshold)
         locations = list(zip(*locations[::-1]))

         # Cream la llista dels rectangles [pos_x, pos_y, width, height]
         rectangles = []
         for loc in locations:
             rect = [int(loc[0])+1, int(loc[1])+1, self.needle_width_resized, self.needle_height_resized]
             rectangles.append(rect)

         # Agrupam els rectangles en un. Ja que un mateix objecte pot estar més d'una vegada rectangulat.
         rectangles, weights = cv.groupRectangles(rectangles, groupThreshold=1,
                                                  eps=0.5)  # El darrer paràmetre ens diu com de aprop estan
                                                            # els rectangles

         if len(rectangles) > 10:
             rectangles = rectangles[:10]

         rectangle_object = []
         for (x, y, w, h) in rectangles:
             rectangle_object.append(Rectangle(int(x * (1/(self.scale_percent/100))),
                                               int(y * (1/(self.scale_percent/100))),
                                               int(w * (1/(self.scale_percent/100))),
                                               int(h * (1/(self.scale_percent/100))), self.line_color, self.name))

         return rectangle_object

