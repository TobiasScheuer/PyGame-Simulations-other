import pygame
import pygame.gfxdraw
import random

"""
Goal of this Simulation:
Visualize a HMI for a 2-D factory including manufacturing machines, intralogistics, productivity stats.
[3-D factory by having floors, switch floor with arrows on display]
Either pre-setup or player-based input for layout
Grid-based system (rectangles are 25x25 pixels)   CHANGE?

Available machines: (add them step by step)
product-adder
storage unit

Available intralogistics elements:
conveyor belt
roller , accumulating roller
robot arm
drones?

Available products:
empty box
bottles

++V0.0 add grid and visualize
++V0.1 add first pre-setup machine, first belt
++V0.1.1 define interfaces and orientation check
++V0.2 add empty box
++V0.3 add animations to machines, movement to products
+V0.4 expand setup -> more machines, more conveyors, more boxes, more products, actual production
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
	def __init__(self, machinetype, coordinates, entity):
		machine = str(machinetype)
		machine = machine.split('.')[1]
		machine = machine.split('\'')[0]
		if isinstance(entity, str) == False:
			entity = str(entity)
		print("Can't place " + machine + " at " + str(coordinates) + ", because of " + entity)

class Resources:
	"""
	doc
	"""
	def check_coordinates(self, coordinates):
		if coordinates[0] < 0 or coordinates[0] > WIDTH:
			raise PlacementError(type(self), coordinates, "horizontal coordinate bounds")
		elif coordinates[1] < 0 or coordinates[1] > HEIGHT:
			raise PlacementError(type(self), coordinates, "vertical coordinate bounds")
		for i, entity in enumerate(LOGISTICS+MACHINES):
			if coordinates == entity.coordinates:
				raise PlacementError(type(self), coordinates, entity)

	def generate_ID(self):
		ID = str(random.randint(1,9999))
		while len(ID) < 4:
			ID = "0" + ID
		while ID in IDS.keys():
			ID = str(random.randint(1,9999))
			while len(ID) < 4:
				ID = "0" + ID
		self.ID = ID

	def __init__(self, coordinates):
		self.check_coordinates(coordinates)
		self.coordinates = coordinates
		self.generate_ID()
		IDS[self.ID] = type(self)
		self.input_rect = list()		# a list of 25x3 rect  
		self.output_rect = list()		# a list of 25x3 rect  

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

	
class Machine(Resources):
	"""
	doc
	"""
	def __init__(self, coordinates):
		super().__init__(coordinates)
		pass

class ProductAdder(Machine):
	"""
	doc
	"""
	def __init__(self, coordinates, orientation, product):
		super().__init__(coordinates)
		self.size = (25,25)
		self.rect = pygame.Rect(coordinates, self.size)
		self.product = product
		if product == "boxes":
			tempimage = pygame.image.load("res/factory/boxAdder.png").convert()
		elif product == "bottles":
			tempimage = pygame.image.load("res/factory/bottleAdder.png").convert()
		self.image = pygame.transform.smoothscale(tempimage, self.size)	
		self.orientation = orientation
		if orientation == "horizontal":
			output_right = pygame.Rect((coordinates[0]+24, coordinates[1]), (3,25))
			self.output_rect.append(output_right)
			output_left = pygame.Rect((coordinates[0]-1, coordinates[1]), (3,25))
			self.output_rect.append(output_left)
			
		elif orientation == "vertical":
			output_up = pygame.Rect((coordinates[0], coordinates[1]-3), (25,3))
			self.output_rect.append(output_up)
			output_down = pygame.Rect((coordinates[0], coordinates[1]+24), (25,3))
			self.output_rect.append(output_down)

	def update(self):
		counter = 0
		for i, logistic in enumerate(LOGISTICS):
			coordinates = (0,0)
			if self.orientation == "horizontal":
				if self.output_rect[0] in logistic.input_rect:	# right output
					coordinates = (self.output_rect[0][0], self.output_rect[0][1] )			
				elif self.output_rect[1] in logistic.input_rect:
					coordinates = (self.output_rect[1][0]-19, self.output_rect[1][1] )
			else:			#vertical
				if self.output_rect[0] in logistic.input_rect:	# top output
					coordinates = (self.output_rect[0][0], self.output_rect[0][1]-19 )			
				elif self.output_rect[1] in logistic.input_rect:
					coordinates = (self.output_rect[1][0], self.output_rect[1][1]-1 )
			if coordinates != (0,0):
				self.generate_ID()
				if self.product == "boxes":
					newProduct = Box(coordinates)
				elif self.product == "bottles":
					newProduct = Bottles(coordinates)
				PRODUCTS.append(newProduct)
				counter += 1
			if counter == 2:
				break
		

class StorageUnit(Machine):
	"""
	doc
	"""
	def __init__(self, coordinates):
		super().__init__(coordinates)
		self.size = (25,25)
		self.rect = pygame.Rect(coordinates, self.size)
		tempimage = pygame.image.load("res/factory/storage.png").convert()
		self.image = pygame.transform.smoothscale(tempimage, self.size)
		self.get_interfaces()
	
	def update(self):
		pass

class Logistics(Resources):
	"""
	doc
	"""
	def __init__(self, coordinates):
		super().__init__(coordinates)
		pass

class Conveyor(Logistics):
	"""
	doc
	"""
	def __init__(self, coordinates):
		super().__init__(coordinates)
		self.direction = None	# stores direction of transportation, "up", "down", "left", "right"
		#self.check_orientation()
	
	def update(self):
		pass	

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
				for i, machine in enumerate(MACHINES):
					if machine.coordinates in possible_neighbours:
						hits.append(machine.coordinates)
				if len(hits) > 2 and isinstance(self, RollerConveyor): #1D Roller Conveyor supposed to only have 2 neighbors
					raise PlacementError(type(self), self.coordinates, "too many neighbours")
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
								self.image = pygame.transform.rotate(self.image, 90)
								self.image1 = pygame.transform.rotate(self.image1, 90)
								break
						elif hits[k][0] > self.coordinates[0]: # neighbour on the right flank
							if input.left > self.coordinates[0]: # input on the right flank
								pass
							else:
								output_rect = pygame.Rect((self.coordinates[0]+24, self.coordinates[1]),(3,25))
								self.direction = "right"
								self.image = pygame.transform.rotate(self.image, 270)
								self.image1 = pygame.transform.rotate(self.image1, 270)
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
								self.image = pygame.transform.flip(self.image, False, True)
								self.image1 = pygame.transform.flip(self.image1, False, True)
								break
						else:
							print('error3')
					if not output_rect == False:
						if output_rect not in self.output_rect: 
							self.output_rect.append(output_rect)
			elif len(self.input_rect) == 2:
				pass
			elif len(self.input_rect) == 3:
				if isinstance(self, TIntersection):
					poss1 = pygame.Rect(self.coordinates[0]-1, self.coordinates[1], 3, 25)
					poss2 = pygame.Rect(self.coordinates[0]+24, self.coordinates[1], 3, 25)
					poss3 = pygame.Rect(self.coordinates[0], self.coordinates[1]-1, 25, 3)
					poss4 = pygame.Rect(self.coordinates[0], self.coordinates[1]+24, 25, 3)
					possible_interfaces = [poss1, poss2, poss3, poss4]
					for i in range(0,4):
						if not possible_interfaces[i] in self.input_rect:
							self.output_rect.append(possible_interfaces[i])
							if i == 0:
								self.direction = "left"
								self.image = pygame.transform.rotate(self.image, 90)
								self.image1 = pygame.transform.rotate(self.image1, 90)
							elif i == 1:
								self.direction = "right"
								self.image = pygame.transform.rotate(self.image, 270)
								self.image1 = pygame.transform.rotate(self.image1, 270)
							elif i == 2:
								self.direction = "up"
								#image correct orientation from loading
							else:
								self.direction = "down"
								self.image = pygame.transform.flip(self.image, False, True)
								self.image1 = pygame.transform.flip(self.image1, False, True)
							break
			else:
				print('error1')
				# TODO: create actual error

class BeltConveyor(Conveyor):
	"""
	doc
	"""
	def __init__(self,coordinates):
		pass
	
	def update(self):
		pass

class RollerConveyor(Conveyor):
	"""
	doc
	"""
	def __init__(self,coordinates):
		super().__init__(coordinates)
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
	2/3 inputs, 1 output, if 2 inputs direction needs to be specified (otherwise type None for automatic orientation)
	"""
	def __init__(self,coordinates, direction):
		super().__init__(coordinates)
		tempimage = pygame.image.load("res/factory/TIntersection.png").convert()
		self.image = pygame.transform.smoothscale(tempimage, self.size)	
		tempimage1 = pygame.image.load("res/factory/TIntersection1.png").convert()
		self.image1 = pygame.transform.smoothscale(tempimage1, self.size)	
		self.direction = direction
		if direction == "up":
			output_interface = pygame.Rect((coordinates[0], coordinates[1]-1), (25,3))
			#picture correct orientation
		elif direction == "down":
			output_interface = pygame.Rect((coordinates[0], coordinates[1]+24), (25,3))
			self.image = pygame.transform.flip(self.image, False, True)
			self.image1 = pygame.transform.flip(self.image1, False, True)
		elif direction == "left":
			output_interface = pygame.Rect((coordinates[0]-1, coordinates[1]), (3,25))
			self.image = pygame.transform.rotate(self.image, 270)
			self.image1 = pygame.transform.rotate(self.image1, 270)
		elif direction == "right":
			output_interface = pygame.Rect((coordinates[0]+24, coordinates[1]), (3,25))
			self.image = pygame.transform.rotate(self.image, 90)
			self.image1 = pygame.transform.rotate(self.image1, 90)
		if direction != None:
			self.output_rect.append(output_interface)
		self.get_interfaces()
		self.check_orientation()	# can only be called here since in class __init__ the images are not yet set
		
		
			
	
	def update(self):
		pass

