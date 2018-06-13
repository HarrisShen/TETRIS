class GameStats():
	
	def __init__(self):
		self.high_score = 0
		self.game_active = False
		self.game_over = True
		
		self.init_dynamic_stats()
		
	def init_dynamic_stats(self):
		self.score = 0
		self.level = 1
		
	def update_high(self):
		if self.score > self.high_score:
			self.high_score = self.score
		
	def update_level(self, ai_settings):
		if self.score > 0:
			if self.score < 10:
				if self.score % 5 == 0:
					self.level += 1
					ai_settings.update_game_speed()
			elif self.score < 40:
				if self.score % 10 == 0:
					self.level += 1
					ai_settings.update_game_speed(0.85)
			elif self.score >= 40:
				if self.score % 20 == 0:
					self.level += 1
					ai_settings.update_game_speed(0.95)
