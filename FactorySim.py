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
++V0.1.1 define interfaces and orientation check
++V0.2 add empty box
++V0.3 add animations to machines, movement to products
V0.4 expand setup -> more machines, more conveyors, more boxes, more products, actual production
V0.5a switch to player based layout
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
		self.input_rect = list()		# a list of 25x3 rect  
		self.output_rect = list()		# a list of 25x3 rect 
	
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
		if orientation == "horizontal":
			output_right = pygame.Rect((coordinates[0]+24, coordinates[1]), (3,25))
			self.output_rect.append(output_right)
			output_left = pygame.Rect((coordinates[0]-1, coordinates[1]), (3,25))
			self.output_rect.append(output_left)
		elif orientation == "vertical":
			output_up = pygame.Rect((coordinates[0], coordinates[1]-1), (25,3))
			self.output_rect.append(output_up)
			output_down = pygame.Rect((coordinates[0], coordinates[1]+24), (25,3))
			self.output_rect.append(output_down)

	def update(self):
		pass


class Logistics:
	"""
	doc
	"""
	def __init__(self, coordinates, ID):
		self.coordinates = coordinates
		self.ID = ID
		self.input_rect = list()	# max 3 inputs, 25x3 rects
		self.output_rect = list()	# max 3 outputs, 25x3 rects
	
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

	def get_interfaces(self):
		"""
		goes through all currently existing machines and logistic elements,
		if one of their output interfaces overlap with own rect -> interface found -> add to own input interfaces
		"""
		for i,machine in enumerate(MACHINES):
			outputlist_indexes = self.rect.collidelistall(machine.output_rect)
			if len(outputlist_indexes) > 0:
				for j in range(0, len(outputlist_indexes)):
					if machine.output_rect[outputlist_indexes[j]] not in self.input_rect:
						self.input_rect.append(machine.output_rect[outputlist_indexes[j]])
		for i,logistic in enumerate(LOGISTICS):
			if logistic.coordinates == self.coordinates:
				pass
			else:
				outputlist_indexes = self.rect.collidelistall(logistic.output_rect)
				if len(outputlist_indexes) > 0:
					for j in range(0, len(outputlist_indexes)):
						if logistic.output_rect[outputlist_indexes[j]] not in self.input_rect:
							self.input_rect.append(logistic.output_rect[outputlist_indexes[j]])

	def check_orientation(self):
		if self.direction == None:
			if len(self.input_rect) == 0:
				pass
			elif len(self.input_rect) == 1:
				input = self.input_rect[0]
				possible_neighbours = [(self.coordinates[0]-25,self.coordinates[1]), (self.coordinates[0]+25,self.coordinates[1]), (self.coordinates[0],self.coordinates[1]+25), (self.coordinates[0],self.coordinates[1]-25)]
				hits = list()
				for i,logistic in enumerate(LOGISTICS):
					if logistic.coordinates in possible_neighbours:
						hits.append(logistic.coordinates)
				if len(hits) > 2:
					raise PlacementError
				elif len(hits) <= 0:
					pass
				else:
					output_rect = False
					for k in range (0,len(hits)):
						if hits[k][0] < self.coordinates[0]: # neighbour on left flank
							if input.left < self.coordinates[0]: # input on left flank
								pass
							else: # input not on left flank -> has to be output
								output_rect = pygame.Rect((self.coordinates[0]-1, self.coordinates[1]),(3,25))
								self.direction = "left"
								self.image = pygame.transform.rotate(self.image, 270)
								self.image1 = pygame.transform.rotate(self.image1, 270)
								break
						elif hits[k][0] > self.coordinates[0]: # neighbour on the right flank
							if input.left > self.coordinates[0]: # input on the right flank
								pass
							else:
								output_rect = pygame.Rect((self.coordinates[0]+24, self.coordinates[1]),(3,25))
								self.direction = "right"
								self.image = pygame.transform.rotate(self.image, 90)
								self.image1 = pygame.transform.rotate(self.image1, 90)
								break
						elif hits[k][1] < self.coordinates[1]: # neighbour above
							if input.top < self.coordinates[1]: # input above
								pass
							else:
								output_rect = pygame.Rect((self.coordinates[0], self.coordinates[1]-1),(25,3))
								self.direction = "up"
								#image correct orientation from loading
								break
						elif hits[k][1] > self.coordinates[1]:
							if input.top > self.coordinates[1]:
								pass
							else:
								output_rect = pygame.Rect((self.coordinates[0], self.coordinates[1]+24),(25,3))
								self.direction = "down"
								self.image = pygame.transform.flip(self.image, True, False)
								self.image1 = pygame.transform.flip(self.image1, True, False)
								break
						else:
							print('error3')
					if not output_rect == False:
						if output_rect not in self.output_rect: 
							self.output_rect.append(output_rect)
			elif len(self.input_rect) == 2:
				pass
			elif len(self.input_rect) == 3:
				pass
			else:
				print('error1')
				# TODO: create actual error

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
		tempimage1 = pygame.image.load("res/factory/rollerConveyor1.png").convert()
		self.image1 = pygame.transform.smoothscale(tempimage1, self.size)	
		self.get_interfaces()
		self.check_orientation()	# can only be called here since in class __init__ the images are not yet set
			
	
	def update(self):
		pass

