from pygame import gfxdraw

def draw_grid(screen, HEIGHT, WIDTH, block_size):
	"""
	IN: screen: pygame display surface where grid is drawn on
	HEIGHT: height of grid
	WIDTH: width of grid
	block_size: size (=height=width) of the grid rectangles
	
	creates a grid of 25x25 pixel rectangles. There are the boxes which all further elements are aligned on
	creates the boxes by drawing horizontal and vertical lines
	color is greyish (20,20,20) with alpha value 60 for high-transparency
	"""
	
	for z in range(0, int(HEIGHT/block_size)):
		gfxdraw.hline(screen, 0, WIDTH, z*block_size, (20,20,20, 60) ) 
	for x in range(0, int(WIDTH/block_size)):
		gfxdraw.vline(screen, x*block_size, 0, HEIGHT, (20,20,20, 60) )
