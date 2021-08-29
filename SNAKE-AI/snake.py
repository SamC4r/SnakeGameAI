import pygame
from pygame.math import Vector2
import os
import random
import neat
import math

pygame.init()
pygame.font.init()

SNAKE_BODY = pygame.transform.scale(pygame.image.load(os.path.join("E:\AAAACODE_TODO\Redes Neuronales\SNAKE-AI\images\snakebody.png")),(30,30))
APPLE = pygame.transform.scale(pygame.image.load(os.path.join("E:\AAAACODE_TODO\Redes Neuronales\SNAKE-AI\images\manzana.png")),(30,30))
SNAKE_HEAD = [pygame.image.load(os.path.join("E:\AAAACODE_TODO\Redes Neuronales\SNAKE-AI\images","SnakeHead"+str(x)+".png"))for x in range(1,5)]
EAT_SOUND = pygame.mixer.Sound("E:\AAAACODE_TODO\Redes Neuronales\SNAKE-AI\coin.wav")#os.path.join("E:\AAAACODE_TODO\Redes Neuronales\SNAKE-AI\images\sounds\coin.wav"))

CELL_SIZE = APPLE.get_height()

ALTO = 810
ANCHO = 810
#HIGHEST RANGE = 81 px
WIN = pygame.display.set_mode((ALTO,ANCHO))
STAT_FONT = pygame.font.SysFont("Russo One",30)
fast_mode = True




class Snake:
    def __init__(self):
        self.body = [Vector2(10,10),Vector2(10,11),Vector2(10,12)]
        self.direction = Vector2(0,0)
        self.add = False
        self.distance_to_fruit = 0
        self.distance_to_wall = Vector2(0,0)
        self.distance_to_wall_up = 0
        self.distance_to_wall_down = 0
        self.distance_to_wall_left = 0
        self.distance_to_wall_right = 0
        self.distance_to_body = Vector2(0,0)



    def draw(self):
        
        for block in self.body[1:]:
            WIN.blit(SNAKE_BODY,(block.x*CELL_SIZE,block.y*CELL_SIZE))
        
        if self.direction == Vector2(0,-1):#UP
            WIN.blit(SNAKE_HEAD[0],(self.body[0].x*CELL_SIZE,self.body[0].y*CELL_SIZE))
        if self.direction == Vector2(0,1):#DWON
            WIN.blit(SNAKE_HEAD[2],(self.body[0].x*CELL_SIZE,self.body[0].y*CELL_SIZE))
        if self.direction == Vector2(1,0):#RIGHT
            WIN.blit(SNAKE_HEAD[1],(self.body[0].x*CELL_SIZE,self.body[0].y*CELL_SIZE))
        if self.direction == Vector2(-1,0):#lEFT
            WIN.blit(SNAKE_HEAD[3],(self.body[0].x*CELL_SIZE,self.body[0].y*CELL_SIZE))

        #print(self.body[0])
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
        
        

        u = -CELL_SIZE
        for y in range(int(self.body[0].y)*CELL_SIZE):
            if Vector2(self.body[0].x*CELL_SIZE, y) in self.body*CELL_SIZE:
                u = y
        
        d = ALTO/CELL_SIZE
        for y in range(ALTO, int(self.body[0].y),-1):
            if Vector2(self.body[0].x, y) in self.body:
                d = y
                
                
        r = ANCHO/CELL_SIZE
        for x in range(ANCHO, int(self.body[0].x), -1):
            if Vector2(x, self.body[0].y) in self.body:
                r = y
                
        l = -CELL_SIZE
        for x in range(int(self.body[0].x)*CELL_SIZE):
            if Vector2(x,self.body[0].y*CELL_SIZE) in self.body*CELL_SIZE:
                #print('asd')
                l = x

        self.distance_to_wall_up = self.body[0].y - u
        self.distance_to_wall_down = d-self.body[0].y
        self.distance_to_wall_right = r- self.body[0].x
        self.distance_to_wall_left = self.body[0].x -l 
        self.distance_to_fruit = Vector2(apple.pos.x-self.body[0].x*CELL_SIZE,apple.pos.y-self.body[0].y*CELL_SIZE)

        '''
        if self.direction == Vector2(0,-1):#UP

            #vect = Vector2(apple.pos.x-self.body[0].x*CELL_SIZE,apple.pos.y-self.body[0].y*CELL_SIZE)
            #self.distance_to_fruit = math.sqrt(math.pow(vect.x,2)+math.pow(vect.y,2))

            self.distance_to_wall = Vector2(0,self.body[0].y*CELL_SIZE+CELL_SIZE)
            for block in self.body[1:]:
                self.distance_to_body = Vector2(0,self.body[0].y-block.y)



        elif self.direction == Vector2(0,1):#DOWN
            #self.distance_to_fruit = Vector2(0,self.body[0].y*CELL_SIZE-apple.pos.y)
            
            self.distance_to_wall = Vector2(0,ALTO/CELL_SIZE-self.body[0].y*CELL_SIZE)
            for block in self.body[1:]:
                self.distance_to_body = Vector2(0,block.y-self.body[0].y)

        elif self.direction == Vector2(1,0):#RIGHT
            #self.distance_to_fruit = Vector2(apple.pos.x-self.body[0].x*CELL_SIZE,0)
            
            self.distance_to_wall = Vector2(ANCHO/CELL_SIZE-self.body[0].y*CELL_SIZE,0)
            for block in self.body[1:]:
                self.distance_to_body = Vector2(self.body[0].x-block.x,0)


        elif self.direction == Vector2(-1,0):#LEFT
            #self.distance_to_fruit = Vector2(self.body[0].x*CELL_SIZE-apple.pos.x,0)
            
            self.distance_to_wall = Vector2(self.body[0].x*CELL_SIZE+CELL_SIZE,0)
            
            for block in self.body[1:]:
                self.distance_to_body = Vector2(block.x-self.body[0].x,0)
                    #print(block,self.body[0],self.distance_to_body)
        '''


    def move_up(self):
        self.direction = Vector2(0,-1)     
    
    def move_down(self):
        self.direction = Vector2(0,1) 

    def move_right(self):
        self.direction = Vector2(1,0) 

    def move_left(self):
        self.direction = Vector2(-1,0) 

    def die(self):
        if self.body[0] == self.body[-1] or self.body[0].x*CELL_SIZE >= ANCHO or self.body[0].y*CELL_SIZE >= ALTO or self.body[0].x*CELL_SIZE <= -CELL_SIZE or self.body[0].y*CELL_SIZE <= -CELL_SIZE:
            return True

        for i in self.body[1:]:
            if self.body[0] == i:
                return True

    def get_mask(self):
        return pygame.mask.from_surface(SNAKE_BODY)

