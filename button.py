import pygame

class Button():

	def __init__(self, ai_settings, screen, stats, msg, top):
		self.ai_settings = ai_settings
		self.screen = screen
		self.stats = stats
		
		self.msg = msg
		self.top = top
		
		self.width, self.height = 86, 30
		self.button_color = ai_settings.bg_color
		self.frame_color = ai_settings.frame_color
		self.text_color = (255,255,255)
		self.font = pygame.font.SysFont('arial', 20, bold=True)
		
		self.prep_button()
		self.prep_msg(self.msg)
	
	def prep_button(self):
		self.frame_rect = pygame.Rect(0, 0, self.width, self.height)
		self.frame_rect.centerx = self.ai_settings.ms_centerx
		self.frame_rect.top = self.top
		self.button_rect = pygame.Rect(0, 0, self.width-6,
			self.height-6)
		self.button_rect.centerx = self.ai_settings.ms_centerx
		self.button_rect.top = self.top+3
		self.rect = self.button_rect
			
	def prep_msg(self, msg):
		self.msg_image = self.font.render(msg, False, self.text_color,
			self.ai_settings.bg_color)
		self.msg_image_rect = self.msg_image.get_rect()
		self.msg_image_rect.center = self.frame_rect.center
		
	def update_msg(self, new_msg):
		self.msg = new_msg
		self.prep_msg(self.msg)
		
	def update_top(self, new_top):
		self.top = new_top
		self.prep_button()
		self.prep_msg(self.msg)
				
	def draw_button(self):
		self.screen.fill(self.frame_color, self.frame_rect)
		self.screen.fill(self.button_color, self.button_rect)
		self.screen.blit(self.msg_image, self.msg_image_rect)
