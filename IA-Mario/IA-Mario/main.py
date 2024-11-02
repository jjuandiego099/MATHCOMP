import cv2 as cv    # opencv
import numpy as np  # numpy
from time import time
import math
from tkinter import *
from package.WindowCapture import WindowCapture
from package.CatchObject import CatchObject
from multiprocessing import Process, Queue
from package.XarxesNeuronals import XarxesNetwork
from package.Pyautogui import Pyautogui
from package.KeyBoardInput import KeyBoardInput
from package.Singleton import Singleton

######################################################################
# Per a la IA es fan les següents suposicions:
# - En Mario mai s'acotarà
# - Les monedes no són importants (ni les petites ni les gegants)
# - En Mario mai tornarà gran
# - En Mario mai entrarà dins tubs
######################################################################

#### Variables

# Colors de la simplificació de les imatges
colorMario = [0, 255, 0]
colorEnemics = [0, 0, 255]
colorObstacle = [33, 33, 33]

config = Singleton()
on = True

printLoop = False

teclaReinici = 'F1' # Modificar-ho en el cas d'utilitzar un altra 'slot' dins l'emulador

# Es el temps màxim que pot estar una IA viva
temps_max = 300 # Segons

def selectROI(img, x, y, dx, dy):
    """
    Donada una  imatge crea una subimatge de la mateixa
    :param img: Imatge que es vol retallar
    :param x: Posició x (Centre del ROI)
    :param y: Posició y (Centre del ROI)
    :param dx: Desplaçament x respecte param x
    :param dy: Desplaçament y respecte param y
    :return: La imatge retallada
    """
    width = img.shape[1]
    height = img.shape[0]

    # Si la x o y és més gran que el propi width o height de la imatge o la x o la y tenen valor negatiu
    # Llavors retornam la imatge fora retallar.
    if width < x or x < 0 or height < y or y < 0:
         return img

    first_row = x - dx
    last_row = x + dx

    first_column = y - dy
    last_column = y + dy

    # Es fa la comprovació de que no ens hem sortit de la imatge principal
    if first_row < 0:
        first_row = 0

    if img.shape[1] < last_row: # Width
        last_row = img.shape[1]

    if first_column < 0:
        first_column = 0

    if img.shape[0] < last_column: # Height
        last_column = img.shape[0]

    return img[first_column:last_column, first_row:last_row]

def trobaObj(queue_in, queue_response):
    """
    Donada la coa d'entrada, cerca els objectes dins la imatge. A la coa de sortida s'hi guardaràn els distints punts
    que s'han trobat. En cas de no haver trobat cap punt, aquest serà array buid.

    Format dels objectes de la coa queue_in: [plantilla (que es vol capturar), imatge (on es vol cercar), umbral]
    El procés acaba quan reb un array buid.
    :param queue_in: Coa d'entrada
    :param queue_response: Coa de sortida o de resposta
    """
    array = queue_in.get() # Bloquetja
    while len(array) > 0:
        obj = array[0]
        screenshot = array[1]
        threshold = array[2]
        queue_response.put(obj.findPosition_reduce(screenshot, threshold))
        array = queue_in.get()

def ferMoviment(queue_in, queue_out):
    """
    Donada la coa d'entrada, aplica els moviments respectius. Amb la coa de sortida donam pas al programa principal per
    continuar les seues tasques.

    Format dels objectes de la coa queue_in: [inputs*]
    El procés acaba quan reb un array buid.
    :param queue_in: Coa d'entrada
    :param queue_response: Coa de sortida o de resposta
    """
    output = queue_in.get() # Bloquetja
    while len(output) > 0:
        if config.moviments == 2:
            if output[0] == 0:
                KeyBoardInput.press('d')
            else:
                KeyBoardInput.press('c')
        else:
            a = output[0]
            b = output[1]

            if a == 0 and b == 0:
                pass
            elif a == 0 and b == 1:
                KeyBoardInput.press('c')
            elif a == 1 and b == 0:
                KeyBoardInput.press('a')
            else:
                KeyBoardInput.press('d')

        '''
            # Alternativa dels 4 moviments
        
            if a == 0 and b == 0:
                KeyBoardInput.press('d')
            elif a == 0 and b == 1:
                KeyBoardInput.press('a')
            elif a == 1 and b == 0:
                KeyBoardInput.pressAndHold('d')
                KeyBoardInput.press('c')
            else:
                KeyBoardInput.pressAndHold('a')
                KeyBoardInput.press('c')
    
            KeyBoardInput.release('d', 'a')
        '''

        queue_out.put("OK")
        output = queue_in.get()

