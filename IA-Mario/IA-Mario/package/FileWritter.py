import os

class FileWritter(object):

    def __init__(self, path):
        self.file = open(path, "w", encoding='utf8')

    def writeString(self, string):
        """
        Escriu un string dins el fitxer carregat.
        :param string: String que es vol escriure
        """
        self.file.write(string)

    def writeLine(self, string):
        """
        Escriu una línia dins el fitxer carregat. Fa un salt de línia.
        :param string: String que es vol escriure
        """
        self.file.write(string + os.linesep)

    def close(self):
        """
        Tanca fitxer.
        """
        self.file.close()