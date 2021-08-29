import pygame
from pygame.math import Vector2
import os
import random
import neat
import time

pygame.init()
pygame.font.init()

SNAKE_BODY = pygame.transform.scale(pygame.image.load(os.path.join("E:\AAAACODE_TODO\Redes Neuronales\SNAKE-AI\images\snakebody.png")),(30,30))
APPLE = pygame.transform.scale(pygame.image.load(os.path.join("E:\AAAACODE_TODO\Redes Neuronales\SNAKE-AI\images\manzana.png")),(30,30))
EAT_SOUND = pygame.mixer.Sound("coin.wav")#os.path.join("E:\AAAACODE_TODO\Redes Neuronales\SNAKE-AI\images\sounds\coin.wav"))
SNAKE_HEAD = []
for x in range(1,5):
    SNAKE_HEAD += [pygame.transform.scale(pygame.image.load(os.path.join("E:\AAAACODE_TODO\Redes Neuronales\SNAKE-AI\images\SnakeHead"+str(x)+".png")),(30,30))]
CELL_SIZE = APPLE.get_height()

ALTO = 810
ANCHO = 810
#HIGHEST RANGE = 81 px
WIN = pygame.display.set_mode((ALTO,ANCHO))
STAT_FONT = pygame.font.SysFont("Russo One",30)




class Snake:
    def __init__(self):

        self.body = [Vector2(10,10),Vector2(10,11),Vector2(10,12)]
        self.direction = Vector2(0,-1)
        self.add = False
        self.distance_to_fruit = Vector2(0,0)
        self.distance_to_wall = Vector2(0,0)



    def draw(self):
        for block in self.body:
            WIN.blit(SNAKE_BODY,(block.x*CELL_SIZE,block.y*CELL_SIZE))
        if self.direction == Vector2(0,-1):#UP
            WIN.blit(SNAKE_HEAD[0],(self.body[0].x*CELL_SIZE,self.body[0].y*CELL_SIZE))
        if self.direction == Vector2(0,1):#DWON
            WIN.blit(SNAKE_HEAD[2],(self.body[0].x*CELL_SIZE,self.body[0].y*CELL_SIZE))
        if self.direction == Vector2(1,0):#RIGHT
            WIN.blit(SNAKE_HEAD[1],(self.body[0].x*CELL_SIZE,self.body[0].y*CELL_SIZE))
        if self.direction == Vector2(-1,0):#lEFT
            WIN.blit(SNAKE_HEAD[3],(self.body[0].x*CELL_SIZE,self.body[0].y*CELL_SIZE))

    def move(self):
        
        if self.add == True:
            body_copy = self.body[:]#para omitir el ultimo elemento
            body_copy.insert(0,body_copy[0]+self.direction)#insert le anade una nueva posicion a la lista que seria la 0. mueve la antigua 0 a la 1 y la 1 a la 2
            self.body = body_copy[:]
            self.add = False
        else:
            body_copy = self.body[:-1]#para omitir el ultimo elemento
            body_copy.insert(0,body_copy[0]+self.direction)#insert le anade una nueva posicion a la lista que seria la 0. mueve la antigua 0 a la 1 y la 1 a la 2
            self.body = body_copy[:]
        #print(self.body)
    def vision(self,apple):
        
        if self.direction == Vector2(0,-1):#UP
            self.distance_to_fruit = Vector2(0,apple.pos.y-self.body[0].y*CELL_SIZE)
            self.distance_to_wall = Vector2(0,0-self.body[0].y*CELL_SIZE)

        elif self.direction == Vector2(0,1):#DOWN
            self.distance_to_fruit = Vector2(0,apple.pos.y-self.body[0].y*CELL_SIZE)
            self.distance_to_wall = Vector2(0,ALTO/CELL_SIZE-self.body[0].y*CELL_SIZE)

        elif self.direction == Vector2(1,0):#RIGHT
            self.distance_to_fruit = Vector2(apple.pos.x-self.body[0].x*CELL_SIZE,0)
            self.distance_to_wall = Vector2(ANCHO/CELL_SIZE-self.body[0].y*CELL_SIZE,0)

        elif self.direction == Vector2(-1,0):#LEFT
            self.distance_to_fruit = Vector2(apple.pos.x-self.body[0].x*CELL_SIZE,0)
            self.distance_to_wall = Vector2(0-self.body[0].y*CELL_SIZE,0)
        #print (self.distance_to_wall,self.distance_to_fruit)


    def move_up(self):
        self.direction = Vector2(0,-1)     
    
    def move_down(self):
        self.direction = Vector2(0,1) 

    def move_right(self):
        self.direction = Vector2(1,0) 

    def move_left(self):
        self.direction = Vector2(-1,0) 

    def die(self):
        if self.body[0].x*CELL_SIZE >= ANCHO or self.body[0].y*CELL_SIZE >= ALTO or self.body[0].x*CELL_SIZE < -CELL_SIZE*0.3 or self.body[0].y*CELL_SIZE < -CELL_SIZE*0.3:
            return True
                
        for block in self.body[1:]:
            if self.body[0] == block:
                return True

    def get_mask(self):
        return pygame.mask.from_surface(SNAKE_BODY)

class Apple:
    def __init__(self):
        self.generate()
    
    def draw(self):
        WIN.blit(APPLE,(self.pos.x,self.pos.y))
        #print(self.pos,'aa')
    def generate(self):
        self.x = random.randrange(0,ANCHO-CELL_SIZE)
        self.y = random.randrange(0,ALTO-CELL_SIZE)
        self.pos = Vector2(self.x,self.y)

    def check_collision(self,snake):
        #print(snake.body[0])
        snake_mask = snake.get_mask()
        
        apple_mask = pygame.mask.from_surface(APPLE)
        apple_offset = (round(self.pos.x - snake.body[0].x*CELL_SIZE ),round(self.pos.y - snake.body[0].y*CELL_SIZE))
        
        collision_point = snake_mask.overlap(apple_mask,apple_offset)
        #print(self.timer)
        if collision_point:
            
            self.generate()
            #print(self.score)
            snake.add = True
            return True




def points():

    snake = Snake()
    apple = Apple()
    score = 0
    
    clock = pygame.time.Clock() 


    while True:
        clock.tick(30)

        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()


            if event.type == pygame.KEYDOWN and snake.direction.y != 1:
                if event.key == pygame.K_UP:
                        snake.move_up()
            if event.type == pygame.KEYDOWN and snake.direction.y != -1:
                if event.key == pygame.K_DOWN:
                        snake.move_down()
                        
            if event.type == pygame.KEYDOWN and snake.direction.x != -1:  
                if event.key == pygame.K_RIGHT:
                        snake.move_right()
            if event.type == pygame.KEYDOWN and snake.direction.x != 1:
                if event.key == pygame.K_LEFT:
                        snake.move_left()
        


        if apple.check_collision(snake):
            score += 1

        WIN.fill((175,215,70))

            
        snake.draw()
        apple.draw()
        snake.move()
        #snake.die()
        if snake.die():
           time.sleep(0.5)
           points()
        #p#rint(score)
        text = STAT_FONT.render("SCORE: {}".format(str(score)),1,(255,255,255))
        WIN.blit(text,(ANCHO-text.get_width()-10,10)) #win.blit = win.draw
        pygame.display.update()



points()