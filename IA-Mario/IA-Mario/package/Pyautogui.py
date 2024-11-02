import pydirectinput                # pip install pydirectinput
from pywinauto import application   # pip install pywinauto
from pywinauto.findwindows import WindowAmbiguousError, WindowNotFoundError

class Pyautogui():

    def __init__(self):
        pass

    @staticmethod
    def press(*args):
        """
        Pitja i amolla la tecla. Accepta tants d'arguments com es desitjin.
        """
        for i in args:
            pydirectinput.press(i)

    @staticmethod
    def hold(*args):
        """
        Manté apretat una tecla. Accepta tants d'arguments com es desitjin.
        """
        for i in args:
            pydirectinput.keyDown(i)

    @staticmethod
    def release(*args):
        """
        Amolla una tecla. Accepta tants d'arguments com es desitjin.
        """
        for i in args:
            pydirectinput.keyUp(i)

    @staticmethod
    def moveToGame(handle):
        '''
        Al iniciar, es col·loca a la pantalla que s'ha passat per paràmetre.
        :param handle: codi de la finestra en hexadecimal
        :return: null
        '''
        try:
            app = application.Application()
            app.connect(handle=int(handle, 16))
            app_dialog = app.top_window()
            app_dialog.set_focus()

        except(WindowNotFoundError):
            print("Window Not Found")
        except(WindowAmbiguousError):
            print("Too many Windows Found")
