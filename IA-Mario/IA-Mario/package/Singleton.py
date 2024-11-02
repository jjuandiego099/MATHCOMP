"""
Singleton.py
~~~~~~~~~~
Patró Singleton. Ens permet emmagatzemar atributs constants. Pel nostre problema, hi guardam tot allò
parametrizable, és a dir, tot allò que pot variar entre un experiment i un altre. Com per exemple: nombre de xarxes,
nombre de fills per a cada xarxa, etc.
"""

import math

class Singleton:

    __INSTANCE = None

    class __Data:
        def __init__(self):
            # Atributs relacionats amb la vista del nostre agent
            self.n_visors = 4
            self.graus = 180 # 360º (default)

            ## Metriques:
            #   - Temps: 1
            #   - Espai: 2
            #   - Velocitat: 3
            #   - Nedat: 4 (default)
            self.metrica = 4

            # % de fills nous. Valor entre [0-1]
            # 1 Significarà que la a la pròxima generació
            # un 100% seran fills i, per tant, no hi haurà
            # xarxes aleatòries noves.
            self.percent = 0.9 # x 100 (%)

            self.__init_xarxes = 50

            ## Possibles moviments:
            #   - 2
            #   - 4 (default)
            self.moviments = 2

            ## Possibles renous:
            #   - Gaussià: 1
            #   - Uniforme: 2 (default)
            self.renou = 2

        def get_n_xarxes_a_fabricar(self):
            """
            Aquest mètode retorna el nombre de fills nous que s'han de generar
            tenint en compte el percentatge de noves xarxes aleatòries que s'han de generar.
            :return: Total de xarxes que ha de fabricar.
            """

            # Arrodonim cap abaix
            return math.floor(self.__init_xarxes * self.percent)


        ### Getter i setter
        @property
        def init_xarxes(self):
            # Getter
            return self.__init_xarxes

        @init_xarxes.setter
        def set_n_xarxes(self, val):
            # Setter
            self.__init_xarxes = val

    def __new__(cls, *args, **kwargs):
        if cls.__INSTANCE is None:
            cls.__INSTANCE = cls.__Data()
        return cls.__INSTANCE
