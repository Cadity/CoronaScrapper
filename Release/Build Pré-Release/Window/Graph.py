import tkinter as tk
from tkinter import messagebox
from Scrapper.WriteData import MainFunction, Etape_E, WriteFile, GetGenList
from math import *

def GetValues():
    # Déclaration de variables
        maxValue = 0
        minValue = 100
        genList = GetGenList()
        valCV = list()
        valPang = list()
        errorList = list()

        for a in genList: # On crée une boucle dans lequel a prends la valeur d'une occurence de la liste Genlist
            try: # On essaye de collecter les taux de conservations ...
                valCV.append(Etape_E(a.split("Protéine ")[1])[4]) # ... pour la protéine a de la Chauve-souris
                valPang.append(Etape_E(a.split("Protéine ")[1])[5]) # ... pour la protéine a du pangolin
                # ... par rapport à l'homme
            except: # Levée d'une exception si le gène n'a pas réussi à être analysé
                errorList.append(a) # On le retire de la liste parce qu'il ne correspond à aucune valeur dans les listes de taux de conservations

        errorString = ""
        for b in errorList:
            errorString = errorString + b.split("Protéine ")[1] + ", "
            genList.remove(b)

        analysisError = messagebox.showinfo(title="Erreur d'acquisition des informations sur le gène", message="Le(s) gène(s) " + errorString + "est/sont inaccessible(s)")

        finalList = list()
        finalList.append(genList)
        finalList.append(valCV)
        finalList.append(valPang)
        return finalList

def DisplayGraph():
    def draw_samples (canvas, lght, dataList):

        genList = dataList[0]
        valCV = dataList[1]
        valPang = dataList[2]

        canWidht = lght[0]
        canHeight = lght[1]

        minXLoc = canWidht * 0.07
        maxXLoc = canHeight * 0.9

        canvas.create_line ((minXLoc, canHeight * 0.1), (minXLoc, maxXLoc),
                            fill="black", width=3, arrow="first", arrowshape=(10,20,10))

        canvas.create_line ((canWidht * 0.97, maxXLoc), (minXLoc, maxXLoc),
                            fill="black", width=3, arrow="first", arrowshape=(10,20,10))

        canvas.create_text (canWidht * 0.94, maxXLoc + 30, text= "x (gènes)",
                        fill= "black", font= ("courier", 20, "bold italic"),
                        anchor="center", justify= "center")

        canvas.create_text (canWidht * 0.15, canHeight * 0.1 - 20, text= "y (taux de conservation %)",
                        fill= "black", font= ("courier", 20, "bold italic"),
                        anchor="center", justify= "center")


        posY = canWidht * 0.15
        # Création de la liste

        height = canHeight - 500

        def MakeSideValue():
            minValue = 100
            maxValue = 0

            for x in range(len(genList)):
                if valCV[x] < minValue:
                    minValue = valCV[x]

                if valCV[x] > maxValue:
                    maxValue = valCV[x]

                if valPang[x] < minValue:
                    minValue = valPang[x]

                if valPang[x] < minValue:
                    maxValue = valPang[x]
            
            minValue = round(minValue, 0)
            maxValue = round(maxValue, 0)
            tempMaxValue = maxValue

            heightSize = (maxXLoc - minXLoc - 40) / (maxValue - minValue)
            posX = heightSize + 50
            maxX = posX

            while maxValue != minValue - 1:
                canvas.create_text (minXLoc - 40, posX, text= str(maxValue) + "%",
                        fill= "black", font= ("courier", 15, "bold italic"),
                        anchor="center", justify= "center")
                posX = posX + heightSize
                maxValue = maxValue - 1

            cvXValue = list()
            pangXValue = list()
            print(valPang)
            for x in range(len(genList)):

                if valPang[x] % 1 > 0.5:
                    pgVal = round(tempMaxValue - valPang[x], 0) + 1
                else:
                    pgVal = round(tempMaxValue - valPang[x], 0)

                if valCV[x] % 1 > 0.5:
                    cvVal = round(tempMaxValue - valCV[x], 0) + 1
                else:
                    cvVal = round(tempMaxValue - valCV[x], 0)

                if cvVal == 0:
                    cvVal = maxX
                else:
                    cvVal = maxX + (cvVal * heightSize)
                    cvVal = cvVal - (valCV[x] - floor(valCV[x])) * heightSize

                if pgVal == 0:
                    pgVal = maxX
                else:
                    print(pgVal) 
                    pgVal = maxX + (pgVal * heightSize)
                    
                    pgVal = pgVal - (valPang[x] - floor(valPang[x])) * heightSize

                cvXValue.append(cvVal)
                pangXValue.append(pgVal)

            print(pangXValue)
            return (cvXValue, pangXValue)

        heightList = MakeSideValue()

        for x in range(len(genList)):

            heightCV = heightList[0][x]
            heightPang = heightList[1][x]

            canvas.create_text (posY, maxXLoc + 15, text= genList[x],
                        fill= "black", font= ("courier", 15, "bold italic"),
                        anchor="center", justify= "center")

            canvas.create_line ((posY - 30, heightCV), (posY - 30, maxXLoc),
                            fill="green", width=10)
            
            canvas.create_text (posY - 40, heightCV - 20, text= str(valCV[x]) + " %\n(Chauve-Souris)",
                        fill= "black", font= ("courier", 11),
                        anchor="center", justify= "center") 


            posY = posY + 70

            canvas.create_text (posY - 10, heightPang - 20, text= str(valPang[x]) + " %\n(Pangolin)",
                        fill= "black", font= ("courier", 11),
                        anchor="center", justify= "center") 

            canvas.create_line ((posY - 30, heightPang), (posY - 30, maxXLoc),
                            fill="red", width=10)
             
            posY = posY + 200
            
    resultList = GetValues()
    root= tk.Tk()
    root.title ("CoronaWrapper - Graphique")
    lght = (1200, 800)

    canvas=tk.Canvas(root, width=lght[0], height=lght[1], bg="white")
    canvas.pack()
    draw_samples (canvas, lght, resultList)
    root.mainloop()