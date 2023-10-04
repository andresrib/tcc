import os
import time
import random
from importlib import import_module
import player, track, navigator


nPista=2
#modo de treino, sendo 0 nao treinando, 1 treinando visualmente de forma lenta e 2 sendo o treino nao visual rapido
trainingMode = 0

colisionWeight = 0

geracoes = 50

populacao = 30

runTimes = 30

mutation = 5

trainSensors = False

newCross = False

myCross = False

goal = 1

resultFileName = "rerrodar_1Lap_initial"

pista = []


#escolha das pista, entre 0 1 e 2
tracks = [0, 1, 2]

ran = 0

running = False

restartCoolDown = False

first = True

recordCounter = 0

start = False

def setup():
    global car, ai, loops, candidate_number, tester, initial_x, initial_y, best, goal, tracks, nPista, lastGenBest, recordNavigators
    
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
    recordNavigators = [[navigator.navigator(player.player(initial_x, initial_y), 9, 5, 36, tracks[nPista], 59, 64), 1], 
                     [navigator.navigator(player.player(initial_x, initial_y), random.randint(1, 15), random.randint(1, 15), random.randint(1, 60), tracks[nPista], random.randint(30, 90), random.randint(30, 90)), 10],
                      [navigator.navigator(player.player(initial_x, initial_y), random.randint(1, 15), random.randint(1, 15), random.randint(1, 60), tracks[nPista], random.randint(30, 90), random.randint(30, 90)), 25],
                       [navigator.navigator(player.player(initial_x, initial_y), random.randint(1, 15), random.randint(1, 15), random.randint(1, 60), tracks[nPista], random.randint(30, 90), random.randint(30, 90)), 50]]

    #inicia um navegador de teste para o modo de treino 0 0 14 52.0 72.0 57.0, 1 2 14 50 72.0 61.0
    #3 5 14 61.0 74.0 40
    tester = navigator.navigator(car, 11, 8, 29, tracks[nPista], 63, 56, 47)
    #inicia os 30 navegadores iniciais para o treino
    if trainSensors:
        for i in range(populacao):
            ai.append(navigator.navigator(player.player(initial_x, initial_y), random.randint(1, 15), random.randint(1, 15), random.randint(1, 60), tracks[nPista], random.randint(30, 90), random.randint(30, 90), random.randint(30, 90)))
    else:
        for i in range(populacao):
            ai.append(navigator.navigator(player.player(initial_x, initial_y), random.randint(1, 15), random.randint(1, 15), random.randint(1, 60), tracks[nPista]))
    
    #inicia um placeholder para o melhor da geracao
    best = navigator.navigator(player.player(initial_x, initial_y), random.randint(1, 15), random.randint(1, 15), random.randint(1, 60), tracks[nPista], random.randint(30, 90), random.randint(30, 90), random.randint(30, 90))#[0, 0, 0, 1802]
    best.fitness = 1000000000
    lastGenBest = navigator.navigator(player.player(initial_x, initial_y), random.randint(1, 15), random.randint(1, 15), random.randint(1, 60), tracks[nPista], random.randint(30, 90), random.randint(30, 90), random.randint(30, 90))
    lastGenBest.fitness = 1000000000
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
    global pista, nPista, player, trainingMode, loops, car, ai, candidate_number, initial_x, initial_y, best, goal, running, tracks, lastGenBest, restartCoolDown, printar, recordNavigators, recordCounter, start
    
    
    
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
            crossover()
            candidate_number = 0
            '''with open("Fitness.txt", "a") as fit:
                average = 0
                for candidate in ai:
                    average += candidate.fitness
                    #compara o fitness do melhor com todos da geracao
                    if(candidate.fitness <= best.fitness):
                        #substitui o melhor
                        best = candidate
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
                candidate_number = 0'''
                
        else:
            candidate_number = candidate_number+1
            
            
            
    elif(trainingMode == 2):
        #testa todos os candidatos ao mesmo tempo para melhor otimizacao
        
        running = False
        while( not running):
            running = True
            for candidate in ai:
                if candidate != lastGenBest:
                    if candidate.laps < goal:
                        candidate.fitness = candidate.fitness+1
                    candidate.navigate()
                    candidate.trainNpc()
                running = running and (candidate.laps >= goal) 
        #funcionamento igual ao training mode 1 exceto que nao reseta o candidate_number para 0, quando refatorar o código irei transformar em uma funcao para evitar redundancia       
        with open("Fitness.txt", "a") as fit:
            average = 0
            for candidate in ai:
                if candidate != lastGenBest:
                    candidate.fitness += candidate.npc.colisions * colisionWeight
                average += candidate.fitness
                if(candidate.fitness <= best.fitness):
                    #print(str(candidate.fitness) + "/" + str(best.fitness))
                    best = candidate
            #print(best.fitness)
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
                    best = candidate
            #print(best)
            fit.write(str(best.fitness) + "\t"  + str(average/30) + "\n")
        with open("resultados/todos_gn_pista2.txt", "w") as gn:
                for candidate in ai:
                    gn.write(str(candidate.desiredSpeed) + " " + str(candidate.turningSpeed) + " " + str(candidate.startingReverseDelay) + " " + str(candidate.fitness) + "\n")
        exit()

    #recording mode
    elif trainingMode == 4:
        if start:
            background(255)
            track.desenha(pista, tracks[nPista])
            recordNavigators[recordCounter][0].navigate()
            fill(150,0,0)
            textSize(50)
            text("geracao: " + str(recordNavigators[recordCounter][1]), 10, 60)
            fill(255)
            strokeWeight(10)
            stroke(0, 0, 255)
            recordNavigators[recordCounter][0].drawNpc()   
            if recordNavigators[recordCounter][0].laps < goal:
                recordNavigators[recordCounter][0].fitness += 1
            else:
                recordCounter += 1
                if recordCounter >= len(recordNavigators):
                    start = False
            
    #training mode 0, modo de controle manual           
    else:
        background(255)
        car.accelerate()
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
        car.drawPlayer()
        #tester.drawNpc()
    
    if trainingMode == 1 or trainingMode ==2:
        if ran < runTimes and loops > geracoes:
            restart()
            return()
        elif ran >= runTimes:
            exit()
