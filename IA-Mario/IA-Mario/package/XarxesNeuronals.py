from package.Network import Network
from package.Singleton import Singleton
from package.FileWritter import FileWritter
from datetime import datetime
from os import mkdir
import numpy as np
import random
import pickle

class XarxesNetwork(object):

    def __init__(self, n_xarxes, inputs):
        """
        Crea n xarxes amb un nombre determinat d'inputs.
        :param n_xarxes: Nombre de xarxes
        :param inputs: Nombre d'inputs de cada xarxa.
        """

        # Per coneixer sobre quina xarxa anam
        self.xarxa_nombre_n = 0
        self.n_xarxes = n_xarxes

        self.__inputs = inputs
        self.__generacio = 0

        self.xarxes = []
        self.xarxes = self.generaNXarxesRandom(inputs, self.n_xarxes)

        # Generació de la carpeta arrel
        dateTimeObj = datetime.now()
        timestampStr = dateTimeObj.strftime("%d_%b_%Y_(%H_%M_%S)")
        self.__path_Arrel = "Experiments/"+timestampStr
        mkdir(self.__path_Arrel)

        config = Singleton()
        # Guarda la informació
        fw = FileWritter(self.__path_Arrel+"/info.txt")

        fw.writeString("Nombre de xarxes: " + str(len(self.xarxes)) + "\n")
        fw.writeString("Percentatge de fills: " + str(config.percent * 100.0) + " %\n")
        fw.writeString("Nombre de visors: " + str(config.n_visors) + "\n")
        fw.writeString("Graus de visió: " + str(config.graus) + "\n")

        if config.metrica == 1: # Temps
            fw.writeString("Métrica: Temps" + "\n")
        elif config.metrica == 2: # Espai
            fw.writeString("Métrica: Recorregut" + "\n")
        elif config.metrica == 3: # Velocitat
            fw.writeString("Métrica: Velocitat" + "\n")
        else:
            fw.writeString("Métrica: Nedat" + "\n")
        fw.close()

    def generaNXarxesRandom(self, inputs, iteracions):
        """
        Genera xarxes aleatòries (hidden layers i nombre de neurones per capa)
        """
        llista = []
        config = Singleton()
        for i in range(iteracions):
            nets = [inputs]             # Nombre d'entrades
            it = random.randint(1, 5)   # Mínim dues hidden layers i com a màxim 5
            for i in range(it):
                nets.append(random.randint(inputs, inputs * 3))

            if config.moviments == 2:
                nets.append(1)          # Una sortida
            else:
                nets.append(2)          # Dues sortides

            llista.append(Network(nets))

        return llista

    def get_xarxa(self, idx):
        """Get xarxa i-èssima."""
        try:
            return self.xarxes[idx]
        except:
            print("Error: La xarxa no existent")

    def get_n_xarxes(self):
        """Get array de xarxes. """
        return self.n_xarxes

    def getXarxaActual(self):
        """Return xarxa actual"""
        return self.xarxes[self.xarxa_nombre_n]

    def seguentXarxa(self):
        """
        Prepara el programa per executar la següent xarxa.
        :return: 'True' si encara queden xarxes
                 'False' en cas contrari
        """
        #print("La xarxa actual ha recorregut {}".format(self.xarxes[self.xarxa_nombre_n].get_Recorregut_Total()))

        self.xarxa_nombre_n = self.xarxa_nombre_n + 1
        if self.xarxa_nombre_n == self.n_xarxes:
            return False # Hem passat per totes les xarxes, per tant hem d'aturar
        return True

    def funcio_Seleccio(self):
        """
        Duu a terme el procés de generar el fills on la majoria dels pares es s'ajusten millor a la mètrica establerta.
        """
        self.guardaInformacioGenActual()
        config = Singleton()

        llista = []
        if config.metrica == 1:     # Temps
            for net in self.xarxes:
                llista.append(net.get_Temps_Total())

        elif config.metrica == 2:   # Espai
            for net in self.xarxes:
                llista.append(net.get_Recorregut_Total())

        elif config.metrica == 3:   # Velocitat
            for net in self.xarxes:
                llista.append(net.get_Velocitat_Total())
        else:                       # Nedat
            for net in self.xarxes:
                llista.append(net.get_Nedat_Total())

        llista = np.asarray(llista)
        novaLlista = []
        if np.all((llista == 0)):
            print("Cas especial")
            # Cas especial on tot són zeros
            total = len(llista)
        else:
            llista = llista / sum(llista)
            llista_acc = llista.cumsum()

            randomList = []
            for i in range(config.get_n_xarxes_a_fabricar()):
                # Generara valors entre 0 i 1
                randomList.append(random.random())

            for i in randomList:
                for j in range(len(llista_acc)):
                    if i < llista_acc[j]:
                        #print("Fill de la xarxa {}".format(j))
                        fill = self.xarxes[j].generaFill()
                        novaLlista.append(fill)
                        break

            #print("S'han de generar {} xarxes aleatòries restants".format(config.init_xarxes - len(randomList)))
            total = config.init_xarxes - len(randomList)

        novaLlista = novaLlista + self.generaNXarxesRandom(self.__inputs, total)

        #print("Tamany nova llista {}".format(len(novaLlista)))

        # Ens quedam amb la nova llista
        self.xarxes = novaLlista
        # Reiniciam el comptador
        self.xarxa_nombre_n = 0
        print("Ha acabat amb la generació {}. Passam a la següent".format(self.__generacio))
        self.__generacio = self.__generacio + 1

    def getMillorXarxaActual(self):
        """
        :return: La que es considera la millor xarxa de la generació en concret. Ho fa tenint en compte la mètrica
        utilitzada.
        """
        if len(self.xarxes) != 0:
            # Donam primer valor
            xarxa = self.xarxes[0]
            config = Singleton()

            if config.metrica == 1:  # Temps
                for net in self.xarxes:
                    if net.get_Temps_Total() > xarxa.get_Temps_Total():
                        xarxa = net
            elif config.metrica == 2:  # Espai
                for net in self.xarxes:
                    if net.get_Recorregut_Total() > xarxa.get_Recorregut_Total():
                        xarxa = net
            elif config.metrica == 3:  # Velocitat
                for net in self.xarxes:
                    if net.get_Velocitat_Total() > xarxa.get_Velocitat_Total():
                        xarxa = net
            else: # Nedat
                for net in self.xarxes:
                    if net.get_Nedat_Total() > xarxa.get_Nedat_Total():
                        xarxa = net

            return xarxa
        return None

    def guardaInformacioGenActual(self):
        """
        Guarda la informació de la considerada millor xarxa.
        """
        path = self.__path_Arrel+"/gen_"+str(self.__generacio)
        mkdir(path)

        # Guardam informació de la millor Xarxa
        fw = FileWritter(path + "/info.txt")
        net = self.getMillorXarxaActual()
        fw.writeLine(net.getInfoString())
        fw.close()

        # Guardam la millor xarxa
        with open(path+"/net.pkl", 'wb') as output: # Overwrites any existing file.
            pickle.dump(net, output, pickle.HIGHEST_PROTOCOL)

    ### Getters

    @staticmethod
    def getVelocitat(espai, temps):
        return espai/temps

    @staticmethod
    def getNedat(espai, vegadesC):
        if vegadesC == 0 or vegadesC == 1:
            return 0
        return espai/vegadesC




