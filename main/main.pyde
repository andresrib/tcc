import os
from importlib import import_module
import player, track

desenhar=1
nPista=1
nSensores=3
pista = []
acceleration_delay = 0



def setup():
    size(1200, 700)
    track.inicializa_pista(pista, nPista)
    global car
    
    car = player.player() 

def draw():
    global pista, nPista, player
    background(255)
    car.accelerate()
    track.desenha(pista, nPista)
    car.drawPlayer()
    
def keyPressed():
    if(key == 'w' or key == 'W'):
        car.setFowardTrue()
    if(key == 's' or key == 'S'):
        car.setBackTrue()
    if(key == 'a' or key == 'A'):
        car.setLeftTrue()
    if(key == 'd' or key == 'D'):
        car.setRightTrue()

    
def keyReleased():
    if(key == 'w' or key == 'W'):
        car.setFowardFalse()
    if(key == 's' or key == 'S'):
        car.setBackFalse()
    if(key == 'a' or key == 'A'):
        car.setLeftFalse()
    if(key == 'd' or key == 'D'):
        car.setRightFalse()
    
