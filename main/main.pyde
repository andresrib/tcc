import os
import time
import random
from importlib import import_module
import player, track, navigator


nPista=1
#modo de treino, sendo 0 nao treinando, 1 treinando visualmente de forma lenta e 2 sendo o treino nao visual rapido
trainingMode = 2

colisionWeight = 1

geracoes = 50

populacao = 60

pista = []

runTimes = 3

#escolha das pista, entre 0 1 e 2
tracks = [0, 1, 2]

ran = 0



running = False

def setup():
    global car, ai, loops, candidate_number, tester, initial_x, initial_y, best, goal, tracks, nPista
    goal = 2
    size(1200, 700)
    track.inicializa_pista(pista, tracks[nPista])
    ai = []
    #define as posicoes iniciais do carro de acordo com a pista
    if(tracks[nPista] == 0):
        initial_x = 450
        initial_y = 180
    elif(tracks[nPista] == 1):
        initial_x = 400
        initial_y = 180
    elif(tracks[nPista] == 2):
        initial_x = 450
        initial_y = 180
    car = player.player(initial_x, initial_y)
    #inicia um navegador de teste para o modo de treino 0 0 14 52.0 72.0 57.0, 1 2 14 50 72.0 61.0
    #3 5 14 61.0 74.0 40
    tester = navigator.navigator(car, 11, 8, 29, tracks[nPista], 63, 56, 47)
    #inicia os 30 navegadores iniciais para o treino
    for i in range(populacao):
        ai.append(navigator.navigator(player.player(450, 180), random.randint(1, 15), random.randint(1, 15), random.randint(1, 60), tracks[nPista], random.randint(30, 90), random.randint(30, 90), random.randint(30, 90)))
    #inicia um placeholder para o melhor da geracao
    best = navigator.navigator(player.player(450, 180), random.randint(1, 15), random.randint(1, 15), random.randint(1, 60), tracks[nPista], random.randint(30, 90), random.randint(30, 90), random.randint(30, 90))#[0, 0, 0, 1802]
    best.fitness = 1000000000
    clear()
    background(255)
    track.desenha(pista, tracks[nPista])
    
    loops = 0
    candidate_number = 0
    
    #apaga os dados dos arquivos
    if(trainingMode != 0):
        open('Fitness.txt', 'w').close()
        open('gn.txt', 'w').close()
        #frameRate(28800)
        #frameRate(180)
    else:
        frameRate(30)
