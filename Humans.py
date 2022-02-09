import pygame
import random

"""
Goal of this Visualization/Simulation: Simulate evolution
white background
Humans1 (black pixel), H2 (red pixel), H3 (blue? pixels) population
fight each other. TODO: Fighting properties?

stats:
	      		  | H1 | H2 | H3 | type | mutatable?
speed			     y    y    y      int 	   y
offspring 			 y    y    y      int      y 
perception range	 y    y    y      int       n (later yes?)
------- later more ----------------

++ V0.1 copied from WolfRabbitPlant V0.5
++ V0.2 get basics running (Human class, instances, pixel spawning and moving)
++ V0.3 add environment
++ V0.4 add houses (spawning humans)
++ V0.5 add fighting
V0.6 add humans spawning houses, add capturing houses, colored houses?

"""
WIDTH = 1050
HEIGHT = 420
BACKGROUND = (255, 255, 255)
HUMANS = []
ENVIRONMENT = []
HOUSES = []
RUINS = []
STATS = dict()
screen = None

class HomoSapiens:
	"""
	basic class with shared attributes and methods
	"""
	speed = 2			# how many pixels per move can they travel
	offspring = 1		
	perception = 120	# how many pixels far they can see other humans. will chase/flee each other
	alive = True
	coordinates = [0,0]
	eventless = 0
	
	def __init__(self, team, color, coordinates):
		self.team = team
		self.coordinates = coordinates
		self.pixel = pygame.Surface((4,4))
		self.pixel.fill (color)	#paint pixel with right color

	def chase(self, TargetCoordinates):
		oldCoordinates = self.coordinates
		xdiff = self.coordinates[0]-TargetCoordinates[0] 
		ydiff = self.coordinates[1]-TargetCoordinates[1] 
		Caught = 0 		# variable to check if human caught (0 init, +1 each for in x and y range. 2 -> caught)
		if xdiff < -9: # human to the right and not in range
			self.coordinates[0] = oldCoordinates[0]+self.speed
		elif xdiff > 8:	# human to the left and not in range
			self.coordinates[0] = oldCoordinates[0]-self.speed
		else:
			self.coordinates[0] = TargetCoordinates[0] + 1
			Caught = Caught + 1
		if ydiff < -9: # human below and not in range
			self.coordinates[1] = oldCoordinates[1]+self.speed
		elif ydiff > 8:	# human above and not in range
			self.coordinates[1] = oldCoordinates[1]-self.speed
		else:
			self.coordinates[1] = TargetCoordinates[1] + 1
			Caught = Caught +1
		self.checkCoor()
		if Caught == 2:
			return True

	def avoid(self, TargetCoordinates):
		oldCoordinates = self.coordinates
		xdiff = self.coordinates[0]-TargetCoordinates[0] 
		ydiff = self.coordinates[1]-TargetCoordinates[1] 
		if xdiff < -3: # other human to the right
			self.coordinates[0] = oldCoordinates[0]-self.speed
		elif xdiff > 3:	# other human to the left
			self.coordinates[0] = oldCoordinates[0]+self.speed	
		else:
			self.coordinates[0] = oldCoordinates[0]
		if ydiff < -3: # other human below
			self.coordinates[1] = oldCoordinates[1]-self.speed
		elif ydiff > 3:	# other human above
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
			self.coordinates[0] = WIDTH - random.randint(2,4)
		elif self.coordinates[0] <= 0:
			self.coordinates[0] = random.randint(2,4)
		if self.coordinates[1] >= HEIGHT:
			self.coordinates[1] = HEIGHT - random.randint(2,4)
		elif self.coordinates[1] <= 0:
			self.coordinates[1] = random.randint(2,4)
		while not screen.get_at(self.coordinates) == BACKGROUND:
			# checks if pixel background color (->empty)
			oldCoordinates = self.coordinates
			self.coordinates = [oldCoordinates[0]+random.randrange(-3,4), oldCoordinates[1]+random.randrange(-3,4) ]
			if self.coordinates[0] >= WIDTH:
				self.coordinates[0] = WIDTH - random.randint(2,4)
			elif self.coordinates[0] <= 0:
				self.coordinates[0] = random.randint(2,4)
			if self.coordinates[1] >= HEIGHT:
				self.coordinates[1] = HEIGHT - random.randint(2,4)
			elif self.coordinates[1] <= 0:
				self.coordinates[1] = random.randint(2,4)
	
	def buildHouse(self):
		global HOUSES
		global STATS
		houseClose = False
		for i,house in enumerate(HOUSES):
			if house.coordinates[0] in range(self.coordinates[0]-65, self.coordinates[0]+66):
				if house.coordinates[1] in range(self.coordinates[1]-65, self.coordinates[1]+66):
					houseClose = True
					break
		if houseClose == False:
			#closeToEdge = False
			if self.coordinates[0] in range(0,21) or self.coordinates[0] in range(WIDTH-20, WIDTH+1):
				#closeToEdge = True
				pass
			elif self.coordinates[1] in range(0,21) or self.coordinates[1] in range(HEIGHT-20, HEIGHT+1):
				#closeToEdge = True
				pass
			else:
			#if closeToEdge == False:
				newHouse = House(self.coordinates, self.team)
				HOUSES.append(newHouse)
				STATS['Houses'] = STATS['Houses'] + 1

	def update(self):
		oldCoordinates = self.coordinates
		minX = self.coordinates[0] - self.perception
		maxX = self.coordinates[0] + self.perception +  1 
		minY = self.coordinates[1] - self.perception
		maxY = self.coordinates[1] + self.perception + 1 
		movedThisTurn = False
		for i, human in enumerate(HUMANS): 
			if human.team != self.team: 
				if human.coordinates[0] in range(minX, maxX) and human.coordinates[1] in range(minY, maxY) and human.alive == True:
					movedThisTurn = True
					self.eventless = 0
					chaser = random.randint (1,7)	# simplified approach to not have both humans chase each other, as these leads to both moving in parallel
					if chaser == 1:
						Caught = self.chase(human.coordinates)	# moves towards other human
						if Caught == True:
							winner = random.randint(1,2)
							if winner == 1:
								human.alive = False
								tempTeam = 'H'+ str(human.team)
							else:
								self.alive = False
								tempTeam = 'H'+ str(self.team)
							STATS[tempTeam] = STATS [tempTeam] - 1
							STATS['KILLS'] = STATS['KILLS'] + 1
							Caught = 0
						break
			elif movedThisTurn == False and self.coordinates != human.coordinates: # no enemies near, same team, not itself
				if human.coordinates[0] in range(minX, maxX) and human.coordinates[1] in range(minY, maxY) and human.alive == True:
					self.eventless = self.eventless + 1
					chaser = random.randint (1,11)	# simplified approach to not have both humans chase each other, as these leads to both moving in parallel
					if chaser == 1:
						movedThisTurn = True
						self.avoid (human.coordinates)
					break
		if movedThisTurn == False: #  no human found, check for houses to attack or move randomly
				for l, house in enumerate(HOUSES):
					if house.coordinates[0] in range(minX-100, maxX+100) and house.coordinates[1] in range(minY-100, maxY+100):
						if house.team != self.team:
							self.chase(house.coordinates)
							movedThisTurn = True
							break 
		if movedThisTurn == False: # move randomly
			self.eventless = self.eventless + 1
			if self.eventless > 450:
				chance = random.randint(1,7)
				if chance == 3:
					self.buildHouse()
				self.eventless = 0
			else:
				self.coordinates = [oldCoordinates[0]+self.speed*random.randrange(-2,3), oldCoordinates[1]+self.speed*random.randrange(-2,3) ]
				self.checkCoor()
					
