import pygame
from pygame.math import Vector2 
import random
import os
import neat
import argparse
import pickle

pygame.init()


ANCHO = 800
ALTO = 800

local_dir = os.path.dirname(__file__)

SNAKE_BODY = pygame.transform.scale(pygame.image.load(os.path.join(local_dir,"images/snakebody.png")),(20,20))
APPLE = pygame.transform.scale(pygame.image.load(os.path.join(local_dir,"images/manzana.png")),(20,20))
SNAKE_HEAD = []
for x in range(1,5):
	SNAKE_HEAD+=[pygame.transform.scale(pygame.image.load(os.path.join(local_dir,"images/SnakeHead"+str(x)+".png")),(20,20))]

EAT_SOUND = pygame.mixer.Sound("coin.wav")


WIN = pygame.display.set_mode((ANCHO,ALTO))
SCORE_TEXT = pygame.font.SysFont("Russo One",35)

fast_mode = True

population = 0


class Snake:
	def __init__(self):
		self.body = [Vector2(20,100),Vector2(20,110),Vector2(20,120)]
		self.direction = Vector2(0,-20)
		self.add = False
		self.distance_to_wall_up = 0
		self.distance_to_wall_down = 0
		self.distance_to_wall_left = 0
		self.distance_to_wall_right = 0
		self.distance_to_body = Vector2(0,0)

	def draw(self):
		for bloque in self.body:
			WIN.blit(SNAKE_BODY,(bloque.x,bloque.y))

		if self.direction == Vector2(0,-20):
			WIN.blit(SNAKE_HEAD[0],(self.body[0].x,self.body[0].y))

		if self.direction == Vector2(0,20):
			WIN.blit(SNAKE_HEAD[2],(self.body[0].x,self.body[0].y))

		if self.direction == Vector2(20,0):
			WIN.blit(SNAKE_HEAD[1],(self.body[0].x,self.body[0].y))

		if self.direction == Vector2(-20,0):
			WIN.blit(SNAKE_HEAD[3],(self.body[0].x,self.body[0].y))

	def move(self):
		
		#[0,1,2] --> [0,1] --> [None,0,1] --> [-1,0,1]
		if self.add == True:
			body_copy = self.body
			body_copy.insert(0,body_copy[0]+self.direction)
			self.body = body_copy[:]
			self.add = False
		else:
			body_copy = self.body[:-1]
			body_copy.insert(0,body_copy[0]+self.direction)
			self.body = body_copy[:]


	def move_up(self):
		self.direction = Vector2(0,-20)

	def move_down(self):
		self.direction = Vector2(0,20)

	def move_right(self):
		self.direction = Vector2(20,0)

	def move_left(self):
		self.direction = Vector2(-20,0)

	def die(self):

		if self.body[0].x >= ANCHO or self.body[0].y >= ALTO or self.body[0].x <= -20 or self.body[0].y <= -20:
			return True

		#SNake se toca a si misma
		for i in self.body[1:]:
			if self.body[0] == i:
				return True

	def vision(self,apple):
        
        

		u = 0
		for y in range(int(self.body[0].y)):
			if Vector2(self.body[0].x, y) in self.body:
				u = y
        
		d = ALTO
		for y in range(ALTO, int(self.body[0].y),-1):
			if Vector2(self.body[0].x, y) in self.body:
				d = y
                
                
		r = ANCHO
		for x in range(ANCHO, int(self.body[0].x), -1):
			if Vector2(x, self.body[0].y) in self.body:
				r = x
                
		l = 0
		for x in range(int(self.body[0].x)):
			if Vector2(x,self.body[0].y) in self.body:
				#print('asd')
				l = x

		self.distance_to_wall_up = self.body[0].y - u
		self.distance_to_wall_down = d - self.body[0].y
		self.distance_to_wall_right = r - self.body[0].x
		self.distance_to_wall_left = self.body[0].x - l 
		self.distance_to_fruit = Vector2(apple.pos.x-self.body[0].x,apple.pos.y-self.body[0].y)


