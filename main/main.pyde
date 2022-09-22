import os
import time
import random
from importlib import import_module
import player, track, navigator

desenhar=1
nPista=1
nSensores=3
pista = []
acceleration_delay = 0
trainingMode = True


def setup():
    ae = open("AE.txt", "r")
    """if(ae.read() == ""):
        ae.close()
        ae = open("AE.txt", "a")
        ae.write("geracao 1:\n")
        for i in range(30):
            dSpeed = random.randint(1,15)
            tSpeed = random.randint(1,15)
            rDelay = random.randint(1,60)
            ae.write(str(dSpeed) + " " + str(tSpeed) + " " + str(rDelay) + "\n")"""
    aeData = ae.read()
    ae.close()     
    aeStrings = aeData.split("\n")
    aeStrings.remove("")
    n = len(aeStrings) - 30
    print(aeStrings)
    del aeStrings[:n]
    print(aeStrings)
    size(1200, 700)
    track.inicializa_pista(pista, nPista)
    global car, ai
    if(nPista == 0):
        car = player.player(450, 180)
    elif(nPista == 1):
        car = player.player(400, 180)
    elif(nPista == 2):
        car = player.player(450, 180)
    
    ai = []
    for cromossome in aeStrings:
        dSpeed, tSpeed, rDelay = cromossome.split(" ")
        ai.append(navigator.navigator(car, dSpeed, tSpeed, rDelay, nPista))
    #print(ai)
    background(255)
    track.desenha(pista, nPista)
    car.drawPlayer()
def draw():
    global pista, nPista, player, trainingMode
    
    if(trainingMode):
        while(trainingMode):
            for candidate in ai:
                candidate.navigate()
                candidate.trainNpc()
                print(candidate.npc.x, candidate.npc.y )
            time.sleep(0.5)
    else:
        background(255)
        #car.accelerate()
        track.desenha(pista, nPista)
        ai.navigate()
        #car.drawPlayer()
        ai.drawNpc()
    
def keyPressed():
    global trainingMode
    if(key == 'w' or key == 'W'):
        car.setFowardTrue()
    if(key == 's' or key == 'S'):
        car.setBackTrue()
    if(key == 'a' or key == 'A'):
        car.setLeftTrue()
    if(key == 'd' or key == 'D'):
        car.setRightTrue()
    if(key == 'v' or key == 'V'):
        trainingMode = not trainingMode

    
def keyReleased():
    if(key == 'w' or key == 'W'):
        car.setFowardFalse()
    if(key == 's' or key == 'S'):
        car.setBackFalse()
    if(key == 'a' or key == 'A'):
        car.setLeftFalse()
    if(key == 'd' or key == 'D'):
        car.setRightFalse()
    
