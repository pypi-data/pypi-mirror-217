# -*- coding: utf-8 -*-
""" This is the CLPU module to work with data from metrology.

Please do only add or modify but not delete content.

requires explicitely {
 - os
 - tkinter
 - numpy
 - cv2
 - typing
}

import after installation of pyclpu via {
  from pyclpu import metrology
}

import without installation via {
  root = os.path.dirname(os.path.abspath(/path/to/pyclpu/metrology.py))
  sys.path.append(os.path.abspath(root))
  import metrology
  from importlib import reload 
  reload(metrology)
}

"""

# =============================================================================
# PYTHON HEADER
# =============================================================================
# EXTERNALimport cv2
import os
from tkinter import filedialog #not for the function
import numpy as np
from typing import List, Tuple

# =============================================================================
# CLASSES
# =============================================================================
class ThomsonParabola:
    def __init__(self):
        pass
    # seleccionar_carpeta_destino(): This function open a folder dialog and allow select a destination folder
    # inputs: none
    # outputs; string with the folder path
    @staticmethod
    def Seleccionar_carpeta_destino() -> str:
        carpeta_destino = filedialog.askdirectory(title="Seleccionar carpeta de destino")
        return carpeta_destino

    # seleccionar_archivos(): This function open a multiple filedialog and allow select a destination folder
    # inputs: none
    # outputs: List of string with the files path
    @staticmethod
    def Seleccionar_archivos() -> List[str]:
        archivos = filedialog.askopenfilenames(title="Seleccionar archivos", filetypes=(
        ("Archivos TIFF", "*.tiff;*.tif"), ("Todos los archivos", "*.*")))
        lista = []
        lista.extend(archivos)
        return lista

    # _searchpoint(img, a, sea, k): auxiliar function in cas that the trace is lost allow to search forward one pixel more selecting the best value
    # in the next five pixels adjacent
    # input img: image that is anlizing
    #       pointlist  : list of selected point for this trace
    #       previousvalue: previous value for the Y coordinate
    #       actualX: actual x value in the scan
    # output: the previous value of y
    @staticmethod
    def _searchpoint(img, pointlist, previousvalue, actualX):
        try:
            # create a dictionary
            asa = {}
            # load the adjacent values
            for l in range(3):
                asa[l] = img[actualX, int(previousvalue) + l]

            # select the maximum values
            max_value = max(asa.values())

            # append the best value
            for key, value in asa.items():
                if value == max_value:
                    pointlist.append((int(key + previousvalue), actualX))
                    previousvalue = key + previousvalue
                    break

            return previousvalue

        except Exception as ex:
            raise Exception("searchpoint fail")

    # _rows(img, a, sea, k): auxiliar function search the local maximum in one row
    # input img: image that is anlizing
    #       clone  : copy of image where the local maximum are highligthed
    #       previousvalue: previous value for the Y coordinate
    #       actualX: actual row
    #       threshold: the difference between two point in order to be considered a local maximum
    @staticmethod
    def _rows(img, clone, actualX, threshold):
        # initialize variables
        # set to save the maximum
        localmax = set()

        # row of the image proccesed
        row = img[actualX:actualX + 1, :]

        localMaxima = []
        oldstatus = 0
        newstatus = 0
        maxvalue = 0
        maxvalex = 0

        # scan the row.  Works as a states machine searching for flanks
        for x in range(row.shape[1] - 1):
            centerValue = int(row[0, x])
            rightValue = int(row[0, x + 1])

            if rightValue - centerValue > threshold:
                if newstatus == 0 and oldstatus == 0:
                    minx = x
                    oldstatus = 0
                    newstatus = 1
            elif centerValue - rightValue > threshold:
                if newstatus == 1 and oldstatus == 1:
                    oldstatus = 1
                    newstatus = 0
            else:
                if newstatus == 1 and oldstatus == 0:
                    oldstatus = 1
                    newstatus = 1
                    if maxvalue < centerValue:
                        maxvalue = centerValue
                        maxvalex = x
                elif newstatus == 0 and oldstatus == 1:
                    maxx = x
                    oldstatus = 0
                    newstatus = 0
                    p = (maxvalex, actualX)
                    localMaxima.append(p)
                    localmax.add(maxvalex)

                    maxvalue = 0
                    maxvalex = 0
                elif newstatus == 1 and oldstatus == 1:
                    if maxvalue < centerValue:
                        maxvalue = centerValue
                        maxvalex = x

        # highlight the local maximum
        for maxima in localMaxima:
            cv2.circle(clone, maxima, 1, (255, 255, 0))

        # return the local maximum ordered
        return sorted(localmax)

    # ThompsomParabolaImageprocessingV2: This function search for the different traces in a Thomson parabola image. produces five folder:
    # folder input save the original image
    # folder output save the original image where the traces are painted with different colours
    # folder mask save the traces with different colours
    # folfer ouput gray save the traces without discrimination
    # folder text save the sum of the 5 adjacent values in a csv
    # input: pathDestinationSelected: output folder
    #       picturesSelected: List of path for the different pictures
    #       coluours: List of colours to be used in the different outputs like mask. should be a tuple RGB
    #       threshold: the difference between two point in order to be considered a local maximum
    #       wake: The maximum number of points tha can be founded with searchpoint function
    #       quality: the minimum number of real point admmited in a trace
    @staticmethod
    def ThompsomParabolaImageprocessingV2(pathDestinationSelected: str, picturesSelected: List[str],
                                          colours: List[Tuple[int, int, int]], threshold: int, wake: int, qualit: int):
        # intialize variables
        pictures = picturesSelected
        removepictures = []
        filename = ""

        # output paths
        pathinputs = os.path.join(pathDestinationSelected, "input")
        pathoutputsgray = os.path.join(pathDestinationSelected, "output_gray")
        pathoutputs = os.path.join(pathDestinationSelected, "output")
        pathoutputsmask = os.path.join(pathDestinationSelected, "mask")
        pathoutputtext = os.path.join(pathDestinationSelected, "text")

        # create the folder
        if not os.path.exists(pathinputs):
            os.makedirs(pathinputs)

        if not os.path.exists(pathoutputs):
            os.makedirs(pathoutputs)

        if not os.path.exists(pathoutputsgray):
            os.makedirs(pathoutputsgray)

        if not os.path.exists(pathoutputsmask):
            os.makedirs(pathoutputsmask)

        if not os.path.exists(pathoutputtext):
            os.makedirs(pathoutputtext)

        # start the proccess
        try:
            # scan each file in the List
            for file in picturesSelected:

                # inicialize variables
                memory = {}
                quality = {}
                trazas = {}

                # get the name of the file
                filename = os.path.basename(file)

                # read the file
                img = cv2.imread(file, cv2.IMREAD_ANYDEPTH | cv2.IMREAD_GRAYSCALE)

                # filter the X ray in the image
                cv2.medianBlur(img, 5, img)

                # prepare the different output images
                clone = img.copy()
                clone = cv2.convertScaleAbs(clone, alpha=(255.0 / 65535.0))
                clone3 = img.copy()
                clone3 = cv2.convertScaleAbs(clone3, alpha=(255.0 / 65535.0))
                original = img.copy()
                clone2 = np.zeros_like(img, dtype=np.uint8)
                clone4 = np.zeros_like(img, dtype=np.uint8)
                clone = cv2.cvtColor(clone, cv2.COLOR_GRAY2RGB)
                clone3 = cv2.cvtColor(clone3, cv2.COLOR_GRAY2RGB)

                # range of row scans
                range_iter = range(1020, -1, -1)

                # search the local maximum
                for i in range_iter:
                    sort = ThomsonParabola._rows(img, clone2, i, threshold)
                    if len(sort) != 0:
                        memory[i] = sort
                memory = {k: memory[k] for k in sorted(memory.keys())}

                # combinin the different maximum to find the nearest if doesnt exist search with sarchpoint function a point
                init2 = list(memory.keys())
                counter = 1

                if memory:
                    for j in range(init2[0], init2[-1]):
                        a = []
                        rem = {}

                        # check the actual y in memory
                        if j in memory:
                            qul = 0
                            flse = 0
                            # select all the local maximum in a row
                            for prev in memory[j]:
                                flse = 0
                                a = []
                                a.append((prev, j))
                                me = prev
                                meme = prev
                                qul += 1
                                if j in rem:
                                    rem[j].append(int(meme))
                                else:
                                    aux = []
                                    aux.append(int(me))
                                    rem[j] = aux
                                # compare with the next row to find the closest maximum
                                for k in range(j + 1, init2[-1]):
                                    if k in memory:
                                        if len(memory[k]) != 0:
                                            c1 = 0
                                            for sea in memory[k]:
                                                if sea + 3 >= me and sea - 3 <= me:
                                                    a.append((sea, k))
                                                    c1 = 1
                                                    meme = sea
                                                    me = sea
                                                    qul += 1
                                                    flse = 0
                                                    break
                                                elif sea + 6 >= me and sea <= me:
                                                    meme = sea
                                                    qul += 1
                                                    c1 = 1
                                                    me = ThomsonParabola._searchpoint(img, a, sea, k)
                                                    break
                                                else:
                                                    c1 = 2
                                            if c1 == 1:
                                                if k in rem:
                                                    rem[k].append(int(meme))
                                                else:
                                                    aux = []
                                                    aux.append(int(meme))
                                                    rem[k] = aux
                                                c1 = 0
                                            elif c1 == 2:
                                                me = ThomsonParabola._searchpoint(img, a, me, k)
                                                flse += 1
                                                if flse > wake:
                                                    break
                                        else:
                                            me = ThomsonParabola._searchpoint(img, a, me, k)
                                            flse += 1
                                            if flse > wake:
                                                break
                                    else:
                                        me = ThomsonParabola._searchpoint(img, a, me, k)
                                        flse += 1
                                        if flse > wake:
                                            break
                                    if me > 1200:
                                        break
                                    if flse > wake and len(a) == wake:
                                        for l in range(wake):
                                            a.pop()

                                        break
                                # save the trace and the quality of the trace
                                trazas[counter] = a
                                quality[counter] = qul
                                if counter == 162:
                                    counter = counter
                                qul = 0
                                counter += 1
                                # remove the local maximum already used in this trace
                                for kk in rem.keys():
                                    for kkk in rem[kk]:
                                        if kkk in memory[kk]:
                                            memory[kk].remove(kkk)

                                # remove the traces with not enough quality
                                for a in quality.items():
                                    if a[1] < qualit:
                                        trazas.pop(a[0], None)
                # save proccess
                c3 = 0
                for trazalist in trazas.keys():
                    trazasarray = trazas[trazalist]

                    # save one file for each trace
                    pathoutputtext2 = os.path.join(pathoutputtext, filename)

                    # create path
                    if not os.path.exists(pathoutputtext2):
                        os.makedirs(pathoutputtext2)
                    nam = "Traza" + str(c3) + ".csv"

                    # write csv and prepare the other outputs
                    with open(os.path.join(pathoutputtext2, nam), 'w') as writer:
                        for l in range(len(trazasarray) - 1):
                            clone3 = cv2.line(clone3, trazasarray[l], trazasarray[l + 1], colours[c3], 4)
                            clone4 = cv2.line(clone4, trazasarray[l], trazasarray[l + 1], 255, 3)
                            X = trazasarray[l][0]
                            Y = trazasarray[l][1]

                            Summa = int(original[Y, X - 2]) + int(original[Y, X - 1]) + int(original[Y, X]) + int(
                                original[Y, X + 1]) + int(original[Y, X + 2])
                            towrite = f"{X},{Y},{Summa}"
                            writer.write(towrite + "\n")

                    c3 += 1
                # save the other files
                cv2.imwrite(os.path.join(pathinputs, filename), clone)
                cv2.imwrite(os.path.join(pathoutputs, filename + "out.tiff"), clone3)
                cv2.imwrite(os.path.join(pathoutputsgray, filename + "out2.tiff"), clone2)
                cv2.imwrite(os.path.join(pathoutputsmask, filename + "mask.tiff"), clone4)
                print(filename + "  processed\n")

        # in case of fail the processed picturs are removed and the proccess is restarted
        except Exception as ex:
            print(ex)
            print(filename + "  fail\n")

            for f in removepictures:
                pictures.pop(f)
            # ThompsomParabolaImageprocessingV2(pathDestinationSelected,pictures,colours,threshold,wake,qualit)
