import pygame
import pygame.gfxdraw

"""
Goal of this Simulation:
Visualize a HMI for a 2-D factory including manufacturing machines, intralogistics, productivity stats.
[3-D factory by having floors, switch floor with arrows on display]
Either pre-setup or player-based input for layout
Grid-based system (rectangles are 25x25 pixels)   CHANGE?

Available machines: (add them step by step)
box-adder

Available intralogistics elements:
conveyor belt
roller , accumulating roller
robot arm
storage unit
drones?

Available products:
empty box

++V0.0 add grid and visualize
++V0.1 add first pre-setup machine, first belt
V0.1.1 define interfaces and orientation check
V0.2 add empty box
V0.3 add animations to machines, movement to products
V0.4 

V1.2 decorate HUD

"""

WIDTH = 1000	# make sure this matches a factor of block_size from function create_grid! (does right now)
HEIGHT = 400	# make sure this matches a factor of block_size from function create_grid! (does right now)
BACKGROUND = (255, 255, 255)
MACHINES = list()
LOGISTICS = list()
PRODUCTS = list()
IDS = dict()

class PlacementError(Exception):
	def __init__(self, machinetype):
		machine = str(machinetype)
		machine = machine.split('.')[1]
		machine = machine.split('\'')[0]
		print("Can't place " + machine + " here, there is something in the way!")

class Machine:
	"""
	doc
	"""
	def __init__(self, coordinates, ID):
		self.coordinates = coordinates
		self.ID = ID
	
	def update(self):
		pass

class BoxAdder(Machine):
	"""
	doc
	"""
	def __init__(self, coordinates, orientation, ID):
		super().__init__(coordinates, ID)
		self.size = (25,25)
		self.rect = pygame.Rect(coordinates, self.size)
		tempimage = pygame.image.load("res/factory/boxAdder.png").convert()
		self.image = pygame.transform.smoothscale(tempimage, self.size)	
		self.orientation = orientation

	def update(self):
		pass


class Logistics:
	"""
	doc
	"""
	def __init__(self, coordinates, ID):
		self.coordinates = coordinates
		self.ID = ID
	
	def update(self):
		pass

class Conveyor(Logistics):
	"""
	doc
	"""
	def __init__(self, coordinates, ID):
		super().__init__(coordinates, ID)
		self.direction = None	# stores direction of transportation, "up", "down", "left", "right"
		#self.check_orientation()
	
	def update(self):
		pass

	def check_orientation(self):
		if self.direction == None:
			xRange = range (self.coordinates[0]-25, self.coordinates[0] +26)
			yRange = range (self.coordinates[1]-25, self.coordinates[1] +26)
			for i,machine in enumerate(MACHINES):   
				if machine.coordinates[0] in xRange and machine.coordinates[1] in yRange:
					if machine.coordinates == self.coordinates:
						if machine.ID != self.ID:
							raise PlacementError(type(self))
					elif machine.coordinates == (self.coordinates[0]+25, self.coordinates[1]+25):
						pass	# skip machines on diagonally adjacent
					elif machine.coordinates == (self.coordinates[0]-25, self.coordinates[1]-25):
						pass
					else:
						if machine.coordinates[0] == self.coordinates[0]:	# machine above or below
							if machine.orientation == "vertical":			# only changes direction if machine actually facing conveyor
								if machine.coordinates[1] == self.coordinates[1] + 25: # below
									self.direction = "up"
									#image correct orientation from loading
								else:	# above
									self.direction = "down"
									self.image = pygame.transform.flip(self.image, True, False)
									self.image1 = pygame.transform.flip(self.image1, True, False)
						else:	# machine left or right
							if machine.orientation == "horizontal":		# only changes direction if machine actually facing conveyor
								if machine.coordinates[0] == self.coordinates[0] + 25: # right
									self.direction = "left"
									self.image = pygame.transform.rotate(self.image, 270)
									self.image1 = pygame.transform.rotate(self.image1, 270)
								else:	# left
									self.direction = "right"
									self.image = pygame.transform.rotate(self.image, 90)
									self.image1 = pygame.transform.rotate(self.image1, 90)
						break
			for i,logistic in enumerate(LOGISTICS):  
				if logistic.coordinates[0] in xRange and logistic.coordinates[1] in yRange:
					if logistic.coordinates == self.coordinates:
						if logistic.ID != self.ID:
							raise PlacementError(type(self))
					elif logistic.coordinates == (self.coordinates[0]+25, self.coordinates[1]+25):
						pass	# skip machines on diagonally adjacent
					elif logistic.coordinates == (self.coordinates[0]-25, self.coordinates[1]-25):
						pass
					else:
						if logistic.coordinates[0] == self.coordinates[0]:	# logistic above or below
							if logistic.coordinates[1] == self.coordinates[1] + 25: # below
								self.direction = "up"
								#image correct orientation from loading
							else:	# above
								self.direction = "down"
								self.image = pygame.transform.flip(self.image, True, False)
								self.image1 = pygame.transform.flip(self.image1, True, False)
						else:	# logistic left or right
							if logistic.coordinates[0] == self.coordinates[0] + 25: # right
								self.direction = "left"
								self.image = pygame.transform.rotate(self.image, 270)
								self.image1 = pygame.transform.rotate(self.image1, 270)
							else:	# left
								self.direction = "right"
								self.image = pygame.transform.rotate(self.image, 90)
								self.image1 = pygame.transform.rotate(self.image1, 90)
						break
 			#copy paste adapt for LOGISTICS
					
					
		else:	# don't change orientation if already set
			pass

