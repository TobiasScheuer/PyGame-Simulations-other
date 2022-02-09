import pygame
import random

"""
Goal of this Visualization/Simulation: Simulate evolution
white background
wolf (black pixel) and rabbit(red pixel) population
wolf eat rabbits to not die of starvation
evolution -later-
stats:
	      		  | wolf | rabbits | type | mutatable?
speed			     y        y      int 	   y
reproduction rate	 y        y      int       y
offspring		     y        y      range     y
perception range	 y        y      int       n (later yes?)
calories/movement    y        y      int       n
calorie reserve      y        n      int       n
------- later more ----------------

++ V0.1 create wolfes and rabbits
++ V0.2 spawn pixels for animals
++ V0.3 make them move (at random)
++ V0.3.1 perception range and targeting movement
++ V0.4 make them eat, die
++ V0.4.1 introduce starving
++ V0.5 reproduction
+ V0.6 stat collection and plotting
TODO: better stat logging -> plotting
V0.7 evolution trials
++ V1 add environment (rendering disabled, since buggy and slowing)
V2 three species ( orca, tuna, small fish)
V3 balanced species (lions, hyena, deer)
V3.1 balanced species (human 1,2,3) -> Humans.py
V4 single wolf, controllable, game to chase rabbits
"""
WIDTH = 1050
HEIGHT = 420
BACKGROUND = (255, 255, 255)
ANIMALS = []
PLANTS = []
CALMAX = 1400
STATS = dict()
screen = None
COUNTER = 0


class animal:
	"""
	basic class with shared attributes and methods
	"""
	speed = 1			# how many pixels per move can they travel
	repRate = 1000		# every how many ticks are they ready to reproduce
	repTime = 0 		# to count time between reproduction
	offspring = 1		# how many babies on average (range is [n-1, n, n+1])
	calMov = 1			# how many calories are burnt per movement
	calReserve = CALMAX	# Calorie reserve. Goes down calMov per Move. starvation if empty. Rabbit fills by 170. later for rabbits as well
	perception = 115	# how many pixels far they can see other animals. will chase/flee each other
	alive = True
	coordinates = [0,0]
	
	def __init__(self, number, color):
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
		if self.coordinates[0] >= WIDTH:
			self.coordinates[0] = WIDTH - random.randint(1,3)
		elif self.coordinates[0] <= 0:
			self.coordinates[0] = random.randint(1,3)
		if self.coordinates[1] >= HEIGHT:
			self.coordinates[1] = HEIGHT - random.randint(1,3)
		elif self.coordinates[1] <= 0:
			self.coordinates[1] = random.randint(1,3)
		while not screen.get_at(self.coordinates) == BACKGROUND or screen.get_at(self.coordinates) == (10,85,10):
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
					
