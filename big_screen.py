from big_pixel import BigPixel

class BigScreen():
	
	def __init__(self, ai_settings, screen):
		self.ai_settings = ai_settings
		self.screen = screen
		
		self.set_screen_pos()
		self.set_screen_scale()
		
		self.init_pixel_list()
	
	def set_screen_pos(self, pos=(0,0)):
		self.pos = pos
		self.pos_x = pos[0]
		self.pos_y = pos[1]
		
	def set_screen_scale(self, width=10, height=10):
		self.width_pixel = width
		self.height_pixel = height
		self.init_pixel_list()
			
	def init_pixel_list(self):
		self.pixel_list = []
		for y_index in range(self.height_pixel):
			for x_index in range(self.width_pixel):
				new_pixel = BigPixel(self.ai_settings, self.screen)
				new_pixel.set_O_pos(self.pos)
				new_pixel.set_pos((x_index, y_index))
				new_pixel.get_real_pos()
				self.pixel_list.append(new_pixel)
	
	def p_index(self, x=0, y=0):
		return x + y*self.width_pixel
		
	def set_pixel(self, x=0, y=0, if_show=False, color=(255,255,255), width=0):
		if x < self.width_pixel and y < self.height_pixel and\
			x >= 0 and y >= 0:
			new_pixel = BigPixel(self.ai_settings, self.screen)
			new_pixel.set_O_pos(self.pos)
			new_pixel.set_pos((x, y))
			new_pixel.get_real_pos()
			new_pixel.show = if_show
			new_pixel.set_color(color)
			new_pixel.set_width(width)
			self.pixel_list[self.p_index(x,y)] = new_pixel
	
	def draw_screen(self):
		for pixel in self.pixel_list:
			pixel.draw_pixel()

	def clear_screen(self):
		for pixel in self.pixel_list:
			pixel.show = False
			pixel.color = (255,255,255)
			
	def fill_screen(self, color=(255,255,255)):
		for pixel in self.pixel_list:
			pixel.show = True
			pixel.set_color(color)
			
	def draw_line(self, x1, y1, x2=0, y2=0):
		# TODO
		self.clear_screen()