class RobotArm(Logistics):
	"""
	doc
	"""
	def __init__(self,coordinates):
		super().__init__(coordinates)
		self.size = (25,25)
		self.rect = pygame.Rect(coordinates, self.size)
		self.images = dict()
		for i in range(0,8):
			path = "res/factory/robotArm/robotArm" + str(i+1) + ".png"
			tempimage = pygame.image.load(path).convert()
			self.images[i+1] = pygame.transform.smoothscale(tempimage, self.size)		
		self.image = self.images[1]
		self.direction = "right"
		poss1 = pygame.Rect(self.coordinates[0]-1, self.coordinates[1], 3, 25)
		poss2 = pygame.Rect(self.coordinates[0]+24, self.coordinates[1], 3, 25)
		poss3 = pygame.Rect(self.coordinates[0], self.coordinates[1]-1, 25, 3)
		poss4 = pygame.Rect(self.coordinates[0], self.coordinates[1]+24, 25, 3)	
		self.input_rects = self.output_rects = [poss1, poss2, poss3, poss4]
	
	def update(self):
		if self.direction == "up":
			self.image = self.images[1]
		elif self.direction == "down":
			self.image = self.images[5]
		elif self.direction == "left":
			self.image = self.images[7]
		elif self.direction == "right":
			self.image = self.images[3]