class wolf(animal):
	"""
	animal 1
	"""
	def __init__(self, number, color, coordinates):
		super().__init__(number, color)
		self.coordinates = coordinates
		self.perception = 135
		self.repRate = 550 + random.randint(1,151)
		self.speed = 2

	def update(self):
		"""
		wolf state machine:
		if calories < 1, starves
		if reproduction time, mating mode, offspring dependant on hunger state
		elif chase and eat rabbits
		else move randomly
		"""
		if self.calReserve < 1: #if calories under 1, starve
			self.alive = False
			#print('wolf ' + str(self.number) + ' starved')
			STATS['wolves starved'] = STATS['wolves starved'] + 1
			STATS['wolves'] = STATS['wolves'] - 1
		else:					# otherwise: percept and move
			self.repTime = self.repTime + 1
			oldCoordinates = self.coordinates
			if self.repTime > self.repRate:	# wolf: mating mode
				self.speed = 3
				minX = self.coordinates[0] - self.perception - 120
				maxX = self.coordinates[0] + self.perception + 121
				minY = self.coordinates[1] - self.perception - 120
				maxY = self.coordinates[1] + self.perception + 121
				found = False
				chaser = random.randint (1,4)	# simplified approach to not have both animals chase each other, as these leads to both moving in parallel
				if chaser == 1:
					for animal in enumerate(ANIMALS): 
						if isinstance(animal[1], wolf) and animal[1].repTime > self.repRate: # checks for other mate-ready animals
							if animal[1].coordinates[0] in range(minX, maxX) and animal[1].coordinates[1] in range(minY, maxY) and animal[1].alive == True:
								Caught = self.chase(animal[1].coordinates)	# moves towards mate-ready animal
								found = True
								if Caught == True:
									tempOffspring = 0
									if self.calReserve > CALMAX-200:
										tempOffspring = self.offspring + 2
										self.repTime = 50
									elif self.calReserve > CALMAX - 550:
										tempOffspring = self.offspring + 1
										self.repTime = 20
									else:
										tempOffspring = self.offspring
										self.repTime = 0
									for i in range (0, tempOffspring):
										newWolf = wolf(len(ANIMALS)+1, (255,255,255), self.coordinates)							
										ANIMALS.append(newWolf)
										#print('wolves ' + str(self.number) +' and ' + str(animal[1].number) + ' bred ' + str(len(ANIMALS)+1) )
										STATS['born wolves'] = STATS['born wolves'] + 1
										STATS['wolves'] = STATS['wolves'] + 1
									animal[1].repTime = 0
									self.speed = 2
									Caught = 0
								break
				if found == False: #  no animal found, move randomly
						self.coordinates = [oldCoordinates[0]+self.speed*random.randrange(-2,3), oldCoordinates[1]+self.speed*random.randrange(-2,3) ]
						self.checkCoor()
			elif self.calReserve < CALMAX-100:	# wolf: chasing mode
				minX = self.coordinates[0] - self.perception
				maxX = self.coordinates[0] + self.perception + 1
				minY = self.coordinates[1] - self.perception
				maxY = self.coordinates[1] + self.perception + 1
				found = False
				for animal in enumerate(ANIMALS):
					if isinstance(animal[1], rabbit) and animal[1].coordinates[0] in range(minX, maxX) and animal[1].coordinates[1] in range(minY, maxY) and animal[1].alive == True:
						found = True
						Caught = self.chase(animal[1].coordinates)
						if Caught == True:
							animal[1].alive = False
							self.calReserve = self.calReserve + 700
							if self.calReserve > CALMAX:
								self.calReserve = CALMAX
							Caught = 0
							#print('rabbit ' + str(animal[1].number) + ' eaten')
							STATS['rabbits eaten'] = STATS['rabbits eaten'] + 1
							STATS['rabbits'] = STATS['rabbits'] - 1
						break
				if found == False:
					self.coordinates = [oldCoordinates[0]+self.speed*random.randrange(-2,3), oldCoordinates[1]+self.speed*random.randrange(-2,3) ]
					self.checkCoor()
			
			else:	#wolf: move randomly
				self.coordinates = [oldCoordinates[0]+self.speed*random.randrange(-2,3), oldCoordinates[1]+self.speed*random.randrange(-2,3) ]
				self.checkCoor()
			self.calReserve = self.calReserve- self.calMov
			
