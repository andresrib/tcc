import player

class navigator():
    def __init__(self, npc, desiredSpeed = 8, turningSpeed = 4, reverseDelay = 10, middleSensorDistance = 50, cornerSensorsDistance = 45):
        self.npc = npc
        self.desiredSpeed = desiredSpeed
        self.turningSpeed = turningSpeed
        self.reverseDelay = reverseDelay
        self.middleSensorDistance = middleSensorDistance
        self.cornerSensorsDistance = cornerSensorsDistance
        self.leftSensor = True
        self.centerSensor = True
        self.rightSensor = True
    def drawNpc(self):
        self.npc.drawPlayer()
        stroke(0,0,250)
        strokeWeight(3)
        point(self.npc.x + (self.cornerSensorsDistance-4)*cos(self.npc.theta - PI/8), self.npc.y + (self.cornerSensorsDistance-4)*sin(self.npc.theta - PI/8))
        point(self.npc.x + (self.middleSensorDistance-4)*cos(self.npc.theta), self.npc.y + (self.middleSensorDistance-4)*sin(self.npc.theta))
        point(self.npc.x + (self.cornerSensorsDistance-4)*cos(self.npc.theta + PI/8), self.npc.y + (self.cornerSensorsDistance-4)*sin(self.npc.theta + PI/8))
        
    
    def navigate(self):
        self.leftSensor = get(int(self.npc.x + self.cornerSensorsDistance*cos(self.npc.theta - PI/8)), int(self.npc.y + self.cornerSensorsDistance*sin(self.npc.theta - PI/8))) == -1
        #print(get(int(self.npc.x + self.cornerSensorsDistance*cos(self.npc.theta - PI/8)), int(self.npc.y + self.cornerSensorsDistance*sin(self.npc.theta - PI/8))))
        self.centerSensor = get(int(self.npc.x + self.middleSensorDistance*cos(self.npc.theta)), int(self.npc.y + self.middleSensorDistance*sin(self.npc.theta))) != -1
        #print(get(int(self.npc.x + self.middleSensorDistance*cos(self.npc.theta)), int(self.npc.y + self.middleSensorDistance*sin(self.npc.theta))))
        self.rightSensor = get(int(self.npc.x + self.cornerSensorsDistance*cos(self.npc.theta + PI/8)), int(self.npc.y + self.cornerSensorsDistance*sin(self.npc.theta + PI/8))) != -1
        if(self.leftSensor and self.centerSensor and self.rightSensor):
            if(self.npc.speed < self.desiredSpeed):
                self.npc.setBackFalse()
                self.npc.setFowardTrue()
            else:
                self.npc.setFowardFalse()
        else:
            self.npc.setFowardFalse()
        if(self.leftSensor and self.centerSensor and not self.rightSensor):
            self.npc.setLeftFalse()
            self.npc.setRightTrue()
        else:
            if(self.leftSensor and not self.centerSensor and not self.rightSensor):
                if(self.npc.speed > self.turningSpeed):
                    self.npc.setFowardFalse()
                    self.npc.setBackTrue()
                else:
                    self.npc.setBackFalse()
                self.npc.setLeftFalse()
                self.npc.setRightTrue()
            else:
                self.npc.setRightFalse()
        
        if(not self.leftSensor and self.centerSensor and self.rightSensor):
            self.npc.setRightFalse()
            self.npc.setLeftTrue()
        else:
            if(not self.leftSensor and self.centerSensor and self.rightSensor):
                if(self.npc.speed > self.turningSpeed):
                    self.npc.setFowardFalse()
                    self.npc.setBackTrue()
                else:
                    self.npc.setBackFalse()
                self.npc.setRightFalse()
                self.npc.setLeftTrue()
            else:
                self.npc.setLeftFalse()
        if(not self.leftSensor and not self.centerSensor and not self.rightSensor):
            self.npc.setFowardFalse()
            self.npc.setBackTrue()
        else:
            self.npc.setBackFalse()
        self.npc.accelerate()
