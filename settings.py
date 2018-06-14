class Settings():
	
	def __init__(self):
		self.bg_color =(0,0,0)
		self.frame_color = (255,255,255)
		
		self.pixel_size = 10
		self.pixel_dist = 3
		self.pixel_step = self.pixel_size + self.pixel_dist
		
		self.init_game_screen()
		self.init_msg_screen()
		self.init_screen()
		
		self.coloring = True
		self.colored_list = [
			(255,92,89),
			(197,0,197),
			(80,80,255),
			(74,255,74),
			(255,255,0),
			(255,165,0),
			(127,187,207)
			]
		self.init_color()
			
		self.shape_list = [
			[(-1,0),(0,0),(1,0),(2,0)],
			[(-1,0),(0,0),(1,0),(1,1)],
			[(-1,1),(-1,0),(0,0),(1,0)],
			[(-1,0),(0,0),(1,0),(0,1)],
			[(-1,0),(0,0),(0,1),(1,1)],
			[(0,0),(1,0),(0,1),(1,1)],
			[(-1,1),(0,1),(0,0),(1,0)]]
		
		self.rotate_list = [0,1,-1,0]	
		
		self.dif = 0
		self.speed_list = [1000, 850, 550, 300]
		self.dif_list = ['easy', 'medium', 'hard', 'hell']
		self.dif_str = self.dif_list[self.dif]
		
		self.init_dynamic_settings()
		
		self.acc_factor = 0.75
		self.game_ff_speed = 30
		self.ctl_rotating_speed = 240
		self.ctl_moving_speed = 170	
		
		self.scoring = 0
		self.scor_list = ['simple', 'combo', 'multiple']
		self.scor_str = self.scor_list[self.scoring]
		
		
		self.hint = True
		
	def init_game_screen(self):
		# game screen (gs) settings
		self.gs_width_p = 10
		self.gs_height_p = 20
		# next two lines - in real pixels
		self.gs_width_margin = 10
		self.gs_height_margin = 10
		self.gs_pixel_o = (self.gs_width_margin, self.gs_height_margin)
		self.gs_width = self.gs_width_p*self.pixel_step +\
			self.gs_width_margin*2 - self.pixel_dist
		self.gs_height = self.gs_height_p*self.pixel_step +\
			self.gs_height_margin*2 - self.pixel_dist
			
	def init_msg_screen(self):
		self.ms_width = 140
		self.ms_height = 0
		self.ms_o = (self.gs_width,0)
		self.ms_centerx = 217
		
	def init_screen(self):
		self.screen_width = self.gs_width + self.ms_width
		self.screen_height = self.gs_height
		
	def init_color(self):
		self.color_list = []
		if self.coloring:
			self.color_list = self.colored_list
		else:
			for index in range(7):
				self.color_list.append((255,255,255))
			
	def init_dynamic_settings(self):
		self.init_game_speed()
		
	def init_game_speed(self):
		self.game_speed = self.speed_list[self.dif]
		self.game_dif = self.dif_list[self.dif]
	
	def update_game_speed(self, acc_factor=1):
		if acc_factor != 1:
			self.acc_factor = acc_factor
		new_speed = int(self.game_speed * self.acc_factor)
		self.game_speed = new_speed
		
	def get_option_text(self):
		option_text = [self.dif_str, self.scor_str]
		if self.coloring:
			option_text.append('on')
		else:
			option_text.append('off')
		if self.hint:
			option_text.append('on')
		else:
			option_text.append('off')
		return option_text
		
	def update_settings(self, item_i, status_i):
		if item_i == 0:
			if status_i == 0:
				self.dif -= 1
				if self.dif < 0:
					self.dif = 3
			elif status_i == 1:
				self.dif += 1
				if self.dif > 3:
					self.dif = 0
			self.dif_str = self.dif_list[self.dif]
		elif item_i == 1:
			if status_i == 0:
				self.scoring -= 1
				if self.scoring < 0:
					self.scoring = 2
			elif status_i == 1:
				self.scoring += 1
				if self.scoring > 2:
					self.scoring = 0
			self.scor_str = self.scor_list[self.scoring]
		elif item_i == 2:
			self.coloring = not self.coloring
			self.init_color()
		elif item_i == 3:
			self.hint = not self.hint