class BeltConveyor(Conveyor):
	"""
	doc
	"""
	def __init__(self,coordinates, ID):
		pass
	
	def update(self):
		pass

class RollerConveyor(Conveyor):
	"""
	doc
	"""
	def __init__(self,coordinates, ID):
		super().__init__(coordinates, ID)
		self.size = (25,25)
		self.rect = pygame.Rect(coordinates, self.size)
		tempimage = pygame.image.load("res/factory/rollerConveyor.png").convert()
		self.image = pygame.transform.smoothscale(tempimage, self.size)	
		tempimage = pygame.image.load("res/factory/rollerConveyor1.png").convert()
		self.image1 = pygame.transform.smoothscale(tempimage, self.size)	
		self.check_orientation()	# can only be called here since in class __init__ the images are not yet set
	
	def update(self):
		pass

class RobotArm(Logistics):
	"""
	doc
	"""
	def __init__(self):
		pass
	
	def update(self):
		pass

class StorageUnit(Logistics):
	"""
	doc
	"""
	def __init__(self):
		pass
	
	def update(self):
		pass

class Product:
	"""
	doc
	"""
	def __init__(self):
		pass
	
	def update(self):
		pass

def create_grid(screen):
	"""
	creates a grid of 25x25 pixel rectangles. There are the boxes which all further elements are aligned on
	creates the boxes by drawing horizontal and vertical lines
	color is greyish (20,20,20) with alpha value 60 for high-transparency
	"""
	block_size = 25 
	for z in range(0, int(HEIGHT/block_size)):
		pygame.gfxdraw.hline(screen, 0, WIDTH, z*block_size, (20,20,20, 60) ) 
	for x in range(0, int(WIDTH/block_size)):
		pygame.gfxdraw.vline(screen, x*block_size, 0, HEIGHT, (20,20,20, 60) )

def main():
	global MACHINES
	global LOGISTICS
	global PRODUCTS
	global IDS
	clock = pygame.time.Clock()
	pygame.init()
	screen = pygame.display.set_mode((WIDTH, HEIGHT))
	box_adder1 = BoxAdder((50,50), "horizontal", "0000")
	MACHINES.append(box_adder1)
	IDS["0000"] = type(box_adder1)

	roller1 = RollerConveyor((75,50), "0001")
	LOGISTICS.append(roller1)
	IDS["0001"] = type(roller1)
	roller2 = RollerConveyor((100,50), "0002")
	LOGISTICS.append(roller2)
	IDS["0002"] = type(roller2)
	roller3 = RollerConveyor((100,75), "0003")
	LOGISTICS.append(roller3)
	IDS["0003"] = type(roller3)
	XYTIMER, t = pygame.USEREVENT+1, 4000
	pygame.time.set_timer(XYTIMER, t)
	caption = 'FactorySim'
	pygame.display.set_caption(caption)
	while 1:
		screen.fill(BACKGROUND)
		create_grid(screen)
		for event in pygame.event.get():
			if event.type == XYTIMER:
				pass
		for i,machine in enumerate(MACHINES):
			screen.blit(machine.image, machine.rect)
		for i,entity in enumerate(LOGISTICS):
			screen.blit(entity.image, entity.rect)	
		pygame.display.flip()
		clock.tick(25)

if __name__ == "__main__":
	main()