#crossover
def crossover():
    global loops, ai, nPista, ran, runTimes, lastGenBest, first, trainSensors, mutation
    newAi = []
    with open("gn.txt", "a") as gn:
        for candidate in ai:
            if trainSensors:
                gn.write(str(candidate.desiredSpeed) + " " + str(candidate.turningSpeed) + " " + str(candidate.startingReverseDelay) + " " + str(candidate.middleSensorDistance) + " " + str(candidate.cornerSensorsDistance) + " " + str(candidate.sideSensorsDistance) + " " + str(candidate.fitness) + "\n")
            else:
                gn.write(str(candidate.desiredSpeed) + " " + str(candidate.turningSpeed) + " " + str(candidate.startingReverseDelay) + " " + str(candidate.fitness) + "\n")
            if candidate != best:#(candidate.desiredSpeed != best.desiredSpeed or candidate.turningSpeed != best.turningSpeed or candidate.startingReverseDelay != best.startingReverseDelay or candidate.middleSensorDistance != best.middleSensorDistance or candidate.cornerSensorsDistance != best.cornerSensorsDistance or candidate.middleSensorDistance != best.middleSensorDistance or candidate.sideSensorsDistance != best.sideSensorsDistance):
                
                if newCross:
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
                    rDelay = candidate.startingReverseDelay + ( - candidate.startingReverseDelay + best.startingReverseDelay) * percentual
                    if rDelay < 1:
                        rDelay = 1
                    if rDelay > 60:
                        rDelay = 60
                
                elif myCross:
                    percentual = random.randint(8, 12)/10.0
                    dSpeed = (candidate.desiredSpeed + best.desiredSpeed * percentual)//2
                    if dSpeed < 1:
                        dSpeed = 1
                    if dSpeed > 15:
                        dSpeed = 15
                    
                    percentual = random.randint(8, 12)/10.0
                    tSpeed = (candidate.turningSpeed + best.turningSpeed * percentual)//2
                    if tSpeed < 1:
                        tSpeed = 1
                    if tSpeed > 15:
                        tSpeed = 15
                    
                    percentual = random.randint(8, 12)/10.0
                    rDelay = (candidate.startingReverseDelay + best.startingReverseDelay * percentual)//2
                    if tSpeed < 1:
                        tSpeed = 1
                    if tSpeed > 15:
                        tSpeed = 15
                    
                else:
                    dSpeed = (candidate.desiredSpeed + best.desiredSpeed)/2
                    if dSpeed < 1:
                        dSpeed = 1
                    if dSpeed > 15:
                        dSpeed = 15
                        
                    tSpeed = (candidate.turningSpeed + best.turningSpeed)/2
                    if tSpeed < 1:
                        tSpeed = 1
                    if tSpeed > 15:
                        tSpeed = 15
                        
                    rDelay = (candidate.startingReverseDelay + best.startingReverseDelay)/2
                    if rDelay < 1:
                        rDelay = 1
                    if rDelay > 60:
                        rDelay = 60
                                    
                
                
                    
                if(random.randint(1, 100) <= mutation):
                    dSpeed = random.randint(1,15)
                if(random.randint(1, 100) <= mutation):
                    tSpeed = random.randint(1,15)
                if(random.randint(1, 100) <= mutation):
                    rDelay = random.randint(1,60)
                    
                
                if trainSensors:
                    if newCross:    
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
                    elif myCross:
                        percentual = random.randint(8, 12)/10.0
                        msDistance = (candidate.middleSensorDistance + best.middleSensorDistance * percentual)//2
                        
                        percentual = random.randint(8, 12)/10.0                        
                        csDistance = (candidate.cornerSensorsDistance + best.cornerSensorsDistance * percentual)//2
                        
                        percentual = random.randint(8, 12)/10.0
                        ssDistance = (candidate.sideSensorsDistance + best.sideSensorsDistance * percentual)//2
                        
                    else:
                        msDistance = (candidate.middleSensorDistance + best.middleSensorDistance)/2
                        if msDistance < 30:
                            msDistance = 30
                        if msDistance > 90:
                            msDistance = 90
                            

                        csDistance = (candidate.cornerSensorsDistance + best.cornerSensorsDistance)/2
                        if csDistance < 30:
                            csDistance = 30
                        if csDistance > 90:
                            csDistance = 90
                        
                        
                        ssDistance = (candidate.sideSensorsDistance + best.sideSensorsDistance) * percentual
                        if ssDistance < 30:
                            ssDistance = 30
                        if ssDistance > 90:
                            ssDistance = 90
                        
                                    
                    if(random.randint(1, 100) <= mutation):
                        msDistance = random.randint(30,90)
                    if(random.randint(1, 100) <= mutation):
                        csDistance = random.randint(30,90)
                    if(random.randint(1, 100) <= mutation):
                        ssDistance = random.randint(30,90)     
                    newAi.append(navigator.navigator(player.player(initial_x, initial_y), int(dSpeed), int(tSpeed), int(rDelay), tracks[nPista], int(msDistance), int(csDistance), int(ssDistance)))
                else:
                    newAi.append(navigator.navigator(player.player(initial_x, initial_y), int(dSpeed), int(tSpeed), int(rDelay), tracks[nPista]))  
            else:
                newAi.append(best)
                lastGenBest = best
                #temp = navigator.navigator(player.player(initial_x, initial_y), int(dSpeed), int(tSpeed), int(rDelay), tracks[nPista], int(msDistance), int(csDistance), int(ssDistance))
                #temp.fitness = best.fitness
            gn.write("\n")
        gn.write("\n/\n")
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
                        with open ("resultados/" + resultFileName + "_fitness_pista0.txt", "a") as r:
                            r.write("melhor e media\n\n")
                            r.write(results)
                            r.write("\n")
                        with open ("resultados/" + resultFileName + "_gn_pista0.txt", "a") as gen:
                            gen.write("teste\n\n")
                            gen.write(generations)
                            gen.write("\n/\n")
                    if tracks[nPista] == 1:
                        with open ("resultados/" + resultFileName + "_fitness_pista1.txt", "a") as r:
                            r.write("melhor e media\n")
                            r.write(results)
                            r.write("\n")
                        with open ("resultados/" + resultFileName + "_gn_pista1.txt", "a") as gen:
                            gen.write("teste\n\n")
                            gen.write(generations)
                            gen.write("\n/\n")
                    if tracks[nPista] == 2:
                        with open ("resultados/" + resultFileName + "_fitness_pista2.txt", "a") as r:
                            r.write("melhor e media\n\n")
                            r.write(results)
                            r.write("\n")
                        with open ("resultados/" + resultFileName + "_gn_pista2.txt", "a") as gen:
                            gen.write("teste\n")
                            gen.write(generations)
                            gen.write("\n/\n")
            ran = ran + 1
        loops = loops + 1    
        return()
        
