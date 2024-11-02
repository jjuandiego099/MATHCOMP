"""
A module to implement the stochastic gradient descent learning
algorithm for a feedforward neural network.  Gradients are calculated
using backpropagation.  Note that I have focused on making the code
simple, easily readable, and easily modifiable.  It is not optimized,
and omits many desirable features.

Font: http://neuralnetworksanddeeplearning.com/chap1.html
"""

import numpy as np
import copy
import random
from package.Singleton import Singleton

class Network(object):

    def __init__(self, sizes):
        """The list ``sizes`` contains the number of neurons in the
        respective layers of the network.  For example, if the list
        was [2, 3, 1] then it would be a three-layer network, with the
        first layer containing 2 neurons, the second layer 3 neurons,
        and the third layer 1 neuron.  The biases and weights for the
        network are initialized randomly, using a Gaussian
        distribution with mean 0, and variance 1.  Note that the first
        layer is assumed to be an input layer, and by convention we
        won't set any biases for those neurons, since biases are only
        ever used in computing the outputs from later layers."""

        # Métriques
        self.__recorregut = 0
        self.__temps = 0
        self.__velocitat = 0
        self.__vegadesC = 0
        self.__nedat = 0

        self.num_layers = len(sizes)
        self.sizes = sizes
        # Gaussiana 0-1
        self.biases = [np.random.randn(y, 1) for y in sizes[1:]]
        self.weights = [np.random.randn(y, x)
                        for x, y in zip(sizes[:-1], sizes[1:])]

    def getInfoString(self, getWeights = True):
        """
        :return: Retorna un string de la informació de la xarxa
        """
        s = "Recorregut : " + str(self.__recorregut) + "\n"
        s = s + "Temps: " + str(self.__temps) + "\n"
        s = s + "Velocitat: " + str(self.__velocitat) + "\n"
        s = s + "Nedat: " + str(self.__nedat) + "\n"

        s = s + "\nInputs: " + str(self.sizes[0]) + "\n"
        # Recorrem les hidden layers
        #   i = 1 perque ens botam els inputs
        #   len(self.sizes) - 1 perque no volem passar pels outputs
        #   1 anam incrementant i = i + 1
        for i in range(1, len(self.sizes) - 1, 1):
            s = s + "Hidden Layer " + str(i) + ", " + str(self.sizes[i]) + " neurons \n"
            if getWeights:
                for j in range(len(self.weights[i - 1])):
                    s = s + "\tWeight neuron " + str(j + 1) + ": " + str(self.weights[i - 1][j]) + "\n"

        # Output
        s = s + "Outputs: " + str(self.sizes[-1])

        return s


    def feedforward(self, a):
        """Return the output of the network if ``a`` is input."""
        for b, w in zip(self.biases, self.weights):
            a = sigmoid(np.dot(w, a) + b)
        return a


    def generaFill(self):
        """ Crea un fill """
        # "Copiar pesos a un nou objecte"
        fill = copy.deepcopy(self)
        fill.set_Recorregut(0)
        fill.set_Temps_Total(0)
        fill.set_Velocitat_Total(0)
        fill.set_Nedat_Total(0)
        fill.set_Vegades_C(0)
        fill.aplicarRenou()
        return fill

    def aplicarRenou(self):
        """
        Aplica renou a cada un dels pesos de la xarxa.
        :param tipus: Si 1: Gaussià
                      Si 2: Distribució uniforme
        """
        # Renou Gaussià
        # sigma * np.random.rand() + mu
        # sigma = 1;  mu (mitja) = 0

        config = Singleton()

        # Hidden Layers + output. Recorrem les capes
        for i in range(1, len(self.sizes) - 1, 1): # Per cada hidden layer
            for j in range(len(self.weights[i - 1])): # Per cada neurona
                for k in range(len(self.weights[i - 1][j])): # Canviam el pesos de cada una de les neurones
                    if config.renou == 1:
                        # Renou gaussià
                        self.weights[i - 1][j][k] = self.weights[i - 1][j][k] + np.random.randn()
                    else:
                        # Renou distribució uniforme
                        self.weights[i - 1][j][k] = self.weights[i - 1][j][k] + random.randint(-10, 10)


    ### Getters i setters

    def incrementaRecorregut(self):
        self.__recorregut = self.__recorregut + 1

    def decrementaRecorregut(self):
        self.__recorregut = self.__recorregut - 1

    def set_Recorregut(self, recorregut):
        self.__recorregut = recorregut

    def get_Recorregut_Total(self):
        if self.__recorregut < 0:
            return 0
        return self.__recorregut

    def get_Temps_Total(self):
        return self.__temps

    def set_Temps_Total(self, temps):
        self.__temps = temps

    def get_Velocitat_Total(self):
        if self.__velocitat < 0:
            return 0
        return self.__velocitat

    def set_Velocitat_Total(self, velocitat):
        self.__velocitat = velocitat

    def incrementaVegadesC(self):
        self.__vegadesC = self.__vegadesC + 1

    def decrementaVegadesC(self):
        self.__vegadesC = self.__vegadesC - 1

    def get_VegadesC_Total(self):
        return self.__vegadesC

    def get_Nedat_Total(self):
        if self.__nedat < 0:
            return 0
        return self.__nedat

    def set_Vegades_C(self, vegades):
        self.__vegadesC = vegades

    def set_Nedat_Total(self, nedat):
        self.__nedat = nedat

#### Miscellaneous functions
def sigmoid(z):
    """The sigmoid function."""
    # Volem valors extrems 0 o 1.
    # Per tant, els valors que son un poc mes petit de 0.5 tendeixen a 0.
    return 1.0/(1.0+np.exp(-z))

def sigmoid_prime(z):
    """Derivative of the sigmoid function."""
    return sigmoid(z)*(1-sigmoid(z))