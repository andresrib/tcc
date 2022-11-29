class player():
    def __init__(self, x , y , theta = (PI*2), speed = 0, acceleration = 2, desaceleration = -1, maxSpeed = 15, minSpeed = - 8, speedX = 0, speedY = 0, dTheta = PI/72.0, delay = 0, right = False, left = False, foward = False, back = False):
        self.x = x
        
        self.y = y
        
        self.theta = theta
        
        self.speed = speed
        
        self.maxSpeed = maxSpeed
        
        self.acceleration = acceleration
        
        self.desaceleration = desaceleration
        
        self.maxSpeed = maxSpeed
        
        self.minSpeed = minSpeed
        
        self.speedY = speedY
        
        self.speedX = speedX
        
        self.dTheta = dTheta
        
        self.delay = delay
        
        self.left = left
        
        self.right = right
        
        self.foward = foward
        
        self.back = back
        
        self.colisions = 0
                        
    
    def accelerate(self):
        #aumenta a speed pelo valor de acceleration sem ultrapassar a maxspeed
        if self.foward == True:
            if(self.speed + self.acceleration <= self.maxSpeed):
                if(self.delay <= 0):
                    self.speed += self.acceleration
                    self.delay = 5
            else:
                self.speed = self.maxSpeed
        #diminue a speed pelo valor de desaceleration sem ultrapassar a minSpeed
        if self.back == True:
            if(self.speed + self.desaceleration >= self.minSpeed):
                if(self.delay <= 0):
                    self.speed += self.desaceleration
                    self.delay = 5
            else:
                self.speed = self.minSpeed
        #subtrai dTheta do angulo do carro, caso a velocidade seja maior que 8, subtrai 2dTheta
        if self.left == True:
            self.theta -= self.dTheta
            if self.speed > 8:
                self.theta -= self.dTheta
        #soma dTheta do angulo do carro, caso a velocidade seja maior que 8, soma 2dTheta
        if self.right == True:
            self.theta += self.dTheta
            if self.speed > 8:
                self.theta += self.dTheta
        #if self.speed > 2 and self.delay%30 == 0:
        #    self.speed = self.speed - 1
        #delay utilizado para que a aceleracao e desaceleracao nao sejam rapidas demais
        self.delay = self.delay - 1
        self.speedX = self.speed*cos(self.theta)
        self.speedY = self.speed*sin(self.theta)        
        
    #checa a colisao do carro    
    def checkColision(self):
        #print("cor" + str(get(int(self.x), int(self.y))))
        if(get(int(self.x + self.speedX), int(self.y + self.speedY)) == -1 or get(int(self.x + self.speedX), int(self.y + self.speedY)) == 0):
            if(self.speed != 0):
                self.colisions += 1
                #toogle bounceback
                self.speed = (self.speed - (abs(self.speed)/self.speed)) * -1
                #self.speed = 0
            return False
        else:
            return True
     
    #atualiza a posicao e desenha o carro    
    def drawPlayer(self):
        stroke(255, 0, 0)
        strokeWeight(5)
        if(self.checkColision()):
            self.x += self.speedX
            self.y += self.speedY
        #point(self.x, self.y )
        triangle(self.x + 10*cos(self.theta), self.y + 10*sin(self.theta), self.x + 5*cos(self.theta - PI/2), self.y + 5*sin(self.theta - PI/2), self.x + 5*cos(self.theta + PI/2), self.y + 5*sin(self.theta + PI/2))
        
    def setRightTrue(self):
        self.right = True
        
    def setRightFalse(self):
        self.right = False
        
    def setLeftTrue(self):
        self.left = True
        
    def setLeftFalse(self):
        self.left = False
        
    def setFowardTrue(self):
        self.foward = True
        
    def setFowardFalse(self):
        self.foward = False
        
    def setBackTrue(self):
        self.back = True
        
    def setBackFalse(self):
        self.back = False
    
    #atualiza a posicao sem desenhar o carro
    def training(self):
        if(self.checkColision()):
            self.x += self.speedX
            self.y += self.speedY
        
       
        
    