def draw():
    global pista, nPista, player, trainingMode, loops, car, ai, candidate_number, initial_x, initial_y, best, goal, running, tracks
    if trainingMode == 1:
        track.desenha(pista, tracks[nPista])
        ai[candidate_number].navigate()
        #ai[candidate_number].trainNpc()
        ai[candidate_number].drawNpc()
        #aumenta o fitness a cada frame
        if ai[candidate_number].laps < goal:
            ai[candidate_number].fitness = ai[candidate_number].fitness+1
        #confere se a geracao chegou ao final
        elif candidate_number == populacao:
            
            with open("Fitness.txt", "a") as fit:
                average = 0
                for candidate in ai:
                    average += candidate.fitness
                    #compara o fitness do melhor com todos da geracao
                    if(candidate.fitness <= best.fitness):
                        #substitui o melhor
                        best = candidate#[candidate.desiredSpeed, candidate.turningSpeed, candidate.startingReverseDelay, candidate.fitness]
                #print(best)
                #salva o melhor e a media da geracao no arquivo fitness
                fit.write(str(best.fitness) + "\t"  + str(average/30) + "\n")
            newAi = []
            with open("gn.txt", "a") as gn:
                for candidate in ai:
                    #salva os candidatos encontrados
                    gn.write(str(candidate.desiredSpeed) + " " + str(candidate.turningSpeed) + " " + str(candidate.startingReverseDelay) + " " + str(candidate.fitness) + "\n")
                    if (candidate != best):#candidate.desiredSpeed != best.desiredSpeed or candidate.turningSpeed != best.turningSpeed or candidate.startingReverseDelay != best.startingReverseDelay):
                        #cross over
                        dSpeed = (candidate.desiredSpeed + best.desiredSpeed)//2
                        tSpeed = (candidate.turningSpeed + best.turningSpeed)//2
                        rDelay = (candidate.startingReverseDelay + best.startingReverseDelay)//2
                        #mutacao
                        if(random.randint(1, 20) == 1):
                            dSpeed = random.randint(1,15)
                        if(random.randint(1, 20) == 1):
                            tSpeed = random.randint(1,15)
                        if(random.randint(1, 20) == 1):
                            rDelay = random.randint(1,60)
                    else:
                        dSpeed = best.desiredSpeed
                        tSpeed = best.turningSpeed
                        rDelay = best.startingReverseDelay
                    #adicionando o novo candidato a proxima lista de canditatos a serem testados
                    newAi.append(navigator.navigator(player.player(initial_x, initial_y), int(dSpeed), int(tSpeed), int(rDelay), tracks[nPista]))
                gn.write("\n")
                ai = newAi
                #print(loops)
                if(loops >= 49):
                    exit()
                loops = loops + 1
                candidate_number = 0
                
        else:
            candidate_number = candidate_number+1
            
            
            
    elif(trainingMode == 2):
        #testa todos os candidatos ao mesmo tempo para melhor otimizacao
        running = False
        while( not running):
            running = True
            for candidate in ai:
                if candidate.laps < goal:
                    candidate.fitness = candidate.fitness+1
                candidate.navigate()
                candidate.trainNpc()
                running = running and (candidate.laps >= goal) 
        #funcionamento igual ao training mode 1 exceto que nao reseta o candidate_number para 0, quando refatorar o código irei transformar em uma funcao para evitar redundancia       
        with open("Fitness.txt", "a") as fit:
            average = 0
            for candidate in ai:
                candidate.fitness += candidate.npc.colisions * colisionWeight
                average += candidate.fitness
                if(candidate.fitness <= best.fitness):
                    best = candidate#[candidate.desiredSpeed, candidate.turningSpeed, candidate.startingReverseDelay, candidate.fitness]
            #print(best)
            fit.write(str(best.fitness) + "\t"  + str(average/populacao) + "\n")
            crossover()
            
    #testa todas as possibilidades
    elif(trainingMode == 3):
        ai = []
        for sp in range(1, 16):
            for tsp in range(1, 16):
                for rd in range(1, 61):
                    ai.append(navigator.navigator(player.player(initial_x, initial_y), sp, tsp, rd, tracks[nPista]))
        for candidate in ai:
            while candidate.laps<goal:
                candidate.fitness = candidate.fitness+1
                candidate.navigate()
                candidate.trainNpc()
            print(candidate.fitness)
        with open("resultados/todos_fitness_pista2.txt", "w") as fit:
            average = 0
            for candidate in ai:
                average += candidate.fitness
                if(candidate.fitness <= best.fitness):
                    best = candidate#[candidate.desiredSpeed, candidate.turningSpeed, candidate.startingReverseDelay, candidate.fitness]
            #print(best)
            fit.write(str(best.fitness) + "\t"  + str(average/30) + "\n")
        with open("resultados/todos_gn_pista2.txt", "w") as gn:
                for candidate in ai:
                    gn.write(str(candidate.desiredSpeed) + " " + str(candidate.turningSpeed) + " " + str(candidate.startingReverseDelay) + " " + str(candidate.fitness) + "\n")
        exit()

        #training mode 0, modo de controle manual           
    else:
        background(255)
        #car.accelerate()
        track.desenha(pista, tracks[nPista])
        #tester.navigate()
        if tester.laps < goal:
            tester.fitness = tester.fitness+1
        else:
            print(tester.fitness)
            exit()
        #print("middle: " + str(tester.middlePoint) + "\nlaps: " + str(tester.laps))
        strokeWeight(10)
        stroke(0, 0, 255)
        #car.drawPlayer()
        tester.drawNpc()