def filtraColors(captura):
    """
    Filtratge pel nivell en concret: "Super Mario World - Donut Secret 1"
    :param captura: imatge la qual es vol fer el filtratge
    :return: mascara
    """
    # Conversió a HSV
    hsv = cv.cvtColor(captura, cv.COLOR_BGR2HSV)
    kernel5 = np.ones((5, 5), np.uint8)

    # Color pareds
    mask = cv.inRange(hsv, (40, 0, 10), (100, 60, 179))
    erosion = cv.erode(mask, kernel5, iterations=1)
    final_mask = cv.dilate(erosion, kernel5, iterations=2)

    '''
    # Tub blau
    mask = cv.inRange(hsv, (110, 0, 0), (121, 127, 255))
    erosion = cv.erode(mask, kernel, iterations=4)
    mask2 = cv.dilate(erosion, kernel, iterations=4)
    final_mask = cv.bitwise_or(mask1, mask2)
    '''

    '''
    #Tub taronja
    mask = cv.inRange(hsv, (10, 49, 9), (77, 255, 255))
    erosion = cv.erode(mask, kernel, iterations=3)
    dilation = cv.dilate(erosion, kernel, iterations=6)
    kernel = np.ones((8, 8), np.uint8)
    closing = cv.morphologyEx(dilation, cv.MORPH_CLOSE, kernel)
    final_mask = cv.bitwise_or(final_mask, closing)
    '''

    '''
    # Blocs ? - Groc
    kernel = np.ones((4, 7), np.uint8)
    mask = cv.inRange(hsv, (15, 69, 255), (179, 230, 255))
    erosion = cv.erode(mask, kernel, iterations=1)
    kernel = np.ones((13, 33), np.uint8)
    dilation = cv.dilate(erosion, kernel, iterations=2)
    final_mask = cv.bitwise_or(final_mask, dilation)
    '''

    # Bloc ? - Marró
    kernel10 = np.ones((10, 10), np.uint8)
    mask = cv.inRange(hsv, (13, 116, 69), (36, 233, 247))
    erosion = cv.erode(mask, kernel10, iterations=1)
    dilation = cv.dilate(erosion, kernel10, iterations=2)
    final_mask = cv.bitwise_or(final_mask, dilation)

    return final_mask

def haMortMario(img):
    """
    :return: 'True' si en mario ha mort. Es coneix el valor ja que la pantalla es torna color obscura.
    'False' en cas contrari.
    """
    return not np.any(img)

def doLine(img, n_linies, pos_x, pos_y, grau):
    """
    Donat un punt, crea els visors.
        Si visor = 0: No obstacle
        Si visor = 1: Obstacle
        Si visor = 2: Enemic
    :param img: Imatge principal
    :param n_linies: Nombre de visors
    :param pos_x: Punt de on començaran les linies
    :param pos_y: Punt de on començaran les linies
    :param grau: Grau total
    :return: Array amb els valors dels visors
    """
    if grau > 360:
        grau = 360

    if grau == 360:
        n_sectors = n_linies
    else:
        # Per exemple: Si volem 3 linies, tindrem 4 sectors
        n_sectors = n_linies + 1

    # Inicialització de l'array
    obstacles = [0 for i in range(n_linies)]

    # Passam a Radians
    angle = math.radians(grau/n_sectors)
    alpha = angle - math.pi/2

    y0 = pos_y

    for j in range(n_linies):
        # Càlcul de la pendent
        # Si la pendent es negativa significa que estic o bé dins el segon o el quart quadrant
        m = math.tan(alpha)

        i = 0
        while True:
            # 90º o 270º (Verticals)
            if m > 100000 or m < -100000:
                # 90º
                if math.sin(alpha) > 0:
                    y = pos_y + i
                # 270º
                else:
                    y = pos_y - i

                x = pos_x
            else:
                # Quadrant positiu
                if math.cos(alpha) > 0:
                    y = int(m * i + y0)
                    x = pos_x + i
                # Quadrant negatiu
                else:
                    y = int(-m * i + y0)
                    x = pos_x - i

            # Si ens hem sortit de la imatge
            if y < 0 or y >= img.shape[0] or x < 0 or x >= img.shape[1]:
                break

            if np.any(img[y][x] != colorMario) and np.any(img[y][x] != (255, 255, 255)):
                # Significa que hi ha algun obstacle
                if np.any(img[y][x]):
                    # Si es un enemic
                    if np.any(img[y][x] == colorEnemics):
                        obstacles[j] = 2
                    else:
                        obstacles[j] = 1
                    break

            # Pintam les linies
            #img[y][x] = 255, 255, 255

            i = i + 1

        alpha = alpha + angle

    return obstacles

