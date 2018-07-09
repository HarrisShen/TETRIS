import pygame

from msg_board import MsgBoard
from button import Button

class Option():
	
	def __init__(self, ai_settings, screen, stats):
		self.ai_settings = ai_settings
		self.screen = screen
		self.stats = stats
		
		self.opt_screen = pygame.Rect(0, 0, ai_settings.gs_width,
			ai_settings.gs_height)
		
		self.font = pygame.font.SysFont('lucidaconsole', 15, bold=True)
		self.b_font = pygame.font.SysFont('arial', 15, bold=True)
		self.color = (255,255,255)
		self.bg_color = ai_settings.bg_color
		
		self.top = 15
		
		self.title = ['Difficulty', 'Scoring', 'Coloring', 'Next-up', 'Fall-pos']
		
		self.text = ai_settings.get_option_text()
		
		self.center = []
		
		self.cube = []
		
		#	'Difficulty': ['easy', 'medium', 'hard', 'hell']
		#	'Scoring': ['simple', 'combo', 'multiple']
		#	'Coloring': ['on', 'off']
		#	'Next-up': ['on', 'off']
		#	'Fall-pos': ['on', 'off']
		
	def draw_text(self, text_list, top, get_center=False):
		next_top = top
		for text_str in text_list:
			text_image = self.font.render(text_str, False,
				self.color,	self.bg_color)
			text_rect = text_image.get_rect()
			text_rect.top = next_top
			text_rect.centerx = self.opt_screen.centerx
			if get_center:
				self.center.append(text_rect.center)
			next_top = text_rect.bottom + 30
			self.screen.blit(text_image, text_rect)
			
	def draw_frame(self, text_list, width, height):
		for f_index in range(len(text_list)):
			frame_rect = pygame.Rect(0,0, width, height)
			frame_rect.center = self.center[f_index]
			
			left_cube = pygame.Rect(0,0, height, height)
			left_cube.left = frame_rect.left
			left_cube.centery = frame_rect.centery
			self.cube.append(left_cube)
			self.screen.fill(self.bg_color, left_cube)
			
			left_image = self.b_font.render(' < ', False, self.color,
				self.bg_color)
			left_image_rect = left_image.get_rect()
			left_image_rect.center = left_cube.center
			self.screen.blit(left_image, left_image_rect)
			
			right_cube = pygame.Rect(0,0, height, height)
			right_cube.right = frame_rect.right
			right_cube.centery = frame_rect.centery
			self.cube.append(right_cube)
			self.screen.fill(self.bg_color, right_cube)
			
			right_image = self.b_font.render(' > ', False, self.color,
				self.bg_color)
			right_image_rect = right_image.get_rect()
			right_image_rect.center = right_cube.center
			self.screen.blit(right_image, right_image_rect)
			
	def draw_options(self):
		self.draw_text(self.title, self.top)
		self.draw_text(self.text, self.top+20, True)
		self.draw_frame(self.text, 120, 15)
		
	def update_option(self, ai_settings):
		self.ai_settings = ai_settings
		self.text = ai_settings.get_option_text()