def restart():
    global car, ai, loops, candidate_number, tester, initial_x, initial_y, best, goal, tracks, nPista, restartCoolDown, newAi
    newAi = []
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
    if trainSensors:
        for i in range(populacao):
            ai.append(navigator.navigator(player.player(initial_x, initial_y), random.randint(1, 15), random.randint(1, 15), random.randint(1, 60), tracks[nPista], random.randint(30, 90), random.randint(30, 90), random.randint(30, 90)))
    else:
        for i in range(populacao):
            ai.append(navigator.navigator(player.player(initial_x, initial_y), random.randint(1, 15), random.randint(1, 15), random.randint(1, 60), tracks[nPista]))#inicia um placeholder para o melhor da geracao
    #best = navigator.navigator(player.player(initial_x, initial_y), random.randint(1, 15), random.randint(1, 15), random.randint(1, 60), tracks[nPista], random.randint(30, 90), random.randint(30, 90), random.randint(30, 90))
    best.fitness = 1000000000
    loops = 0
    candidate_number = 0
    open('Fitness.txt', 'w').close()
    open('gn.txt', 'w').close()
    restartCoolDown = True
    #print("restart")
    #for candidate in ai:
        #print(candidate.desiredSpeed)

  
    
    
    
   
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
    global start, car
    if(key == 'w' or key == 'W'):
        car.setFowardFalse()
        start = True
    if(key == 's' or key == 'S'):
        car.setBackFalse()
    if(key == 'a' or key == 'A'):
        car.setLeftFalse()
    if(key == 'd' or key == 'D'):
        car.setRightFalse()
    
