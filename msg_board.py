import pygame.font

from big_screen import BigScreen

class MsgBoard():
	
	def __init__(self, ai_settings, screen, stats, brick, clock):
		self.ai_settings = ai_settings
		self.posO = self.ai_settings.ms_o
		self.screen = screen
		self.stats = stats
		self.brick = brick
		self.clock = clock
		
		self.set_shape()
		
		self.init_nb_screen()
		
		self.text_color = (255,255,255)
		self.text_font = pygame.font.SysFont('lucidaconsole', 15,
			bold = True)
			
		self.info_pos = (152,90)
		self.info_x = self.info_pos[0] 
		self.info_y = self.info_pos[1]
		
	def set_shape(self):
		self.shape_num = self.brick.nxt_shape_num
		self.shape = self.ai_settings.shape_list[self.shape_num]
		self.color = self.ai_settings.color_list[self.shape_num]
				
	def init_nb_screen(self):
		self.nb_screen = BigScreen(self.ai_settings, self.screen)
		self.nb_screen.set_screen_pos((185,10))
		self.nb_screen.set_screen_scale(6,6)
		
	def show_nxt_brick(self, ai_settings):
		if ai_settings.next_up:
			self.nb_screen.clear_screen()
			self.set_shape()
			for piece in self.shape:
				self.nb_screen.set_pixel(piece[0]+2, piece[1]+2, 
					True, self.color)
	
	def show_msg(self, msg_list=['']):
		last_bottom = self.info_y
		for msg_str in msg_list:
			msg_image = self.text_font.render(msg_str, 
				False, self.text_color, self.ai_settings.bg_color)
		
			msg_rect = msg_image.get_rect()
			msg_rect.centerx = self.ai_settings.ms_centerx
			msg_rect.top = last_bottom+3
			last_bottom = msg_rect.bottom
			self.screen.blit(msg_image, msg_rect)
			
	def show_info(self, ai_settings):
		# show score and high score of current game
		score_str = 'Score:' + str(self.stats.score)
		line_str = 'Line:' + str(self.stats.line)
		level_str = 'Level:' + str(self.stats.level)
		dif_str = 'Mode:' + ai_settings.dif_str.title()
		
		msg_list = [score_str, line_str, level_str, dif_str]
		self.show_msg(msg_list)
