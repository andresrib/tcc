class player():
    def __init__(self, x = 400, y = 180, theta = (PI*2), speed = 0, acceleration = 3, desaceleration = -2, maxSpeed = 15, minSpeed = - 8, speedX = 0, speedY = 0, dTheta = PI/72.0, delay = 0):
        self.x = x
        
        self.y = y
        
        self.theta = theta
        
        self.speed = speed
        
        self.maxSpeed = maxSpeed
        
        self.acceleration = acceleration
        
        self.desaceleration = desaceleration
        
        self.maxSpeed = maxSpeed
        
        self.speedY = speedY
        
        self.speedX = speedX
        
        self.dTheta = dTheta
        
        self.delay = delay
                
    def accelerate(self, k):
        if k == "W" or k == "w":
            self.speed += self.acceleration
        if k == "S" or k == "s":
            self.speed += self.desaceleration
        if k == "A" or k == "a":
            self.theta += self.dTheta
        if k == "D" or k == "d":
            self.theta -= self.dTheta    
        self.speedX = self.speed*cos(self.theta)
        self.speedY = self.speed*sin(self.theta)
        
        
        
    def checkColision(self):
        if(get(self.x + self.speedX, self.y + self.speedY) == [255, 255, 255]):
            return False
        else:
            return True
        
    def drawPlayer(self):
        stroke(255, 0, 0)
        strokeWeight(20)
        #if()
        self.x += self.speedX
        self.y += self.speedY
        point(self.x, self.y )
        
        
    
