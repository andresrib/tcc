import os
import time
import random
from importlib import import_module
import player, track, navigator

#escolha da pista, entre 0 1 e 2
nPista=0
#modo de treino, sendo 0 nao treinando, 1 treinando visualmente de forma lenta e 2 sendo o treino nao visual rapido
trainingMode = 2

colisionWeight = 10

geracoes = 1000

pista = []

def setup():
    global car, ai, loops, candidate_number, tester, initial_x, initial_y, best, goal
    goal = 2
    size(1200, 700)
    track.inicializa_pista(pista, nPista)
    ai = []
    #define as posicoes iniciais do carro de acordo com a pista
    if(nPista == 0):
        initial_x = 450
        initial_y = 180
    elif(nPista == 1):
        initial_x = 400
        initial_y = 180
    elif(nPista == 2):
        initial_x = 450
        initial_y = 180
    car = player.player(initial_x, initial_y)
    #inicia um navegador de teste para o modo de treino 0 0 14 52.0 72.0 57.0, 1 2 14 50 72.0 61.0
    #3 5 14 61.0 74.0 40
    tester = navigator.navigator(car, 11, 8, 29, nPista, 63, 56, 47)
    #inicia os 30 navegadores iniciais para o treino
    for i in range(60):
        ai.append(navigator.navigator(player.player(450, 180), random.randint(1, 15), random.randint(1, 15), random.randint(1, 60), nPista, random.randint(30, 90), random.randint(30, 90), random.randint(30, 90)))
    #inicia um placeholder para o melhor da geracao
    best = navigator.navigator(player.player(450, 180), random.randint(1, 15), random.randint(1, 15), random.randint(1, 60), nPista, random.randint(30, 90), random.randint(30, 90), random.randint(30, 90))#[0, 0, 0, 1802]
    best.fitness = 1000000000
    background(255)
    track.desenha(pista, nPista)
    
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
    global pista, nPista, player, trainingMode, loops, car, ai, candidate_number, initial_x, initial_y, best, goal
    
    if trainingMode == 1:
        track.desenha(pista, nPista)
        ai[candidate_number].navigate()
        #ai[candidate_number].trainNpc()
        ai[candidate_number].drawNpc()
        #aumenta o fitness a cada frame
        if ai[candidate_number].laps < goal:
            ai[candidate_number].fitness = ai[candidate_number].fitness+1
        #confere se a geracao chegou ao final
        elif candidate_number == 29:
            
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
                    newAi.append(navigator.navigator(player.player(initial_x, initial_y), int(dSpeed), int(tSpeed), int(rDelay), nPista))
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
        while(ai[0].laps < goal or ai[1].laps < goal or ai[2].laps < goal or ai[3].laps < goal or ai[4].laps < goal or ai[5].laps < goal or ai[6].laps < goal or ai[7].laps < goal or ai[8].laps < goal or ai[9].laps < goal or ai[10].laps < goal 
                  or ai[11].laps < goal or ai[12].laps < goal or ai[13].laps < goal or ai[14].laps < goal or ai[15].laps < goal or ai[16].laps < goal or ai[17].laps < goal or ai[18].laps < goal or ai[19].laps < goal or ai[20].laps < goal 
                      or ai[21].laps < goal or  ai[22].laps < goal or ai[23].laps < goal or ai[24].laps < goal or ai[25].laps < goal or ai[26].laps < goal or ai[27].laps < goal or ai[28].laps < goal or ai[29].laps < goal or ai[30].laps < goal or ai[31].laps < goal or ai[32].laps < goal or ai[33].laps < goal or ai[34].laps < goal or ai[35].laps < goal or ai[36].laps < goal or ai[37].laps < goal or ai[38].laps < goal or ai[39].laps < goal or ai[40].laps < goal 
                  or ai[41].laps < goal or ai[42].laps < goal or ai[43].laps < goal or ai[44].laps < goal or ai[45].laps < goal or ai[46].laps < goal or ai[47].laps < goal or ai[48].laps < goal or ai[49].laps < goal or ai[50].laps < goal 
                      or ai[51].laps < goal or  ai[52].laps < goal or ai[53].laps < goal or ai[54].laps < goal or ai[55].laps < goal or ai[56].laps < goal or ai[57].laps < goal or ai[58].laps < goal or ai[59].laps < goal):
            for candidate in ai:
                if candidate.laps < goal:
                    candidate.fitness = candidate.fitness+1
                candidate.navigate()
                candidate.trainNpc()
        #funcionamento igual ao training mode 1 exceto que nao reseta o candidate_number para 0, quando refatorar o código irei transformar em uma funcao para evitar redundancia       
        with open("Fitness.txt", "a") as fit:
            average = 0
            for candidate in ai:
                candidate.fitness += candidate.npc.colisions * colisionWeight
                average += candidate.fitness
                if(candidate.fitness <= best.fitness):
                    best = candidate#[candidate.desiredSpeed, candidate.turningSpeed, candidate.startingReverseDelay, candidate.fitness]
            #print(best)
            fit.write(str(best.fitness) + "\t"  + str(average/30) + "\n")
            newAi = []
            with open("gn.txt", "a") as gn:
                for candidate in ai:
                    gn.write(str(candidate.desiredSpeed) + " " + str(candidate.turningSpeed) + " " + str(candidate.startingReverseDelay) + " " + str(candidate.middleSensorDistance) + " " + str(candidate.cornerSensorsDistance) + " " + str(candidate.sideSensorsDistance) + " " + str(candidate.fitness) + "\n")
                    if (candidate != best):#candidate.desiredSpeed != best[0] or candidate.turningSpeed != best[1] or candidate.startingReverseDelay != best[2]):
                        percentual = random.randint(2, 12)/10.0
                        
                        dSpeed = candidate.desiredSpeed + ( - candidate.desiredSpeed + best.desiredSpeed) * percentual
                        percentual = random.randint(2, 12)/10.0
                        tSpeed = candidate.turningSpeed + ( - candidate.turningSpeed + best.turningSpeed) * percentual
                        percentual = random.randint(2, 12)/10.0
                        rDelay = candidate.reverseDelay + ( - candidate.reverseDelay + best.reverseDelay) * percentual
                        percentual = random.randint(2, 12)/10.0
                        msDistance = candidate.middleSensorDistance + ( - candidate.middleSensorDistance + best.middleSensorDistance) * percentual
                        percentual = random.randint(2, 12)/10.0
                        csDistance = candidate.cornerSensorsDistance + ( - candidate.cornerSensorsDistance + best.cornerSensorsDistance) * percentual
                        percentual = random.randint(2, 12)/10.0
                        ssDistance = candidate.sideSensorsDistance + ( - candidate.sideSensorsDistance + best.sideSensorsDistance) * percentual
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
                    else:
                        dSpeed = best.desiredSpeed
                        tSpeed = best.turningSpeed
                        rDelay = best.startingReverseDelay
                        msDistance =  best.middleSensorDistance
                        csDistance = best.cornerSensorsDistance
                        ssDistance = best.sideSensorsDistance
                    newAi.append(navigator.navigator(player.player(initial_x, initial_y), int(dSpeed), int(tSpeed), int(rDelay), nPista, msDistance, csDistance, ssDistance))
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
                            if nPista == 0:
                                with open ("resultados/testeCross_fitness_pista0.txt", "a") as r:
                                    r.write("melhor e media\n\n")
                                    r.write(results)
                                    r.write("\n\n")
                                with open ("resultados/testeCross_gn_pista0.txt", "a") as gen:
                                    gen.write("teste\n\n")
                                    gen.write(generations)
                                    gen.write("\n")
                            if nPista == 1:
                                with open ("resultados/testeCross_fitness_pista1.txt", "a") as r:
                                    r.write("melhor e media\n")
                                    r.write(results)
                                    r.write("\n")
                                with open ("resultados/testeCross_gn_pista1.txt", "a") as gen:
                                    gen.write("teste\n\n")
                                    gen.write(generations)
                                    gen.write("\n")
                            if nPista == 2:
                                with open ("resultados/testeCross_fitness_pista2.txt", "a") as r:
                                    r.write("melhor e media\n\n")
                                    r.write(results)
                                    r.write("\n\n")
                                with open ("resultados/testeCross_gn_pista2.txt", "a") as gen:
                                    gen.write("teste\n")
                                    gen.write(generations)
                                    gen.write("\n\n")
                    exit()
                loops = loops + 1
    #testa todas as possibilidades
    elif(trainingMode == 3):
        ai = []
        for sp in range(1, 16):
            for tsp in range(1, 16):
                for rd in range(1, 61):
                    ai.append(navigator.navigator(player.player(initial_x, initial_y), sp, tsp, rd, nPista))
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
        track.desenha(pista, nPista)
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
    
