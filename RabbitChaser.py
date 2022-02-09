import pygame
import random

"""
Goal of this Visualization/Simulation: 3rd person controlled wolf chases rabbits
white background
wolf (black pixel) and rabbit(red pixel) population
wolf eat rabbits to not die of starvation
evolution -later-
stats:
	      		  | wolf | rabbits | type | mutatable?
speed			     y        y      int 	   y
reproduction rate	 n        y      int       y
offspring		     n        y      range     y
perception range	 y        y      int       n (later yes?)
calories/movement    y        y      int       n
calorie reserve      y        y      int       n
------- later more ----------------

++V0.1 copied from WolfRabbitPlant
++V0.2 get basics running
++V0.3 add controls for wolf
++V0.4 controls testing and tweaking
V0.5 edit rabbits to flee from wolf
V0.6 environment?
V? ?
"""
WIDTH = 1050
HEIGHT = 420
NOVISION = (66,66,66)
BACKGROUND = (255, 255, 255)
RABBITS = []
CALMAX = 1400
STATS = dict()
screen = None


class animal:
	"""
	basic class with shared attributes and methods
	"""
	speed = 1			# how many pixels per move can they travel
	repRate = 1000		# every how many ticks are they ready to reproduce
	repTime = 0 		# to count time between reproduction
	offspring = 1		# how many babies on average (range is [n-1, n, n+1])
	calMov = 1			# how many calories are burnt per movement
	calReserve = CALMAX	# Calorie reserve. Goes down calMov per Move. starvation if empty. Rabbit fills by XX
	perception = 115	# how many pixels far they can see other animals. will chase/flee each other
	alive = True
	coordinates = [0,0]
	
	def __init__(self, number, color, coordinates):
		self.number = number
		self.pixel = pygame.Surface((5,4))
		self.pixel.fill (color)	#paint pixel with right color

	def chase(self, TargetCoordinates):
		oldCoordinates = self.coordinates
		xdiff = self.coordinates[0]-TargetCoordinates[0] 
		ydiff = self.coordinates[1]-TargetCoordinates[1] 
		Caught = 0 		# variable to check if animal caught (0 init, +1 each for in x and y range. 2 -> caught)
		if xdiff < -6: # animal to the right and not in range
			self.coordinates[0] = oldCoordinates[0]+self.speed
		elif xdiff > 6:	# animal to the left and not in range
			self.coordinates[0] = oldCoordinates[0]-self.speed
		else:
			Caught = Caught +1
		if ydiff < -5: # animal below and not in range
			self.coordinates[1] = oldCoordinates[1]+self.speed
		elif ydiff > 5:	# animal above and not in range
			self.coordinates[1] = oldCoordinates[1]-self.speed
		else:
			Caught = Caught +1
		self.checkCoor()
		if Caught == 2:
			return True

	def avoid(self, TargetCoordinates):
		oldCoordinates = self.coordinates
		xdiff = self.coordinates[0]-TargetCoordinates[0] 
		ydiff = self.coordinates[1]-TargetCoordinates[1] 
		if xdiff < -3: # wolf to the right
			self.coordinates[0] = oldCoordinates[0]-self.speed
		elif xdiff > 3:	# wolf to the left
			self.coordinates[0] = oldCoordinates[0]+self.speed
		else:
			self.coordinates[0] = oldCoordinates[0]
		if ydiff < -3: # wolf below
			self.coordinates[1] = oldCoordinates[1]-self.speed
		elif ydiff > 3:	# wolf above
			self.coordinates[1] = oldCoordinates[1]+self.speed	
		else:
			self.coordinates[1] = oldCoordinates[1]
		self.checkCoor()

	def checkCoor(self):
		"""
		this method ensures that the coordinates are within screen bounds and the pixel is unoccupied
		"""
		global screen
		reTry = True
		if self.coordinates[0] >= WIDTH:
			self.coordinates[0] = WIDTH - random.randint(1,3)
		elif self.coordinates[0] <= 0:
			self.coordinates[0] = random.randint(1,3)
		if self.coordinates[1] >= HEIGHT:
			self.coordinates[1] = HEIGHT - random.randint(1,3)
		elif self.coordinates[1] <= 0:
			self.coordinates[1] = random.randint(1,3)
		if screen.get_at(self.coordinates) == BACKGROUND or screen.get_at(self.coordinates) == NOVISION:
			reTry = False
		while reTry == True:
			# checks if pixel background color (->empty) or plant color 
			oldCoordinates = self.coordinates
			self.coordinates = [oldCoordinates[0]+random.randrange(-2,3), oldCoordinates[1]+random.randrange(-2,3) ]
			if self.coordinates[0] >= WIDTH:
				self.coordinates[0] = WIDTH - random.randint(1,3)
			elif self.coordinates[0] <= 0:
				self.coordinates[0] = random.randint(1,3)
			if self.coordinates[1] >= HEIGHT:
				self.coordinates[1] = HEIGHT - random.randint(1,3)
			elif self.coordinates[1] <= 0:
				self.coordinates[1] = random.randint(1,3)
			if screen.get_at(self.coordinates) == BACKGROUND or screen.get_at(self.coordinates) == NOVISION:
				reTry = False
					