class rabbit(animal):
	"""
	rabbit state machine:
	if calories < 1, starves
	if wolf close, flee
	else
		if reproduction time, mating mode, offspring dependant on hunger state
		elif hungry, eat 
		else move randomly
	"""
	def __init__(self, number, color, coordinates):
		super().__init__(number, color)
		self.coordinates = coordinates
		self.repRate = 200 + random.randint(1,151)
		self.offspring = 4
		self.calReserve = CALMAX - 300

	def update(self):
		global PLANTS
		global COUNTER
		if self.calReserve < 1: #if calories under 1, starve
			self.alive = False
			#print('rabbit ' + str(self.number) + ' starved')
			STATS['rabbits starved'] = STATS['rabbits starved'] + 1
			STATS['rabbits'] = STATS['rabbits'] - 1
		else:
			self.repTime = self.repTime + 1
			oldCoordinates = self.coordinates
			minX = self.coordinates[0] - self.perception
			maxX = self.coordinates[0] + self.perception + 1
			minY = self.coordinates[1] - self.perception
			maxY = self.coordinates[1] + self.perception + 1
			fleeing = False
			if self.calReserve < CALMAX-300 - 500: # if not close to starving, check if there's a need to flee
				for animal in enumerate(ANIMALS): #if wolf close, flee
					if isinstance(animal[1], wolf) and animal[1].coordinates[0] in range(minX, maxX) and animal[1].coordinates[1] in range(minY, maxY) and animal[1].alive == True:
						# run you fool!
						fleeing = True
						self.avoid(animal[1].coordinates)
						break				
			if fleeing == False:
				if self.repTime > self.repRate:	# rabbit: mating mode
					self.speed = 2
					minX = self.coordinates[0] - self.perception - 20
					maxX = self.coordinates[0] + self.perception + 21
					minY = self.coordinates[1] - self.perception - 20
					maxY = self.coordinates[1] + self.perception + 21
					found = False
					chaser = random.randint (1,4)	# simplified approach to not have both animals chase each other, as these leads to both moving in parallel
					if chaser == 2:
						for animal in enumerate(ANIMALS): 
							if isinstance(animal[1], rabbit) and animal[1].repTime > self.repRate: # checks for other mate-ready animals
								if animal[1].coordinates[0] in range(minX, maxX) and animal[1].coordinates[1] in range(minY, maxY) and animal[1].alive == True:
									found = True
									Caught = self.chase(animal[1].coordinates)	# moves towards mate-ready animal
									if Caught == True:
										tempOffspring = 0
										if self.calReserve > CALMAX-300-150:
											tempOffspring = self.offspring + 2
											self.repTime = 30
										elif self.calReserve > CALMAX - 300- 500:
											tempOffspring = self.offspring + 1
											self.repTime = 0
										else:
											tempOffspring = self.offspring
											self.repTime = 0
										for i in range (0, tempOffspring):
											newRabbit = rabbit(len(ANIMALS)+1, (255,0,0), self.coordinates)							
											ANIMALS.append(newRabbit)
											STATS['born rabbits'] = STATS['born rabbits'] + 1
											STATS['rabbits'] = STATS['rabbits'] + 1
										animal[1].repTime = 0
										Caught = 0
										self.speed = 1
									break
					if found == False: #  no animal found, move randomly
						self.coordinates = [oldCoordinates[0]+self.speed*random.randrange(-3,4), oldCoordinates[1]+self.speed*random.randrange(-3,4) ]
						self.checkCoor()
				elif self.calReserve < CALMAX-300 - 100:	# rabbit hungry
					minX = self.coordinates[0] - self.perception
					maxX = self.coordinates[0] + self.perception + 1
					minY = self.coordinates[1] - self.perception
					maxY = self.coordinates[1] + self.perception + 1
					found = False
					Caught = False
					plantIndex = 0
					for i, plant in enumerate(PLANTS):
						if plant.coordinates[0] in range(minX, maxX) and plant.coordinates[1] in range(minY, maxY) and plant.alive == True:
							found = True
							Caught = self.chase(plant.coordinates)
							if Caught == True:
								#plant.alive = False
								plantIndex = i
								self.calReserve = self.calReserve + 320
								if self.calReserve > CALMAX - 300:
									self.calReserve = CALMAX - 300
								COUNTER = COUNTER + 1
							break			
					if found == False:
						self.coordinates = [oldCoordinates[0]+self.speed*random.randrange(-2,3), oldCoordinates[1]+self.speed*random.randrange(-2,3) ]
						self.checkCoor()
					if Caught == True:
						PLANTS.pop(plantIndex)
				
				else:	#rabbit: move randomly
					self.coordinates = [oldCoordinates[0]+self.speed*random.randrange(-3,4), oldCoordinates[1]+self.speed*random.randrange(-3,4) ]
					self.checkCoor()
			self.calReserve = self.calReserve- self.calMov # ToDo: Edit out when food for rabbits added