def offTheProgram():
    """
    Atura el bucle intern del programa una vegada es crida.
    """
    global on
    on = False

def main():
    """
    Execució principal
    """
    # Alerta! La pantalla que es vol capturar no pot estar minimitzada al iniciar l'execució
    window_name = 'Snes9X v1.53 for Windows'
    border_pixels = 400
    titlebar_pixels = 218
    downbar_pixels = 40

    try:
        wincap = WindowCapture(window_name, border_pixels, titlebar_pixels, downbar_pixels)
        captura = wincap.get_screenshot()  # Dona un primer valor
    except:
        print(sys.exc_info()[1])
        print("Finestra minimitzado o no existeix")
        sys.exit()

    hdl = WindowCapture.getHwnd(window_name)
    if len(hdl) != 0 or len(hdl) > 1:
        Pyautogui.moveToGame(hex(hdl[0]))
    else:
        print("Finestra no trobada o s'han trobat més d'un element")
        sys.exit()

    root = Tk()
    root.config(bd=15)

    Label(root, text="Per aturar el programa prem el botó").pack()
    Button(root, text="Off", command=offTheProgram).pack()

    # + 2 perque serà la posició (x,y) den Mario
    network = XarxesNetwork(config.init_xarxes, config.n_visors + 2)

    sub_img = captura                   # Dona un primer valor

    # Inicialització del temps pel càlcul dels FPS
    if printLoop:
        loop_time = time()

    # Objectes que es volen capturar
    n_processos_mario = 2
    mario = CatchObject(colorMario, 'Mario', 'images/mario_positions/mario8.png', 50)
    mario2 = CatchObject(colorMario, 'Mario', 'images/mario_positions/mario_reverse.png', 50)

    n_processos_enemics = 8
    enemic = CatchObject(colorEnemics, 'Enemic', 'images/enemics/enemic_1.png', 15)
    enemic_reverse = CatchObject(colorEnemics, 'Enemic', 'images/enemics/enemic_1_reverse.png', 15)
    enemic2 = CatchObject(colorEnemics, 'Enemic', 'images/enemics/enemic_2.png', 15)
    enemic2_reverse = CatchObject(colorEnemics, 'Enemic', 'images/enemics/enemic_2_reverse.png', 15)
    enemic3 = CatchObject(colorEnemics, 'Enemic', 'images/enemics/enemic_3.png', 20)
    enemic4 = CatchObject(colorEnemics, 'Enemic', 'images/enemics/enemic_4.png', 20)
    enemic5 = CatchObject(colorEnemics, 'Enemic', 'images/enemics/enemic_5.png', 20)
    enemic6 = CatchObject(colorEnemics, 'Enemic', 'images/enemics/enemic_5_reverse.png', 20)

    # Coes de processos
    queue_mario_in = Queue()
    queue_mario_out = Queue()

    queue_enemies_in = Queue()
    queue_enemies_out = Queue()

    # Processos den Mario
    for i in range(n_processos_mario):
        p = Process(target=trobaObj, args=(queue_mario_in, queue_mario_out))
        p.start()

    # Processos dels enemics
    for i in range(n_processos_enemics):
        p = Process(target=trobaObj, args=(queue_enemies_in, queue_enemies_out))
        p.start()

    queue_doMoves = Queue()
    queue_doMoves_out = Queue()
    queue_doMoves_out.put("OK") # Per a que al començament no es quedi bloquejat el nostre fil principal
    Process(target=ferMoviment, args=(queue_doMoves,queue_doMoves_out)).start()

    # Posició anterior den Mario
    # (Valors predeterminats)
    punt_x_anterior = -1
    punt_y_anterior = -1

    offset = 90         # Desplaçament per crear el ROI
    offsetXtra = 80     # En el cas d'haver perdut en Mario, s'usa un desplaçament extra per crear un ROI més gran

    trobat_anteriorment = False
    mario_no_vist = 0   # Comptador dels Frames el qual no s'ha trobat en Mario

    start_time = time()
    next = False

    while on:
        #print("Estic a la xarxa nombre {}".format(network.getXarxaActual()))
        captura = wincap.get_screenshot()

        #print("Temps del bucle {} s".format(time() - start_time))
        if haMortMario(captura) or next or (time() - start_time) > temps_max:
            # Actualitzam informació
            network.getXarxaActual().set_Temps_Total(time() - start_time)
            network.getXarxaActual().set_Velocitat_Total(XarxesNetwork.getVelocitat(network.getXarxaActual().get_Recorregut_Total()
                                                                            ,network.getXarxaActual().get_Temps_Total()))
            network.getXarxaActual().set_Nedat_Total(XarxesNetwork.getNedat(network.getXarxaActual().get_Recorregut_Total()
                                                                            ,network.getXarxaActual().get_VegadesC_Total()))

            next = False
            # Si no queden xarxes
            if not(network.seguentXarxa()):
                network.funcio_Seleccio()

            # Reiniciam el temps
            start_time = time()
            KeyBoardInput.press(teclaReinici)
            KeyBoardInput.release('d', 'a')

        # Inserim els objectes que volem capturar
        queue_mario_in.put([mario, sub_img, 0.4])
        queue_mario_in.put([mario2, sub_img, 0.45])

        queue_enemies_in.put([enemic, captura, 0.55])
        queue_enemies_in.put([enemic_reverse, captura, 0.55])
        queue_enemies_in.put([enemic2, captura, 0.5])
        queue_enemies_in.put([enemic2_reverse, captura, 0.5])
        queue_enemies_in.put([enemic3, captura, 0.5])
        queue_enemies_in.put([enemic4, captura, 0.5])
        queue_enemies_in.put([enemic5, captura, 0.5])
        queue_enemies_in.put([enemic6, captura, 0.5])

        final_mask = filtraColors(captura)

        # Es fa una copia de la captura
        target = captura.copy()
        target[final_mask == 0] = 0                 # Pintam el fons
        target[final_mask == 255] = colorObstacle   # Pintam les pareds

        # Agafam els punts dels enemics
        rectangles_enemies = queue_enemies_out.get()
        for i in range(n_processos_enemics-1):
            rectangles_enemies = np.concatenate((rectangles_enemies, queue_enemies_out.get()))
            
        # Significa que hem trobat algún enemic
        if len(rectangles_enemies) > 0:
            for rec in rectangles_enemies:
                target = rec.printRectangle(target, False)

        # Agafam els punts d'en Mario
        rectangles = queue_mario_out.get()
        for i in range(n_processos_mario-1):
            rectangles = np.concatenate((rectangles, queue_mario_out.get()))

        # Significa que no hem trobat en Mario
        if len(rectangles) == 0:
            mario_no_vist = mario_no_vist + 1
            if punt_x_anterior == -1 and punt_y_anterior == - 1:
                sub_img = captura
            else:
                # Feim que el ROI sigui més gran per tal de poder trobar en Mario dins una regió un poc més gran
                # en comparació l'anterior.
                trobat_anteriorment = False
                sub_img = selectROI(captura, punt_x_anterior, punt_y_anterior,
                                    (offset + offsetXtra), (offset + offsetXtra))
        else:
            mario_no_vist = 0
            for rec in rectangles:
                center_x, center_y = rec.rectangleToPoint()

                # Hem cercat en Mario dins la imatge original
                if punt_x_anterior == -1 and punt_y_anterior == - 1:
                    target = rec.printRectangle(target, False)

                    sub_img = selectROI(captura, center_x, center_y, offset, offset)

                    # Actualitzam punts anteriors
                    punt_x_anterior = center_x
                    punt_y_anterior = center_y
                else:
                    # Si no l'haviem trobat anteriorment, significa que hem usat l'offset extra per crear el ROI
                    if not(trobat_anteriorment):
                        nou_punt_x = (punt_x_anterior - (offset + offsetXtra)) + center_x
                        nou_punt_y = (punt_y_anterior - (offset + offsetXtra)) + center_y
                    else:
                        nou_punt_x = (punt_x_anterior - offset) + center_x
                        nou_punt_y = (punt_y_anterior - offset) + center_y

                    rec.canviaCentre(nou_punt_x, nou_punt_y)
                    target = rec.printRectangle(target)

                    sub_img = selectROI(captura, nou_punt_x, nou_punt_y, offset, offset)

                    punt_x_anterior = nou_punt_x
                    punt_y_anterior = nou_punt_y

            trobat_anteriorment = True

        if punt_x_anterior == 72 or (punt_x_anterior == 144 and (time() - start_time) > 8):
            # print("Aquesta xarxa no té futur")
            next = True
            punt_x_anterior = -1
            punt_y_anterior = -1
            sub_img = cv.imread('defaultframe.png')
            continue

        # Visors
        if punt_x_anterior != -1 and punt_y_anterior != -1:
            visors = doLine(target, config.n_visors, punt_x_anterior, punt_y_anterior, config.graus)
            inputs = visors + [punt_x_anterior, punt_y_anterior]

            # Convertim a matriu d'una sola dimensió
            myinputs = np.zeros((len(inputs), 1))
            myinputs[:, 0] = inputs

            output = network.getXarxaActual().feedforward(myinputs)
            queue_doMoves_out.get() # Bloqueja fil principal

            if config.moviments == 2:
                a = 0
                if (output[0][0] > 0.5):
                    a = 1

                queue_doMoves.put([a])
                if a == 0:
                    network.getXarxaActual().incrementaRecorregut()
                else:
                    network.getXarxaActual().incrementaVegadesC()

            else:

                a = 0
                b = 0
                if (output[0][0] > 0.5):
                    a = 1
                if (output[1][0] > 0.5):
                    b = 1
                queue_doMoves.put([a, b])

                if a == 1 and b == 0:
                    network.getXarxaActual().decrementaRecorregut()
                elif a == 1 and b == 1:
                    network.getXarxaActual().incrementaRecorregut()
                elif a == 0 and b == 1:
                    network.getXarxaActual().incrementaVegadesC()

                '''
                # Versió alternativa dels 4 moviments
                if a == 0 and b == 0:
                    network.getXarxaActual().incrementaRecorregut()
                elif a == 0 and b == 1:
                    network.getXarxaActual().decrementaRecorregut()
                '''

        #cv.imshow('Captura', captura)
        #cv.imshow('Resultat', target)
        #cv.imshow('ROI', sub_img)

        # Si fa temps que no es troba en mario. Es cercarà dins tota la captura.
        if mario_no_vist > 5:
            sub_img = captura
            punt_x_anterior = -1
            punt_y_anterior = -1

        # Si el ROI no es quadrat, donam el valor de la captura per evitar errors de tamany.
        if sub_img.shape[0] != sub_img.shape[1] and sub_img.shape[0] != captura.shape[0] \
                and sub_img.shape[1] != captura.shape[1]:
            sub_img = captura
            punt_x_anterior = -1
            punt_y_anterior = -1

        # Mostra els FPS per consola
        if printLoop:
            print('FPS {}'.format(1 / (time() - loop_time)))
            loop_time = time()

        root.update()

    root.destroy()
    KeyBoardInput.release('d', 'a')

    # Finalitzam tots els processos
    for i in range(n_processos_mario):
        queue_mario_in.put([])

    for i in range(n_processos_enemics):
        queue_enemies_in.put([])

    queue_doMoves.put([])

if __name__== '__main__':
    main()