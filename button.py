import pygame

class Button():

	def __init__(self, ai_settings, screen, stats, msg_list, top,
		centerx):
		self.ai_settings = ai_settings
		self.screen = screen
		self.stats = stats
		
		self.msg_list = msg_list
		self.top = top
		self.centerx = centerx
		
		self.set_size()
		self.button_color = ai_settings.bg_color
		self.frame_color = ai_settings.frame_color
		self.text_color = (255,255,255)
		self.font = pygame.font.SysFont('arial', 20, bold=True)

		self.prep_msg()
		
		self.click_time = 0
	
	def set_size(self, width=86, height=30):
		self.width, self.height = width, height
		self.prep_button()
		
	def prep_button(self):
		self.frame_rect = pygame.Rect(0, 0, self.width, self.height)
		self.frame_rect.centerx = self.centerx
		self.frame_rect.top = self.top
		self.button_rect = pygame.Rect(0, 0, self.width-6,
			self.height-6)
		self.button_rect.center = self.frame_rect.center
		self.rect = self.button_rect
		
	def set_center(self, center):
		self.frame_rect.center = center
		self.button_rect.center = self.frame_rect.center
					
	def prep_msg(self):
		next_top = self.button_rect.top
		self.msg_image = []
		self.msg_image_rect = []
		for msg in self.msg_list:
			msg_image = self.font.render(msg, False,
				self.text_color, self.ai_settings.bg_color)
			msg_image_rect = msg_image.get_rect()
			msg_image_rect.centerx = self.frame_rect.centerx
			msg_image_rect.top = next_top
			next_top = msg_image_rect.bottom
			self.msg_image.append(msg_image)
			self.msg_image_rect.append(msg_image_rect)
		
	def update_msg(self, new_msg_list):
		self.msg_list = new_msg_list
		self.prep_msg()
		
	def update_top(self, new_top):
		self.top = new_top
		self.prep_button()
		self.prep_msg()
				
	def draw_button(self):
		if self.msg_list:
			self.screen.fill(self.frame_color, self.frame_rect)
			self.screen.fill(self.button_color, self.button_rect)
			for i in range(len(self.msg_list)):
				self.screen.blit(self.msg_image[i],
					self.msg_image_rect[i])