class Product:
	"""
	doc
	"""
	def generate_ID(self):
		ID = str(random.randint(1,9999))
		while len(ID) < 4:
			ID = "0" + ID
		while ID in IDS.keys():
			ID = str(random.randint(1,9999))
			while len(ID) < 4:
				ID = "0" + ID
		self.ID = ID

	def __init__(self, coordinates):
		self.generate_ID()
		IDS[self.ID] = type(self)
		self.busy = False
	
	def update(self):
		if self.busy == False:
			upc = 0
			downc = 0
			leftc = 0
			rightc = 0
			xcenter = self.rect[0] + int(self.size[0]*0.5)
			ycenter = self.rect[1] + int(self.size[1]*0.5)
			xline = ((self.rect[0], ycenter ) , ( self.rect[0] + self.size[0],  ycenter))
			yline = ((xcenter, self.rect[1] ) , ( xcenter, self.rect[1]+self.size[1]))
			collision = False
			for i,logistic in enumerate(LOGISTICS):
				if logistic.direction == "up" or logistic.direction == "down":
					yclip = logistic.rect.clipline(yline) #yclip containts line part coordinates which is in logistic rect
					if yclip:	# evaluates if yclip has contents and there is inside the 
						if logistic.direction == "up":
							if upc == 0:
								collision_box = pygame.Rect(self.rect[0], self.rect[1]-3, self.size[0], self.size[1]+3)
								for i, product in enumerate(PRODUCTS):
									if product.rect.colliderect(collision_box) == True and not product.rect == self.rect:
										collision = True
										break
								if collision == False:
									self.rect = self.rect.move(0,-1)
								upc += 1
						elif logistic.direction == "down":
							if downc == 0:
								collision_box = pygame.Rect(self.rect[0], self.rect[1], self.size[0], self.size[1]+3)
								for i, product in enumerate(PRODUCTS):
									if product.rect.colliderect(collision_box) == True and not product.rect == self.rect:
										collision = True
										break
								if collision == False:
									self.rect = self.rect.move(0,1)
								downc += 1
				else:
					xclip = logistic.rect.clipline(xline) #yclip containts line part coordinates which is in logistic rect
					if xclip:	# evaluates if yclip has contents and there is inside the 
						if logistic.direction == "left":
							if leftc == 0:
								collision_box = pygame.Rect(self.rect[0]-3, self.rect[1], self.size[0]+3, self.size[1])
								for i, product in enumerate(PRODUCTS):
									if product.rect.colliderect(collision_box) == True and not product.rect == self.rect:
										collision = True
										break
								if collision == False:
									self.rect = self.rect.move(-1,0)
								leftc += 1
						elif logistic.direction == "right":
							if rightc == 0:
								collision_box = pygame.Rect(self.rect[0], self.rect[1], self.size[0]+3, self.size[1])
								for i, product in enumerate(PRODUCTS):
									if product.rect.colliderect(collision_box) == True and not product.rect == self.rect:
										collision = True
										break
								if collision == False:
									self.rect = self.rect.move(1,0)
								rightc += 1
			machine_index = self.rect.collidelist(MACHINES)
			if machine_index >= 0:
				machine = MACHINES[machine_index]
				if isinstance(machine, StorageUnit):
					self.rect.update((machine.coordinates[0]+3, machine.coordinates[1]+3), self.size)
					self.busy = True

