import os
from importlib import import_module
import player, track, navigator

desenhar=1
nPista=1
nSensores=3
pista = []
acceleration_delay = 0



def setup():
    size(1200, 700)
    track.inicializa_pista(pista, nPista)
    global car, ai
    
    car = player.player() 
    ai = navigator.navigator(car)

def draw():
    global pista, nPista, player
    background(255)
    #car.accelerate()
    
    #ai.npc.accelerate()
    track.desenha(pista, nPista)
    ai.navigate()
    #car.drawPlayer()
    ai.drawNpc()
    
    
"""def keyPressed():
    if(key == 'w' or key == 'W'):
        ai.npc.setFowardTrue()
    if(key == 's' or key == 'S'):
        ai.npc.setBackTrue()
    if(key == 'a' or key == 'A'):
        ai.npc.setLeftTrue()
    if(key == 'd' or key == 'D'):
        ai.npc.setRightTrue()

    
def keyReleased():
    if(key == 'w' or key == 'W'):
        car.setFowardFalse()
    if(key == 's' or key == 'S'):
        car.setBackFalse()
    if(key == 'a' or key == 'A'):
        car.setLeftFalse()
    if(key == 'd' or key == 'D'):
        car.setRightFalse()"""
    