class Apple:
    timer = 0
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
        self.timer+=1
        snake_mask = snake.get_mask()
        
        apple_mask = pygame.mask.from_surface(APPLE)
        apple_offset = (round(self.pos.x - snake.body[0].x*CELL_SIZE ),round(self.pos.y - snake.body[0].y*CELL_SIZE))


        collision_point = snake_mask.overlap(apple_mask,apple_offset)
        #print(self.timer)
        if collision_point:
            
            #self.generate()
            self.timer = -1
            #print(self.score)
            snake.add = True
            return True

        #TO avoid apple spawning on snake body
        for block in snake.body[1:]:
            apple_offset_body =  (round(self.pos.x - block.x*CELL_SIZE ),round(self.pos.y - block.y*CELL_SIZE))
            collision_on_body = snake_mask.overlap(apple_mask,apple_offset_body)
            if collision_on_body:
                self.generate()
        
        return False



def main(genomes,config):#Tabien tiene que evaluar los genomes

    

    for _, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g,config)
        
        g.fitness = points(net)
        
    while False:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
        x,y = pygame.mouse.get_pos()
        print(x,y)

def points(net):

    global fast_mode
    ge = []
    snakes = [Snake()]
    apple = Apple()
    
    score = 0
    fitness = 0

    clock = pygame.time.Clock() 


    while True:
        #clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

        
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    fast_mode = not fast_mode
        '''
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
        '''
        
        if not fast_mode:
            clock.tick(30)
        
        if len(snakes) == 0:
            #print('menor a 0-') 
            return fitness
        else:

            #fitness += .05
            snakes[0].vision(apple)

            output = net.activate((
            
            snakes[0].distance_to_wall_up,
            snakes[0].distance_to_wall_down,
            snakes[0].distance_to_wall_left,
            snakes[0].distance_to_wall_right,
            snakes[0].distance_to_fruit.x,
            snakes[0].distance_to_fruit.y,
            snakes[0].direction.x, 
            snakes[0].direction.y
       
            ))
                
            #print(output)

            directions = [
                    [Vector2(0,1), Vector2(-1,0)],
                    [Vector2(1,0), Vector2(0,-1)],
                ]
            
            snakes[0].direction = directions[output[0] > 0.5][output[1] > 0.5] 
            

            if apple.check_collision(snakes[0]):
                fitness += 50
                score += 1
                EAT_SOUND.play()
                apple = Apple()
                #print('asdas')

       
            WIN.fill((175,215,70))

            snakes[0].draw()
            apple.draw()
            snakes[0].move()

            #fitness+= 0.05

            if snakes[0].die() or apple.timer >= 500:
                fitness -= 0.1
                snakes.pop(0)
                return fitness

            text = STAT_FONT.render("SCORE: {}".format(str(score)),1,(255,255,255))
            WIN.blit(text,(ANCHO-text.get_width()-10,10)) #win.blit = win.draw
            pygame.display.update()


def run(config_file):
    # Load configuration. with all subtopics '[]' and config file name
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)

    # Create the population, which is the top-level object for a NEAT run.
    p = neat.Population(config)

    # Add a stdout reporter to show progress in the terminal.
    p.add_reporter(neat.StdOutReporter(True))
    #stats = neat.StatisticsReporter()
    #p.add_reporter(stats)

    # Run for up to 300 generations.
    winner = p.run(main, 10000)#limite de veces que se ejecuta el programa


if __name__ == '__main__':
    # Determine path to configuration file. This path manipulation is
    # here so that the script will run successfully regardless of the
    # current working directory.
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-feedforward.txt')
    run(config_path)