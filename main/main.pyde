import os
from importlib import import_module
import player, track

desenhar=1
nPista=1
nSensores=3
pista = []



def setup():
    size(1200, 700)
    track.inicializa_pista(pista, nPista)
    global car
    car = player.player() 

def draw():
    global pista, nPista, player
    noFill()
    track.desenha(pista, nPista)
    car.drawPlayer()
    
def keyPressed():
    car.accelerate(k = key)
