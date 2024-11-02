import cv2 as cv
import numpy as np

class Rectangle:

    def __init__(self, center_x, center_y, width, height, line_color=(0, 255, 0), name=''):
        self.pos_x = center_x
        self.pos_y = center_y
        self.width = width
        self.height = height
        self.line_color = line_color
        self.name = name

        self.top_left = (self.pos_x, self.pos_y)
        self.bottom_right = (self.pos_x + self.width, self.pos_y + self.height)
        self.top_left_ten = (self.pos_x, self.pos_y - 10)

    def printRectangle(self, haystack_img, show_name=False):
        """
        Donada una imatge, pinta el rectangle sobre ella.
        :param haystack_img: Imatge sobre la qual es pintarà el rectangle
        :param show_name: Si 'True' pinta el nom de l'objecte en concret
                         'False' cas contrari.
        """
        cv.rectangle(haystack_img, self.top_left, self.bottom_right, self.line_color, -1)  # line_type
        if show_name:
            cv.putText(haystack_img, self.name, self.top_left_ten, cv.FONT_ITALIC, 0.9, self.line_color, 1)

        return haystack_img

    def printCrossHair(self, haystack_img):
        """
        Donada una imatge, en lloc de pintar el rectangle, ho pinta en forma de creu.
        :param haystack_img: Imatge sobre la qual es pintarà la creu.
        """
        center_x, center_y = self.rectangleToPoint()
        cv.drawMarker(haystack_img, (center_x, center_y), self.line_color, 1)
        return haystack_img

    def canviaCentre(self, center_x, center_y):
        """
        Modifica el centre del rectangle. Manté les dimensions originals.
        """
        self.pos_x = center_x - int(self.width / 2)
        self.pos_y = center_y - int(self.height / 2)
        self.top_left = (self.pos_x, self.pos_y)
        self.bottom_right = (self.pos_x + self.width, self.pos_y + self.height)
        self.top_left_ten = (self.pos_x, self.pos_y - 10)


    def rectangleToPoint(self):
        """
        Transforma les coordenades del rectangle a un punt.
        :return: Valor 'x' i 'y'
        """
        # Càlcul del centre del rectangle
        center_x = self.pos_x + int(self.width/2)
        center_y = self.pos_y + int(self.height/2)
        # Retornam el punt
        return center_x, center_y

    def returnInfo(self):
        """
        :return: posició 'x', posició 'y' i amplada i altura del rectangle.
        """
        return self.pos_x, self.pos_y, self.width, self.height

    def returnPoints(self):
        """
        :return: Numpy array de la posició 'x' i 'y' del rectangle.
        """
        return np.array((self.pos_x, self.pos_y))