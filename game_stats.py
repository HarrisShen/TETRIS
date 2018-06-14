class GameStats():
	
	def __init__(self):
		self.high_score = 0
		self.game_active = False
		self.game_over = True
		self.game_option = False
		
		self.init_dynamic_stats()
		
	def init_dynamic_stats(self):
		self.score = 0
		self.screen_score = 0
		self.clear_score = 0
		self.level = 1
		
		self.init_combo_stats()
		
	def init_combo_stats(self):
		self.in_combo = False
		self.combo = 1
		
	def update_score(self, ai_settings, full_row, screen_piece):
		if ai_settings.scoring == 0:
			self.score += full_row
		elif ai_settings.scoring == 1:
			if full_row > 0:
				self.score += self.combo*(full_row*2 - 1)
		elif ai_settings.scoring == 2:
			self.screen_score = screen_piece - (screen_piece%10)
			if full_row > 0:
				self.clear_score += int((1.5*full_row-0.5)*10*10*\
					self.combo*self.level)
			self.score = self.screen_score + self.clear_score

	def update_high(self):
		if self.score > self.high_score:
			self.high_score = self.score
		
	def update_level(self, ai_settings):
		if ai_settings.scoring == 0:
			if self.score > 0:
				if self.score < 10:
					if self.score % 5 == 0:
						self.level += 1
						ai_settings.update_game_speed(multi_factor=\
							self.level)
				elif self.score < 40:
					if self.score % 10 == 0:
						self.level += 1
						ai_settings.update_game_speed(0.85, self.level)
				elif self.score >= 40:
					if self.score % 20 == 0:
						self.level += 1
						ai_settings.update_game_speed(0.95, self.level)
		elif ai_settings.scoring == 1:
			if self.score < 40:
				self.level = int(self.score/10)+1
			elif self.score < 200:
				self.level = int(self.score/20)+3
			elif self.score >= 200:
				self.level = int(self.score/50)+9
			ai_settings.update_game_speed(0.90, self.level)
		elif ai_settings.scoring == 2:
			if self.score < 1500:
				# Lv.1~3
				self.level = int(self.score/500)+1
			elif self.score < 5000:
				# Lv.4~7
				self.level = int(self.score/1000)+3
			elif self.score < 20000:
				# Lv.8~13
				self.level = int(self.score/2500)+6
			elif self.score < 100000:
				# Lv.13~21
				self.level = int(self.score/10000)+12
			elif self.score >= 100000:
				# Lv.22 & higher
				self.level = int(self.score/50000)+20
			ai_settings.update_game_speed(0.90, self.level)
			