class wolf(animal):
	"""
	animal 1
	"""
	def __init__(self, number, color, coordinates):
		super().__init__(number, color, coordinates)
		self.coordinates = coordinates
		self.perception = 135
		self.speed = 2
		#self.vision = pygame.Surface()

	def update(self):
		"""
		wolf state machine:
		if calories < 1, starves
		if reproduction time, mating mode, offspring dependant on hunger state
		elif chase and eat rabbits
		else move randomly
		"""
		global STATS
		if self.calReserve < 1: #if calories under 1, starve
			self.alive = False
			#print('wolf ' + str(self.number) + ' starved')
			STATS['wolves starved'] = STATS['wolves starved'] + 1
			STATS['wolves'] = STATS['wolves'] - 1
		else:				
			xRange = range(self.coordinates[0] - 6, self.coordinates[0] + 7)
			yRange = range(self.coordinates[1] - 5, self.coordinates[1] + 6)
			for i, animal in enumerate(RABBITS):
				if animal.coordinates[0] in xRange and animal.coordinates[1] in yRange:
					if animal.coordinates[1] in range(self.coordinates[1] - 5, self.coordinates[1] + 6):
						animal.alive = False
						RABBITS.pop(i)
						STATS['rabbits'] = STATS['rabbits'] - 1
						STATS['rabbits eaten'] = STATS['rabbits eaten'] + 1
						self.calReserve = self.calReserve + 150
						break
			self.calReserve = self.calReserve- self.calMov
	
	def checkBorders(self):
		if self.coordinates[0] >= WIDTH:
			self.coordinates[0] = WIDTH - random.randint(1,2)
		elif self.coordinates[0] <= 0:
			self.coordinates[0] = random.randint(1,2)
		if self.coordinates[1] >= HEIGHT:
			self.coordinates[1] = HEIGHT - random.randint(1,2)
		elif self.coordinates[1] <= 0:
			self.coordinates[1] = random.randint(1,2)
			
class rabbit(animal):
	"""
	rabbit state machine:
	if wolf close, flee
	else
		if reproduction time, mating mode
		else move randomly
	"""
	def __init__(self, number, color, coordinates):
		super().__init__(number, color, coordinates)
		self.coordinates = coordinates
		self.repRate = 15
		self.offspring = 4

	def update(self):
		oldCoordinates = self.coordinates
		minX = self.coordinates[0] - self.perception
		maxX = self.coordinates[0] + self.perception + 1
		minY = self.coordinates[1] - self.perception
		maxY = self.coordinates[1] + self.perception + 1
		fleeing = False
		for animal in enumerate(RABBITS): #if wolf close, flee
			if isinstance(animal[1], wolf) and animal[1].coordinates[0] in range(minX, maxX) and animal[1].coordinates[1] in range(minY, maxY) and animal[1].alive == True:
				# run you fool!
				fleeing = True
				self.avoid(animal[1].coordinates)
				break				
		if fleeing == False:
			if self.repTime > self.repRate and len(RABBITS)< 150:	# rabbit: mating mode
				self.speed = 2
				minX = self.coordinates[0] - self.perception - 20
				maxX = self.coordinates[0] + self.perception + 21
				minY = self.coordinates[1] - self.perception - 20
				maxY = self.coordinates[1] + self.perception + 21
				found = False
				chaser = random.randint (1,4)	# simplified approach to not have both RABBITS chase each other, as these leads to both moving in parallel
				if chaser == 2:
					for animal in enumerate(RABBITS): 
						if isinstance(animal[1], rabbit) and animal[1].repTime > self.repRate: # checks for other mate-ready RABBITS
							if animal[1].coordinates[0] in range(minX, maxX) and animal[1].coordinates[1] in range(minY, maxY) and animal[1].alive == True:
								found = True
								Caught = self.chase(animal[1].coordinates)	# moves towards mate-ready animal
								if Caught == True:
									for i in range (0, self.offspring):
										newRabbit = rabbit(len(RABBITS)+1, (255,0,0), self.coordinates)							
										RABBITS.append(newRabbit)
										STATS['rabbits'] = STATS['rabbits'] + 1
									self.repTime = 0
									animal[1].repTime = 0
									Caught = 0
									self.speed = 1
									animal[1].speed = 1
								break
				if found == False: #  no animal found, move randomly
					self.coordinates = [oldCoordinates[0]+self.speed*random.randrange(-3,4), oldCoordinates[1]+self.speed*random.randrange(-3,4) ]
					self.checkCoor()
			else:	#rabbit: move randomly
				self.coordinates = [oldCoordinates[0]+self.speed*random.randrange(-3,4), oldCoordinates[1]+self.speed*random.randrange(-3,4) ]
				self.checkCoor()

