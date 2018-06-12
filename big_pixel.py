import pygame

class BigPixel():
	
	def __init__(self, ai_settings, screen):
		self.ai_settings = ai_settings
		self.screen = screen
		
		self.size = ai_settings.pixel_size
		self.show = False
		self.set_color()
		# O_pos is in real pixels
		self.set_O_pos()
		# positions are measured in big pixels
		self.set_pos()
		
		self.get_real_pos()
			
	def set_pos(self, pos=(0,0)):
		self.pos = pos
		self.pos_x = pos[0]
		self.pos_y = pos[1]
	
	def set_O_pos(self, posO=(0,0)):
		self.pos_o = posO
		self.o_x = posO[0]
		self.o_y = posO[1]	
			
	def set_color(self, new_color=(255,255,255)):
		self.color = new_color
	
	def get_real_pos(self):
		self.real_x = self.pos_x*self.ai_settings.pixel_step + self.o_x
		self.real_y = self.pos_y*self.ai_settings.pixel_step + self.o_y
		self.real_pos = (self.real_x, self.real_y)
		
	def draw_pixel(self):
		self.rect = pygame.Rect(self.real_x, self.real_y, self.size, 
			self.size)		
		if self.show:
			pygame.draw.rect(self.screen, self.color, self.rect)		