#crossover
def crossover():
    global loops, ai, nPista, ran, runTimes
    newAi = []
    with open("gn.txt", "a") as gn:
        for candidate in ai:
            gn.write(str(candidate.desiredSpeed) + " " + str(candidate.turningSpeed) + " " + str(candidate.startingReverseDelay) + " " + str(candidate.middleSensorDistance) + " " + str(candidate.cornerSensorsDistance) + " " + str(candidate.sideSensorsDistance) + " " + str(candidate.fitness) + "\n")
            if (candidate != best):
                
                percentual = random.randint(2, 12)/10.0        
                dSpeed = candidate.desiredSpeed + ( - candidate.desiredSpeed + best.desiredSpeed) * percentual
                if dSpeed < 1:
                    dSpeed = 1
                if dSpeed > 15:
                    dSpeed = 15
                    
                percentual = random.randint(2, 12)/10.0
                tSpeed = candidate.turningSpeed + ( - candidate.turningSpeed + best.turningSpeed) * percentual
                if tSpeed < 1:
                    tSpeed = 1
                if tSpeed > 15:
                    tSpeed = 15
                    
                percentual = random.randint(2, 12)/10.0
                rDelay = candidate.reverseDelay + ( - candidate.reverseDelay + best.reverseDelay) * percentual
                if rDelay < 1:
                    rDelay = 1
                if rDelay > 60:
                    rDelay = 60
                                    
                percentual = random.randint(2, 12)/10.0
                msDistance = candidate.middleSensorDistance + ( - candidate.middleSensorDistance + best.middleSensorDistance) * percentual
                if msDistance < 30:
                    msDistance = 30
                if msDistance > 90:
                    msDistance = 90
                    
                percentual = random.randint(2, 12)/10.0
                csDistance = candidate.cornerSensorsDistance + ( - candidate.cornerSensorsDistance + best.cornerSensorsDistance) * percentual
                if csDistance < 30:
                    csDistance = 30
                if csDistance > 90:
                    csDistance = 90
                
                percentual = random.randint(2, 12)/10.0
                ssDistance = candidate.sideSensorsDistance + ( - candidate.sideSensorsDistance + best.sideSensorsDistance) * percentual
                if ssDistance < 30:
                    ssDistance = 30
                if ssDistance > 90:
                    ssDistance = 90
                
                if(random.randint(1, 10) == 1):
                    dSpeed = random.randint(1,15)
                if(random.randint(1, 10) == 1):
                    tSpeed = random.randint(1,15)
                if(random.randint(1, 10) == 1):
                    rDelay = random.randint(1,60)
                if(random.randint(1, 10) == 1):
                    msDistance = random.randint(30,90)
                if(random.randint(1, 10) == 1):
                    csDistance = random.randint(30,90)
                if(random.randint(1, 10) == 1):
                    ssDistance = random.randint(30,90)
                newAi.append(navigator.navigator(player.player(initial_x, initial_y), int(dSpeed), int(tSpeed), int(rDelay), tracks[nPista], msDistance, csDistance, ssDistance))
                
            else:
                newAi.append(best)
            
        gn.write("\n")
        ai = newAi
        #print(loops)
        if(loops >= geracoes):
            #salva os dados do experimento em arquivos persistentes
            with open("Fitness.txt", "r") as fit:
                with open("gn.txt", "r") as gn:
                    results = fit.read()
                    generations = gn.read()
                    #print(results)
                    if tracks[nPista] == 0:
                        with open ("resultados/testeRunning_fitness_pista0.txt", "a") as r:
                            r.write("melhor e media\n\n")
                            r.write(results)
                            r.write("\n\n")
                        with open ("resultados/testeRunning_gn_pista0.txt", "a") as gen:
                            gen.write("teste\n\n")
                            gen.write(generations)
                            gen.write("\n")
                    if tracks[nPista] == 1:
                        with open ("resultados/testeRunning_fitness_pista1.txt", "a") as r:
                            r.write("melhor e media\n")
                            r.write(results)
                            r.write("\n")
                        with open ("resultados/testeRunning_gn_pista1.txt", "a") as gen:
                            gen.write("teste\n\n")
                            gen.write(generations)
                            gen.write("\n")
                    if tracks[nPista] == 2:
                        with open ("resultados/testeRunning_fitness_pista2.txt", "a") as r:
                            r.write("melhor e media\n\n")
                            r.write(results)
                            r.write("\n\n")
                        with open ("resultados/testeRunning_gn_pista2.txt", "a") as gen:
                            gen.write("teste\n")
                            gen.write(generations)
                            gen.write("\n\n")
            """if ran < runTimes:
                ran = ran + 1
                restart()
                return(ai)"""
            exit()
        loops = loops + 1    
        return(newAi)
        
def restart():
    global car, ai, loops, candidate_number, tester, initial_x, initial_y, best, goal, tracks, nPista
    goal = 2
    ai = []
    #define as posicoes iniciais do carro de acordo com a pista
    if(tracks[nPista] == 0):
        initial_x = 450
        initial_y = 180
    elif(tracks[nPista] == 1):
        initial_x = 400
        initial_y = 180
    elif(tracks[nPista] == 2):
        initial_x = 450
        initial_y = 180
    car = player.player(initial_x, initial_y)
    #inicia os 30 navegadores iniciais para o treino
    for i in range(populacao):
        ai.append(navigator.navigator(player.player(450, 180), random.randint(1, 15), random.randint(1, 15), random.randint(1, 60), tracks[nPista], random.randint(30, 90), random.randint(30, 90), random.randint(30, 90)))
    #inicia um placeholder para o melhor da geracao
    best = navigator.navigator(player.player(450, 180), random.randint(1, 15), random.randint(1, 15), random.randint(1, 60), tracks[nPista], random.randint(30, 90), random.randint(30, 90), random.randint(30, 90))
    best.fitness = 1000000000
    
    loops = 0
    candidate_number = 0
    
    #apaga os dados dos arquivos
    if(trainingMode != 0):
        open('Fitness.txt', 'w').close()
        open('gn.txt', 'w').close()
        #frameRate(28800)
        #frameRate(180)
    else:
        frameRate(30)    
    
    
    
   
#define os controles para o modo manual
def keyPressed():
    if(key == 'w' or key == 'W'):
        car.setFowardTrue()
    if(key == 's' or key == 'S'):
        car.setBackTrue()
    if(key == 'a' or key == 'A'):
        car.setLeftTrue()
    if(key == 'd' or key == 'D'):
        car.setRightTrue()

#define os controles para o modo manual
def keyReleased():
    if(key == 'w' or key == 'W'):
        car.setFowardFalse()
    if(key == 's' or key == 'S'):
        car.setBackFalse()
    if(key == 'a' or key == 'A'):
        car.setLeftFalse()
    if(key == 'd' or key == 'D'):
        car.setRightFalse()
    
