import os
import time
import random
from importlib import import_module
import player, track, navigator

desenhar=1
nPista=2#random.randint(0, 2)
nSensores=3
pista = []
acceleration_delay = 0
trainingMode = True



def setup():
    global car, ai, loops
    size(1200, 700)
    track.inicializa_pista(pista, nPista)
    ai = []
    if(nPista == 0):
        car = player.player(450, 180)
    elif(nPista == 1):
        car = player.player(400, 180)
    elif(nPista == 2):
        car = player.player(450, 180)
    for i in range(30):
        ai.append(navigator.navigator(car, random.randint(1, 15), random.randint(1, 15), random.randint(1, 60), nPista))
    background(255)
    track.desenha(pista, nPista)
    
    loops = 0
    if(trainingMode):
        open('Fitness.txt', 'w').close()
        open('gn.txt', 'w').close()
def draw():
    global pista, nPista, player, trainingMode, loops
    
    if(trainingMode):
        global car, ai
        if(nPista == 0):
            car = player.player(450, 180)
        elif(nPista == 1):
            car = player.player(400, 180)
        elif(nPista == 2):
            car = player.player(450, 180)
        background(255)
        track.desenha(pista, nPista)
        while(ai[0].laps == 0 or ai[1].laps == 0 or ai[2].laps == 0 or ai[3].laps == 0 or ai[4].laps == 0 or ai[5].laps == 0 or ai[6].laps == 0 or ai[7].laps == 0 or ai[8].laps == 0 or ai[9].laps == 0 or ai[10].laps == 0 
                  or ai[11].laps == 0 or ai[12].laps == 0 or ai[13].laps == 0 or ai[14].laps == 0 or ai[15].laps == 0 or ai[16].laps == 0 or ai[17].laps == 0 or ai[18].laps == 0 or ai[19].laps == 0 or ai[20].laps == 0 
                      or ai[21].laps == 0 or  ai[22].laps == 0 or ai[23].laps == 0 or ai[24].laps == 0 or ai[25].laps == 0 or ai[26].laps == 0 or ai[27].laps == 0 or ai[28].laps == 0 or ai[29].laps == 0):
            for candidate in ai:
                #if (candidate.laps == 0):
                    
                #if(candidate.fitness>1800 and candidate.laps == 0):
                #    candidate.laps = 1
                candidate.navigate()
                candidate.trainNpc()
            print(ai[0].fitness)
        best = [ai[0].desiredSpeed, ai[0].turningSpeed, ai[0].reverseDelay, ai[0].fitness]
        with open("Fitness.txt", "a") as fit:
            average = 0
            for candidate in ai:
                average += candidate.fitness
                if(candidate.fitness < best[3]):
                    best = [candidate.desiredSpeed, candidate.turningSpeed, candidate.reverseDelay, candidate.fitness]
            fit.write(str(best[3]) + "\t"  + str(average/30) + "\n")
        newAi = []
        with open("gn.txt", "a") as gn:
            for candidate in ai:
                gn.write(str(candidate.desiredSpeed) + " " + str(candidate.turningSpeed) + " " + str(candidate.reverseDelay) + " " + str(candidate.fitness) + "\n")
                if (candidate.desiredSpeed != best[0] or candidate.turningSpeed != best[1] or candidate.reverseDelay != best[2]):
                    dSpeed = (candidate.desiredSpeed + best[0])//2
                    tSpeed = (candidate.turningSpeed + best[1])//2
                    rDelay = (candidate.reverseDelay + best[2])//2
                    if(random.randint(1, 20) == 1):
                        dSpeed = random.randint(1,15)
                    if(random.randint(1, 20) == 1):
                        tSpeed = random.randint(1,15)
                    if(random.randint(1, 20) == 1):
                        rDelay = random.randint(1,60)
                else:
                    dSpeed = best[0]
                    tSpeed = best[1]
                    rDelay = best[2]
                newAi.append(navigator.navigator(car, int(dSpeed), int(tSpeed), int(rDelay), nPista))
            gn.write("\n")
            ai = newAi
            #print(loops)
            loops = loops + 1
            if(loops >= 50):
                exit()
    else:
        background(255)
        #car.accelerate()
        track.desenha(pista, nPista)
        ai[0].navigate()
        strokeWeight(10)
        stroke(0, 0, 255)
        point(450, 500)
        point(450, 380)
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
    