class Apple:
	timer = 0

	def __init__(self):
		self.generate()


	def draw(self):
		WIN.blit(APPLE,(self.pos.x,self.pos.y))


	def generate(self):
		self.x = random.randrange(0,ANCHO/20)
		self.y = random.randrange(0,ALTO/20)
		self.pos = Vector2(self.x*20,self.y*20)

	def check_collision(self,snake):
		self.timer+=1
		if snake.body[0] == self.pos:
			self.generate()
			snake.add = True
			self.timer = -1
			return True

		for bloque in snake.body[1:]:
			if self.pos == bloque:
				self.generate()

		return False


max_apples = 0

def main(genomes,config):
    

    for _, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g,config)
        g.fitness = points(net)
    print("MAX APPLES",max_apples)


def points(net):

	global fast_mode
	global max_apples
	apple = Apple()
	score = 0
	fitness = 0

	ge = []
	snakes = [Snake()]

	fps = pygame.time.Clock()

	while True:

		#fps.tick(30)

		for event in pygame.event.get():
			
			if event.type == pygame.QUIT:
				save(population)
				quit()

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
					fast_mode = not fast_mode
		'''
			if event.type == pygame.KEYDOWN and snake.direction.y != 20:
				if event.key == pygame.K_UP:
					snake.move_up()

			if event.type == pygame.KEYDOWN and snake.direction.y != -20:
				if event.key == pygame.K_DOWN:
					snake.move_down()


			if event.type == pygame.KEYDOWN and snake.direction.x != -20:
				if event.key == pygame.K_RIGHT:
					snake.move_right()

			if event.type == pygame.KEYDOWN and snake.direction.x != 20:
				if event.key == pygame.K_LEFT:
					snake.move_left()
			'''

		if not fast_mode:
			fps.tick(60)
		#	print("s")

		if len(snakes) == 0:
			break
		else:
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
				[Vector2(0,20), Vector2(-20,0)],
				[Vector2(20,0), Vector2(0,-20)],
			]
			            
			snakes[0].direction = directions[output[0] > 0.5][output[1] > 0.5] 
	
			fitness += 0.005	#for it to understand that remaining alive is also good. Otherwise you it gets stuck 	            

			if apple.check_collision(snakes[0]):
				fitness += 1
				score += 1
				EAT_SOUND.play()
				apple = Apple()
				#print('asdas')

			if snakes[0].die() or apple.timer >= 400:
				#fitness -= 0.1
				snakes.pop(0)
				max_apples = max(max_apples,score)
				return fitness
						
		
		snakes[0].move()

		WIN.fill((175,215,70))
		snakes[0].draw()
		apple.draw()
		text = SCORE_TEXT.render("Score: {}".format(score),1,(255,255,255))

		if(args.norender == None or int(args.norender) != 0):
			WIN.blit(text,(ANCHO-text.get_width()-20,20))
			pygame.display.update()
			

	


def run(config_file,p):
	global population
    # Load configuration. with all subtopics '[]' and config file name
	config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
							neat.DefaultSpeciesSet, neat.DefaultStagnation,
							config_file)

    # Create the population, which is the top-level object for a NEAT run.
	if not p:
		p = neat.Population(config)


	if args.population == None:
		p.add_reporter(neat.StdOutReporter(True))

    # Add a stdout reporter to show progress in the terminal.
    #if not p:
	#	p.add_reporter(neat.StdOutReporter(True))
    #stats = neat.StatisticsReporter()
    #p.add_reporter(stats)

    # Run for up to 1000 generations.
	population = p
	winner = p.run(main, 1000)#limite de veces que se ejecuta el programa
	save(p)

def load(file_name):
	with open(str(file_name),'rb') as file:
		return pickle.load(file)

def save(population):
	with open('population.dat','wb') as file:
		pickle.dump(population,file,pickle.HIGHEST_PROTOCOL)


if __name__ == '__main__':
	config_path = os.path.join(local_dir,'config-feedforward.txt')

	parser = argparse.ArgumentParser(description='Snake AI with Neat by sammas24')
	parser.add_argument('--norender','-r', help='do not render snake for faster result. Parse 0 to dont render. Example: python3 snake_ai.py -r 0')

	parser.add_argument('--population','-p', '--population', help='load_population_results')
	args = parser.parse_args()

	if not any(vars(args).values()) or args.population == None:
		run(config_path,None)
	else:
		run(config_path,load(args.population))
