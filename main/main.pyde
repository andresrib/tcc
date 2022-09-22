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
    size(1200, 700)
    if(not trainingMode):
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
        #print(aeStrings)
        del aeStrings[:n]
        #print(aeStrings)
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
            dSpeed, tSpeed, rDelay, = cromossome.split(" ")
            ai.append(navigator.navigator(car, int(dSpeed), int(tSpeed), int(rDelay), nPista))
        #print(ai)
        background(255)
        track.desenha(pista, nPista)

def draw():
    global pista, nPista, player, trainingMode
    
    if(trainingMode):
        nPista = random.randint(0, 2)
        ae = open("AE.txt", "r")
        aeData = ae.read()
        ae.close()     
        aeStrings = aeData.split("\n")
        aeStrings.remove("")
        n = len(aeStrings) - 30
        del aeStrings[:n]
        
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
            dSpeed, tSpeed, rDelay, = cromossome.split(" ")
            ai.append(navigator.navigator(car, int(dSpeed), int(tSpeed), int(rDelay), nPista))
        #print(ai)
        background(255)
        track.desenha(pista, nPista)
        while(ai[0].laps == 0 and ai[1].laps == 0 and ai[2].laps == 0 and ai[3].laps == 0 and ai[4].laps == 0 and ai[5].laps == 0 and ai[6].laps == 0 and ai[7].laps == 0 and ai[8].laps == 0 and ai[9].laps == 0 and ai[10].laps == 0 
                  and ai[11].laps == 0 and ai[12].laps == 0 and ai[13].laps == 0 and ai[14].laps == 0 and ai[15].laps == 0 and ai[16].laps == 0 and ai[17].laps == 0 and ai[18].laps == 0 and ai[19].laps == 0 and ai[20].laps == 0 
                      and ai[21].laps == 0 and  ai[22].laps == 0 and ai[23].laps == 0 and ai[24].laps == 0 and ai[25].laps == 0 and ai[26].laps == 0 and ai[27].laps == 0 and ai[28].laps == 0 and ai[29].laps == 0):
            for candidate in ai:
                candidate.navigate()
                candidate.trainNpc()
                print(candidate.npc.x, candidate.npc.y )
            #time.sleep(0.5)
        best = [ai[0].desiredSpeed, ai[0].turningSpeed, ai[0].reverseDelay, ai[0].fitness]
        with open("Fitness.txt", "a") as fit:
            for candidate in ai:
                fit.write(str(candidate.fitness) + "\n")
                if(candidate.fitness < best[3]):
                    best = [candidate.desiredSpeed, candidate.turningSpeed, candidate.reverseDelay, candidate.fitness]
        with open("AE.txt", "a") as ae:
            for candidate in ai:
                if (candidate.desiredSpeed != best[0] or candidate.turningSpeed != best[1] or candidate.reverseDelay != best[2]):
                    if(random.randint(1, 20) != 1):
                        dSpeed = (candidate.desiredSpeed + best[0])//2
                    else:
                        dSpeed = random.randint(1,15)
                    if(random.randint(1, 20) != 1):
                        tSpeed = (candidate.turningSpeed + best[1])//2
                    else:
                        tSpeed = random.randint(1,15)
                    if(random.randint(1, 20) != 1):
                        rDelay = (candidate.reverseDelay + best[2])//2
                    else:
                        rDelay = random.randint(1,60)
                else:
                    dSpeed = best[0]
                    tSpeed = best[1]
                    rDelay = best[2]
                ae.write(str(dSpeed) + " " + str(tSpeed) + " " + str(rDelay) + "\n")
            
    else:
        background(255)
        #car.accelerate()
        track.desenha(pista, nPista)
        ai[0].navigate()
        #car.drawPlayer()
        ai[0].drawNpc()
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
    #if(key == 'v' or key == 'V'):
    #    trainingMode = not trainingMode

    
def keyReleased():
    if(key == 'w' or key == 'W'):
        car.setFowardFalse()
    if(key == 's' or key == 'S'):
        car.setBackFalse()
    if(key == 'a' or key == 'A'):
        car.setLeftFalse()
    if(key == 'd' or key == 'D'):
        car.setRightFalse()
    
