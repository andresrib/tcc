import player

class navigator():
    def __init__(self, npc, desiredSpeed , turningSpeed , startingReverseDelay , track, middleSensorDistance = 50, cornerSensorsDistance = 45, sideSensorsDistance = 60, previousTheta = PI, previousX = 0, previousY = 0, fitness = 0, laps = 0, middlePoint = False):
        self.npc = npc
        self.desiredSpeed = desiredSpeed
        self.turningSpeed = turningSpeed
        self.reverseDelay = startingReverseDelay
        self.startingReverseDelay = startingReverseDelay
        self.track = track
        self.middleSensorDistance = middleSensorDistance
        self.cornerSensorsDistance = cornerSensorsDistance
        self.sideSensorsDistance = sideSensorsDistance
        self.leftSideSensor = True
        self.leftSensor = True
        self.centerSensor = True
        self.rightSensor = True
        self.rightSideSensor = True
        self.previousTheta = previousTheta
        self.previousX = previousX
        self.previousY = previousY
        self.fitness = fitness
        self.laps = laps
        self.middlePoint = middlePoint
        
    def drawNpc(self):
        #desenha o carro
        self.npc.drawPlayer()
        stroke(0,0,250)
        strokeWeight(3)
        #desenha os sensores
        point(self.npc.x + (self.sideSensorsDistance-4)*cos(self.npc.theta - PI/2), self.npc.y + (self.sideSensorsDistance-4)*sin(self.npc.theta - PI/2))
        point(self.npc.x + (self.cornerSensorsDistance-4)*cos(self.npc.theta - PI/4), self.npc.y + (self.cornerSensorsDistance-4)*sin(self.npc.theta - PI/4))
        point(self.npc.x + (self.middleSensorDistance-4)*cos(self.npc.theta), self.npc.y + (self.middleSensorDistance-4)*sin(self.npc.theta))
        point(self.npc.x + (self.cornerSensorsDistance-4)*cos(self.npc.theta + PI/4), self.npc.y + (self.cornerSensorsDistance-4)*sin(self.npc.theta + PI/4))
        point(self.npc.x + (self.sideSensorsDistance-4)*cos(self.npc.theta + PI/2), self.npc.y + (self.sideSensorsDistance-4)*sin(self.npc.theta + PI/2))
    
    def trainNpc(self):
        self.npc.training()
    
    #verifica se o navegador passou pelo checkpoint e terminou a pista, no sentido horario
    def finishTrack(self):
        if(self.track == 0):
            if(self.previousX>450 and self.npc.x <= 450 and self.npc.y > 400 and self.npc.y < 500):
                self.middlePoint = True
                #exit()
            if(self.previousY>190 and self.npc.y <= 190 and self.npc.x > 400 and self.npc.x < 500 and self.middlePoint):
                self.laps = self.laps + 1
                self.middlePoint = False
                #exit()
        elif(self.track == 1):
            if(self.previousX>450 and self.npc.x <= 450 and self.npc.y > 350 and self.npc.y < 500):
                self.middlePoint = True
                #exit()
            if(0<self.previousX<390 and self.npc.x >= 390 and self.npc.y < 250 and self.middlePoint):
                self.laps = self.laps + 1
                self.middlePoint = False
                #exit()
        elif(self.track == 2):
            if(self.previousY>190 and self.npc.y <= 190 and self.npc.x > 400 and self.npc.x < 500):
                self.middlePoint = True
                #exit()
            if(self.previousY>210 and self.npc.y <= 210 and self.npc.x > 400 and self.npc.x < 500 and self.middlePoint):
                self.laps = self.laps + 1
                self.middlePoint = False
                #exit()
        if(self.fitness>1800 and self.laps == 0):
            self.laps = 1
        
    def navigate(self):
        #verifica a cor na posicao dos sensores
        leftSideSensorPixel = get(int(self.npc.x + (self.sideSensorsDistance)*cos(self.npc.theta - PI/2)), int(self.npc.y + (self.sideSensorsDistance)*sin(self.npc.theta - PI/2)))
        leftSensorPixel = get(int(self.npc.x + self.cornerSensorsDistance*cos(self.npc.theta - PI/4)), int(self.npc.y + self.cornerSensorsDistance*sin(self.npc.theta - PI/4)))
        centerSensorPixel = get(int(self.npc.x + self.middleSensorDistance*cos(self.npc.theta)), int(self.npc.y + self.middleSensorDistance*sin(self.npc.theta)))
        rightSensorPixel = get(int(self.npc.x + self.cornerSensorsDistance*cos(self.npc.theta + PI/4)), int(self.npc.y + self.cornerSensorsDistance*sin(self.npc.theta + PI/4)))
        rightSideSensorPixel = get(int(self.npc.x + (self.sideSensorsDistance)*cos(self.npc.theta + PI/2)), int(self.npc.y + (self.sideSensorsDistance)*sin(self.npc.theta + PI/2)))
        
        #caso os sensores estejam na pista, as variaveis recebem true
        self.leftSideSensor = leftSideSensorPixel != -1 and leftSideSensorPixel != 0
        self.leftSensor = leftSensorPixel != -1 and leftSensorPixel != 0
        self.centerSensor = centerSensorPixel != -1 and centerSensorPixel != 0
        self.rightSensor = rightSensorPixel != -1 and rightSensorPixel != 0
        self.rightSideSensor = rightSideSensorPixel != -1 and rightSideSensorPixel != 0
        #print(self.centerSensor)
        
        #caso os 3 sensores frontais estejam na pista, acelera
        if(self.leftSensor and self.centerSensor and self.rightSensor):
            if(self.npc.speed < self.desiredSpeed):
                self.npc.setBackFalse()
                self.npc.setFowardTrue()
            else:
                self.npc.setFowardFalse()
            """if(self.leftSideSensor and not self.rightSideSensor):
                self.npc.setLeftTrue()
            elif(not self.leftSideSensor and self.rightSideSensor):
                self.npc.setRightTrue()"""
        else:
            self.npc.setFowardFalse()
        
        
        #caso sensor frontal direito fora da pista, virar para esquerda
        if(self.leftSensor and self.centerSensor and not self.rightSensor):
            self.npc.setRightFalse()
            self.npc.setLeftTrue()
        else:
            #caso sensor frontal central fora da pista, vira a esquerda e desacelera para a turningSpeed ao mesmo tempo
            if(self.leftSensor and not self.centerSensor and not self.rightSensor):
                if(self.npc.speed > self.turningSpeed):
                    self.npc.setFowardFalse()
                    self.npc.setBackTrue()
                else:
                    self.npc.setBackFalse()
                self.npc.setRightFalse()
                self.npc.setLeftTrue()
            else:
                self.npc.setLeftFalse()
        
        
        #caso sensor frontal esquerdo fora da pista, virar para direita
        if(not self.leftSensor and self.centerSensor and self.rightSensor):
            self.npc.setLeftFalse()
            self.npc.setRightTrue()
        else:
            #caso sensor frontal central fora da pista, vira a direita e desacelera para a turningSpeed ao mesmo tempo
            if(not self.leftSensor and not self.centerSensor and self.rightSensor):
                if(self.npc.speed > self.turningSpeed):
                    self.npc.setFowardFalse()
                    self.npc.setBackTrue()
                else:
                    self.npc.setBackFalse()
                self.npc.setLeftFalse()
                self.npc.setRightTrue()
            else:
                self.npc.setRightFalse()
        
        
        #caso nenhum sensor frontal na pista, verifica os sensores laterais
        if(not self.leftSensor and not self.centerSensor and not self.rightSensor):
            self.npc.setFowardFalse()
            self.npc.setBackTrue()
            if(self.leftSideSensor and not self.rightSideSensor):
                self.npc.setLeftTrue()
            elif(not self.leftSideSensor and self.rightSideSensor):
                self.npc.setRightTrue()
            elif(self.npc.theta == self.previousTheta):
                self.npc.setLeftTrue()
        #else:
            #self.npc.setBackFalse()
           
        #caso apenas sensor frontal central fora da pista,verifica os sensores laterais 
        if(self.leftSensor and not self.centerSensor and self.rightSensor):
            if(self.leftSideSensor and not self.rightSideSensor):
                self.npc.setLeftTrue()
            elif(not self.leftSideSensor and self.rightSideSensor):
                self.npc.setRightTrue()
            else:
                self.npc.setFowardTrue()
         
        #caso a posicao do carro nao mude durante o tempo previsto no reverseDelay, comeca a dar re        
        if (self.previousX == self.npc.x and self.previousY == self.npc.y and self.npc.speed>-1):
            self.reverseDelay = self.reverseDelay - 1
            if(self.reverseDelay<1):
                self.npc.setFowardFalse()
                self.npc.setBackTrue()
                if(self.reverseDelay<-3):
                    self.reverseDelay = self.startingReverseDelay
        #salva o angulo atual do carro para futuras comparacoes
        self.previousTheta = self.npc.theta
        #verifica se terminou o percurso
        self.finishTrack()
        #if(self.laps==0):
        #    self.fitness = self.fitness + 1
        #print("fitness :" + str(self.fitness))
        self.previousX = self.npc.x
        self.previousY = self.npc.y
        self.npc.accelerate()