class Box(Product):
	"""
	doc
	"""
	def __init__(self, coordinates):
		super().__init__(coordinates)
		self.size = (19,17)
		self.rect = pygame.Rect((coordinates[0]+3, coordinates[1]+3), self.size)
		tempimage = pygame.image.load("res/factory/box.png").convert_alpha()
		self.image = pygame.transform.smoothscale(tempimage, self.size)	
		self.content = None

class Bottles(Product):
	"""
	doc
	"""
	def __init__(self, coordinates):
		super().__init__(coordinates)
		self.size = (19,17)
		self.rect = pygame.Rect((coordinates[0]+3, coordinates[1]+3), self.size)
		tempimage = pygame.image.load("res/factory/bottles.png").convert_alpha()
		self.image = pygame.transform.smoothscale(tempimage, self.size)
		tempimage = pygame.image.load("res/factory/boxedBottles.png").convert_alpha()
		self.image_boxed = pygame.transform.smoothscale(tempimage, self.size)
		


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
	box_adder1 = ProductAdder((50,50), "horizontal", "boxes")
	MACHINES.append(box_adder1)
	box_adder2 = ProductAdder((175,50), "horizontal", "boxes")
	MACHINES.append(box_adder2)
	bottle_adder1 = ProductAdder((100,0), "vertical", "bottles")
	MACHINES.append(bottle_adder1)
	bottle_adder2 = ProductAdder((350,100), "vertical", "bottles")
	MACHINES.append(bottle_adder2)
	storage1 = StorageUnit((75,150))
	MACHINES.append(storage1)
	storage2 = StorageUnit((325,200))
	MACHINES.append(storage2)

	roller_coordinates = [(75,50), (100,75), (100,100), (75,100), (75,125), (125,50), (100,25), (150,50)]
	roller_coordinates2 = [(350,75), (375,75), (400,75), (400,100), (400,125), (400,150), (375,150), (350,150), (325,175)]
	merged_lists = roller_coordinates+roller_coordinates2
	for i in range(0,len(merged_lists)):
		new_roller = RollerConveyor(merged_lists[i])
		LOGISTICS.append(new_roller)
	TIntersection1 = TIntersection((100,50), None)
	LOGISTICS.append(TIntersection1)
	robotArm1 = RobotArm((300,150))
	LOGISTICS.append(robotArm1)
	TIntersection2 = TIntersection((325,150), "down")
	LOGISTICS.append(TIntersection2)

	box1 = Box((75,50))
	PRODUCTS.append(box1)
	bottles1 = Bottles((350,75))
	PRODUCTS.append(bottles1)
	BOXTIMER, t = pygame.USEREVENT+1, 4000
	pygame.time.set_timer(BOXTIMER, t)
	caption = 'FactorySim'
	pygame.display.set_caption(caption)
	counter = 0
	for j in range(0,len(LOGISTICS)+3):
		for i,entity in enumerate(LOGISTICS):
			if isinstance(entity, Conveyor):
				entity.get_interfaces()
				entity.check_orientation()
	for i, machine in enumerate(MACHINES):
			machine.get_interfaces()
	while 1:
		screen.fill(BACKGROUND)
		create_grid(screen)
		for event in pygame.event.get():
			if event.type == BOXTIMER:
				for i,machine in enumerate(MACHINES):
					machine.update()
				#print(IDS.keys())
		for i,machine in enumerate(MACHINES):
				screen.blit(machine.image, machine.rect)
		if counter == 0:
			for i,entity in enumerate(LOGISTICS):
				screen.blit(entity.image, entity.rect)	
			counter = 1
		else:
			for i,entity in enumerate(LOGISTICS):
				if isinstance(entity, Conveyor):
					screen.blit(entity.image1, entity.rect)	
				else:
					screen.blit(entity.image, entity.rect)
					entity.update()
			counter = 0		
		for i,product in enumerate(PRODUCTS):
				screen.blit(product.image, product.rect)
				product.update()

		pygame.display.flip()
		clock.tick(24)
		#slow-mo:
		#clock.tick(5)

if __name__ == "__main__":
	main()