class plantClass:
	"""
	base class for plants
	"""
	repRate = 4 + random.randint(1,3)		# low reptime since .update() only called every 4 seconds!
	repTime = 0 		# to count time between reproduction
	offspring = 1		# how many babies on average (range is [n-1, n, n+1])

	def __init__(self, number, color, coordinates):
		self.number = number
		self.pixel = pygame.Surface((5,5))
		self.pixel.fill (color)	#paint pixel with right color
		self.coordinates = coordinates
		self.repTime = 0
		self.offspring = 1
		self.alive = True
	
	def update(self):
		self.repTime = self.repTime + 1
		if self.repTime > self.repRate and len(PLANTS) < 1000:
			for i in range(0, self.offspring):
				newCoordinates = self.coordinates
				j = random.randint(1,5)
				skip = False
				if j == 1:
					newCoordinates[0] = self.coordinates[0] + random.randint(1,8)
				elif j == 2:
					newCoordinates[0] = self.coordinates[0] - random.randint(1,8)
				elif j == 3:
					newCoordinates[1] = self.coordinates[1] + random.randint(1,8)
				else:
					newCoordinates[1] = self.coordinates[1] - random.randint(1,8)
				if newCoordinates[0] >= WIDTH:
					skip = True
				elif newCoordinates[0] <= 0:
					skip = True
				if newCoordinates[1] >= HEIGHT:
					skip = True
				elif newCoordinates[1] <= 0:
					skip = True
				if skip == False:
					newPlant = plantClass(len(PLANTS)+1, (10,85,10), newCoordinates)							
					PLANTS.append(newPlant)
			self.repTime = 0


def main():
	global screen
	global ANIMAL
	global PLANTS
	global STATS
	global COUNTER
	STATS = {
    'wolves': 0,
	'rabbits': 0,
	'born wolves' : 0,
	'born rabbits': 0,
	'rabbits eaten': 0,
	'wolves starved' : 0,
	'rabbits starved' : 0 }
	clock = pygame.time.Clock()
	pygame.init()
	screen = pygame.display.set_mode((WIDTH, HEIGHT))
	PLANTS =  []
	for i in range (1,146):
		randCoordinates = [random.randrange(1,WIDTH), random.randrange(1, HEIGHT)]
		Plant = plantClass(i, (10,85,10), randCoordinates)
		PLANTS.append (Plant)
	for i in range (1,10):
		randCoordinates = [random.randrange(1,WIDTH), random.randrange(1, HEIGHT)]
		Wolf = wolf(i, (0,0,0), randCoordinates)	#number, Color (black)
		ANIMALS.append (Wolf)
		STATS['wolves'] = STATS['wolves'] + 1
	for i in range (1,30):
		randCoordinates = [random.randrange(1,WIDTH), random.randrange(1, HEIGHT)]
		Rabbit = rabbit(i, (255,0,0), randCoordinates)	#number, Color (red)
		ANIMALS.append (Rabbit)
		STATS['rabbits'] = STATS['rabbits'] + 1
	MOVEEVENT, t = pygame.USEREVENT+1, 4100
	pygame.time.set_timer(MOVEEVENT, t)
	pygame.event.set_allowed([MOVEEVENT]) # not allowing any keyboard input, allegedly improves performance
	
	while 1:
		screen.fill(BACKGROUND)
		for event in pygame.event.get():
			if event.type == MOVEEVENT:
				#print(STATS)
				#print(str(len(PLANTS)) + ' ' + str(COUNTER))
				caption = 'wolves: ' + str(STATS['wolves']) + ' rabbits: ' + str(STATS['rabbits']) + ' plants: ' + str(len(PLANTS)) 
				pygame.display.set_caption(caption)
				for i, plant in enumerate(PLANTS):
					#if plant.alive:
					#screen.blit(plant.pixel, plant.coordinates) #makes no sense in current implementation since Background filling overdrawds plant pixels
					plant.update()
						#if not plant.alive:
						#	del PLANTS[i]
		for i, animal in enumerate(ANIMALS):
			if animal.alive:
				screen.blit(animal.pixel, animal.coordinates)	# moves the pixel to new coordinates(coordinates moved in class method)
				animal.update()
				if not animal.alive:
					del ANIMALS[i]
		pygame.display.flip()
		clock.tick(16)

if __name__ == "__main__":
	main()