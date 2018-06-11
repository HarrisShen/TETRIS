from big_screen import BigScreen

class MsgBoard():
	
	def __init__(self, ai_settings, screen, stats, brick):
		self.ai_settings = ai_settings
		self.posO = self.ai_settings.ms_o
		self.screen = screen
		self.stats = stats
		self.shape_num = brick.nxt_shape_num
		self.shape = self.ai_settings.shape_list[self.shape_num]
		
	def show_nxt_brick(self):
		if self.shape_num >= 0:
			nb_screen = BigScreen(self.ai_settings, self.screen)
			nb_screen.set_screen_pos((160,0))
			nb_screen.set_screen_scale(4,4)
			for piece in self.shape:
				nb_screen.set_pixel(piece[0]+2, piece[1]+2, True)
			nb_screen.draw_screen()
		
		
		