class H1(HomoSapiens):
	offspring = 3
	def __init__(self, team, color, coordinates):
		super().__init__( team, color, coordinates)
		pass
		

class H2(HomoSapiens):
	offspring = 4
	speed = 2
	offspring = 3
	def __init__(self, team, color, coordinates):
		super().__init__( team, color, coordinates)
		pass
		

class H3(HomoSapiens):
	offspring = 3
	def __init__(self, team, color, coordinates):
		super().__init__( team, color, coordinates)
		pass
		

class Env:
	def __init__(self, coordinates):
		self.coordinates = coordinates

class Mountain(Env):
	def __init__(self, coordinates):
		super().__init__(coordinates)
		self.size = (100,60)
		tempimage = pygame.image.load("res/mountain.png").convert()
		self.image = pygame.transform.smoothscale(tempimage, self.size)		
		self.rect = pygame.Rect (coordinates, self.size)
		
class Lake(Env):
	def __init__(self, coordinates):
		super().__init__(coordinates)
		self.size = (75,70)
		tempimage = pygame.image.load("res/lake.png").convert()
		self.image = pygame.transform.smoothscale(tempimage, self.size)		
		self.rect = pygame.Rect (coordinates, self.size)

class House(Env):
	def __init__(self, coordinates, team):
		super().__init__(coordinates)
		self.team = team
		self.size = (25,25)
		if self.team == 1:
			path = 'res/house_black.png'
		elif self.team == 2:
			path = 'res/house_blue.png'
		else:
			path = 'res/house_red.png'
		tempimage = pygame.image.load(path).convert()
		self.image = pygame.transform.smoothscale(tempimage, self.size)		
		self.rect = pygame.Rect (coordinates, self.size)
	
	def spawn(self):
		global HUMANS
		global STATS
		if self.team == 1:
			for i in range(1,H1.offspring):
				newHuman = H1 (1, (0,0,0), [self.coordinates[0]+50, self.coordinates[1]+50])
				HUMANS.append(newHuman)
				STATS ['H1'] = STATS ['H1'] + 1 
		elif self.team == 2:
			for i in range(1,H2.offspring):
				newHuman = H2 (2, (0,0,255), [self.coordinates[0]+50, self.coordinates[1]+50])
				HUMANS.append(newHuman)
				STATS ['H2'] = STATS ['H2'] + 1 
		else:
			for i in range(1,H3.offspring):
				newHuman = H3 (3, (255,0,0), [self.coordinates[0]+50, self.coordinates[1]+50])
				HUMANS.append(newHuman)
				STATS ['H3'] = STATS ['H3'] + 1 