def main():
	global screen
	global ANIMAL
	global STATS
	STATS = {
	'rabbits': 0,
	'rabbits eaten': 0,
	'rabbits starved' : 0 }
	clock = pygame.time.Clock()
	pygame.init()
	screen = pygame.display.set_mode((WIDTH, HEIGHT))
	randCoordinates = [random.randrange(1,WIDTH), random.randrange(1, HEIGHT)]
	Wolf = wolf(1, (0,0,0), randCoordinates)	#number, Color (black)
	for i in range (1,30):
		randCoordinates = [random.randrange(1,WIDTH), random.randrange(1, HEIGHT)]
		Rabbit = rabbit(i, (255,0,0), randCoordinates)	#number, Color (red)
		RABBITS.append (Rabbit)
		STATS['rabbits'] = STATS['rabbits'] + 1
	CAPTIONEVENT, t = pygame.USEREVENT+1, 4500
	pygame.time.set_timer(CAPTIONEVENT, t)
	RABBITEVENT, t2 = pygame.USEREVENT+2, 2000
	pygame.time.set_timer(RABBITEVENT, t2)
	caption = ' rabbits: ' + str(STATS['rabbits']) + '   rabbits eaten: ' + str(STATS['rabbits eaten'])
	pygame.display.set_caption(caption)
	while 1:
		screen.fill(NOVISION)
		pygame.draw.circle(screen, BACKGROUND, Wolf.coordinates, Wolf.perception) # draws a white circle around the wolf with its perception range as radius
		for event in pygame.event.get():
			if event.type == CAPTIONEVENT:
				caption = ' rabbits: ' + str(STATS['rabbits']) + '   rabbits eaten: ' + str(STATS['rabbits eaten'])
				pygame.display.set_caption(caption)
			elif event.type == RABBITEVENT:
				for i, animal in enumerate(RABBITS):
					animal.repTime = animal.repTime + random.randint(1,5) 
		for i, animal in enumerate(RABBITS):
			if animal.alive:
				if not screen.get_at(animal.coordinates) == NOVISION:
					screen.blit(animal.pixel, animal.coordinates)	# moves the pixel to new coordinates(coordinates moved in class method)
				animal.update()
				if not animal.alive:
					del RABBITS[i]
		screen.blit(Wolf.pixel, Wolf.coordinates)
		Wolf.update()
		pygame.display.flip()
		Keys = pygame.key.get_pressed()
		if Keys[pygame.K_w] == True:
			Wolf.coordinates[1] = Wolf.coordinates[1] - Wolf.speed
			Wolf.checkBorders()
		if Keys[pygame.K_s] == True:
			Wolf.coordinates[1] = Wolf.coordinates[1] + Wolf.speed
			Wolf.checkBorders()
		if Keys[pygame.K_a] == True:
			Wolf.coordinates[0] = Wolf.coordinates[0] - Wolf.speed
			Wolf.checkBorders()
		if Keys[pygame.K_d] == True:
			Wolf.coordinates[0] = Wolf.coordinates[0] + Wolf.speed
			Wolf.checkBorders()
		clock.tick(25)

if __name__ == "__main__":
	main()