class TIntersection(RollerConveyor):
	"""
	2 inputs, 1 output, needs specified direction during init
	"""
	def __init__(self,coordinates, ID, direction):
		super().__init__(coordinates, ID)
		self.direction = direction
		if direction == "up":
			output_up = pygame.Rect((coordinates[0], coordinates[1]-1), (25,3))
			self.output_rect.append(output_up)
		elif direction == "down":
			output_down = pygame.Rect((coordinates[0], coordinates[1]+24), (25,3))
			self.output_rect.append(output_down)
		elif direction == "left":
			output_left = pygame.Rect((coordinates[0]-1, coordinates[1]), (3,25))
			self.output_rect.append(output_left)
		elif direction == "right":
			output_right = pygame.Rect((coordinates[0]+24, coordinates[1]), (3,25))
			self.output_rect.append(output_right)
		self.get_interfaces()
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
	def __init__(self, coordinates, ID):
		self.ID = ID
	
	def update(self):
		transporter_index = self.rect.collidelist(LOGISTICS)
		if transporter_index >= 0:
			transporter = LOGISTICS[transporter_index]
			if transporter.direction == "up":
				self.rect = self.rect.move(0,-1)
			elif transporter.direction == "down":
				self.rect = self.rect.move(0,1)
			elif transporter.direction == "left":
				self.rect = self.rect.move(-1,0)
			elif transporter.direction == "right":
				self.rect = self.rect.move(1,0)
			else:
				print(transporter)
				print("error")	# TODO: add actual Error

class Box(Product):
	"""
	doc
	"""
	def __init__(self, coordinates, ID):
		super().__init__(coordinates, ID)
		self.size = (19,18)
		self.rect = pygame.Rect((coordinates[0]+3, coordinates[1]+3), self.size)
		tempimage = pygame.image.load("res/factory/box.png").convert()
		self.image = pygame.transform.smoothscale(tempimage, self.size)	


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
	box1 = Box((75,50), "0004")
	for i,entity in enumerate(LOGISTICS):
		print(entity.input_rect)
		print(entity.output_rect)
		entity.get_interfaces()
		entity.check_orientation()
		print(entity.input_rect)
		print(entity.output_rect)
	for i,entity in enumerate(LOGISTICS):
		print(entity.input_rect)
		print(entity.output_rect)
		entity.get_interfaces()
		entity.check_orientation()
		print(entity.input_rect)
		print(entity.output_rect)
	for i,entity in enumerate(LOGISTICS):
		print(entity.direction)
	PRODUCTS.append(box1)
	IDS["0004"] = type(box1)
	XYTIMER, t = pygame.USEREVENT+1, 4000
	pygame.time.set_timer(XYTIMER, t)
	caption = 'FactorySim'
	pygame.display.set_caption(caption)
	counter = 0
	while 1:
		screen.fill(BACKGROUND)
		create_grid(screen)
		for event in pygame.event.get():
			if event.type == XYTIMER:
				pass
		for i,machine in enumerate(MACHINES):
				screen.blit(machine.image, machine.rect)
		if counter == 0:
			for i,entity in enumerate(LOGISTICS):
				screen.blit(entity.image, entity.rect)	
			counter = 1
		else:
			for i,entity in enumerate(LOGISTICS):
				screen.blit(entity.image1, entity.rect)	
			counter = 0		
		for i,product in enumerate(PRODUCTS):
				screen.blit(product.image, product.rect)
				product.update()

		pygame.display.flip()
		clock.tick(25)

if __name__ == "__main__":
	main()