class Ruin(Env):
	def __init__(self, coordinates):
		super().__init__(coordinates)
		self.size = (20,20)
		path =  'res/ruin.png'
		tempimage = pygame.image.load(path).convert()
		self.image = pygame.transform.smoothscale(tempimage, self.size)		
		self.rect = pygame.Rect (coordinates, self.size)
		self.counter = 0

def main():
	global screen
	global HUMANS
	global ENVIRONMENT
	global HOUSES
	global STATS
	STATS = {	# TODO: update these
    'H1': 0,
	'H2': 0,
	'H3' : 0,
	'Houses': 0,
	'KILLS': 0,
	'wolves starved' : 0,
	'rabbits starved' : 0 }
	clock = pygame.time.Clock()
	pygame.init()
	screen = pygame.display.set_mode((WIDTH, HEIGHT))
	for i in range (1,3*15+1):
		j = i%3
		if j == 1:
			randCoordinates = [random.randrange(1,WIDTH/3), random.randrange(1, HEIGHT)]
			Human = H1(1, (0,0,0), randCoordinates)
			STATS ['H1'] = STATS['H1'] + 1
		elif j == 2:
			randCoordinates = [random.randrange(WIDTH/3,2*WIDTH/3), random.randrange(1, HEIGHT)]
			Human = H2(2, (0,0,255), randCoordinates)
			STATS ['H2'] = STATS['H2'] + 1
		else:
			randCoordinates = [random.randrange(2*WIDTH/3,WIDTH), random.randrange(1, HEIGHT)]
			Human = H3(3, (255,0,0), randCoordinates)
			STATS ['H3'] = STATS['H3'] + 1
		HUMANS.append (Human)
	
	Lake1 = Lake((0,HEIGHT-60))
	Lake2 = Lake((70,HEIGHT-70))
	Lake3 = Lake((350,80))
	Mountain1 = Mountain((600, 80))
	Mountain2 = Mountain((692, 65))
	House1 = House ((random.randrange(1,WIDTH/3), random.randrange(1, HEIGHT-90)), 1)
	House2 = House ((random.randrange(WIDTH/3,2*WIDTH/3), random.randrange(300, HEIGHT-40)), 2)
	House3 = House ((random.randrange(2*WIDTH/3,WIDTH), random.randrange(300, HEIGHT-40)), 3)
	ENVIRONMENT.append(Lake1)
	ENVIRONMENT.append(Lake2)
	ENVIRONMENT.append(Lake3)
	ENVIRONMENT.append(Mountain1)
	ENVIRONMENT.append(Mountain2)
	HOUSES.append(House1)
	HOUSES.append(House2)
	HOUSES.append(House3)
	STATS['Houses'] = 3
	THREEKTIMER, t = pygame.USEREVENT+1, 4000
	pygame.time.set_timer(THREEKTIMER, t)
	HOUSETIMER, t2 = pygame.USEREVENT+2, 6000
	pygame.time.set_timer(HOUSETIMER, t2)
	pygame.event.set_allowed([THREEKTIMER, HOUSETIMER]) # not allowing any keyboard input, allegedly improves performance
	caption = 'H1: ' + str(STATS['H1']) + ' H2: ' + str(STATS['H2']) + ' H3: ' + str(STATS['H3']) + ' Houses: ' + str(STATS['Houses']) + ' Kills: ' + str(STATS['KILLS'])
	pygame.display.set_caption(caption)
	while 1:
		screen.fill(BACKGROUND)
		for event in pygame.event.get():
			if event.type == THREEKTIMER:	#	 every 3000 milsec
				caption = 'H1: ' + str(STATS['H1']) + ' H2: ' + str(STATS['H2']) + ' H3: ' + str(STATS['H3']) + ' Houses: ' + str(STATS['Houses']) + ' Kills: ' + str(STATS['KILLS'])
				pygame.display.set_caption(caption)
				for l,house in enumerate(HOUSES):
					house.spawn()
			elif event.type == HOUSETIMER:
				popcounter = 0
				for i,house in enumerate(HOUSES):
					counter1 = 0 
					counter2 = 0
					for l, human in enumerate(HUMANS): # check for nearby humans. house.coordinates in upper right corner of graphic!
						if human.coordinates[0] in range(house.coordinates[0]-55,house.coordinates[0]+81): # house.size = (25,25) 		
							if human.coordinates[1] in range(house.coordinates[1]-55,house.coordinates[1]+81):	
								if human.team == house.team:
									counter1 = counter1 + 1
								else:
									counter2 = counter2 + 1
					#print (str(counter1) + ', ' + str(counter2))
					if counter2 > (2*counter1 + 1):
						newRuin = Ruin(house.coordinates)
						RUINS.append(newRuin)
						HOUSES.pop(i-popcounter)
						popcounter = popcounter + 1
						STATS['Houses'] = STATS['Houses'] - 1
				popcounter = 0
				for i,ruin in enumerate(RUINS):
					ruin.counter = ruin.counter + 1
					if ruin.counter > 3:
						RUINS.pop(i-popcounter)
						popcounter = popcounter + 1
		for i,env in enumerate(ENVIRONMENT):
			screen.blit(env.image, env.rect)
		#testpixel = pygame.Surface((4,4))
		#testpixel.fill ((0,0,0))
		for i,house in enumerate(HOUSES):
			screen.blit(house.image, house.rect)
		for i,ruin in enumerate(RUINS):
			screen.blit(ruin.image, ruin.rect)
		random.shuffle(HUMANS) # mix order of humans
		for i, human in enumerate(HUMANS):
			if human.alive:
				screen.blit(human.pixel, human.coordinates)	# moves the pixel to new coordinates(coordinates moved in class method)
				human.update()
				if not human.alive:
					del HUMANS[i]
		pygame.display.flip()
		clock.tick(15)

if __name__ == "__main__":
	main()