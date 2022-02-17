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
V0.1 add first pre-setup machine, first belt
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


class Machine:
	"""
	doc
	"""
	def __init__(self):
		pass
	
	def update(self):
		pass

class BoxAdder(Machine):
	"""
	doc
	"""
	def __init__(self, coordinates):
		self.size = (25,25)
		self.rect = pygame.Rect(coordinates, self.size)
		tempimage = pygame.image.load("res/boxAdder.png").convert()
		self.image = pygame.transform.smoothscale(tempimage, self.size)	
	
	def update(self):
		pass


class Logistics:
	"""
	doc
	"""
	def __init__(self):
		pass
	
	def update(self):
		pass

class Conveyor(Logistics):
	"""
	doc
	"""
	def __init__(self):
		pass
	
	def update(self):
		pass

class BeltConveyor(Conveyor):
	"""
	doc
	"""
	def __init__(self):
		pass
	
	def update(self):
		pass

class RollerConveyor(Conveyor):
	"""
	doc
	"""
	def __init__(self,coordinates):
		self.size = (25,25)
		self.rect = pygame.Rect(coordinates, self.size)
		tempimage = pygame.image.load("res/boxAdder.png").convert()
		self.image = pygame.transform.smoothscale(tempimage, self.size)	
		tempimage = pygame.image.load("res/boxAdder.png").convert()
		self.image = pygame.transform.smoothscale(tempimage, self.size)	
	
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
	clock = pygame.time.Clock()
	pygame.init()
	screen = pygame.display.set_mode((WIDTH, HEIGHT))
	box_adder1 = BoxAdder((50,50))
	MACHINES.append(box_adder1)
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
		pygame.display.flip()
		clock.tick(25)

if __name__ == "__main__":
	main()