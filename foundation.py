import pygame

from big_pixel import BigPixel
from big_screen import BigScreen

class Foundation():
	
	def __init__(self, ai_settings, screen, stats):
		self.ai_settings = ai_settings
		self.x_max = ai_settings.gs_width_p
		self.y_max = ai_settings.gs_height_p
		self.screen = screen
		self.stats = stats
		
		self.create_new()
	
	def create_new(self):
		self.piece_list = []
		
		self.column_list = []
		for x in range(self.x_max):
			self.column_list.append([])
			
		self.color_list = {}		
	
	def add_pieces(self, piece_l=[], piece_color=(255,255,255)):
		self.piece_list += piece_l
		
		for piece in piece_l:
			self.color_list[piece] = piece_color
			self.column_list[piece[0]].append(piece[1])
		
	def clear_full(self):
		# detect full rows and clear them
		new_piece_list = []
		
		new_column_list = []
		for i in range(self.x_max):
			new_column_list.append([])
			
		new_color_list = {}
		
		full_row_num = 0
		row_index = self.y_max-1
		while row_index >= 0 :
			cnt = 0
			for piece in self.piece_list:
				if piece[1] == row_index:
					cnt += 1
			if cnt == self.x_max:
				for piece in self.piece_list:
					if piece[1] == row_index:
						continue
					elif piece[1] < row_index:
						new_piece = (piece[0], piece[1]+1)
						new_piece_list.append(new_piece)
						new_color_list[new_piece] =\
							self.color_list[piece]
						new_column_list[new_piece[0]].append(new_piece[1])
					elif piece[1] > row_index:
						new_piece_list.append(piece)
						new_color_list[piece] = self.color_list[piece]
						new_column_list[piece[0]].append(piece[1])
				self.piece_list = new_piece_list
				new_piece_list = []
				self.column_list = new_column_list
				new_column_list = []
				for i in range(self.x_max):
					new_column_list.append([])
				self.color_list = new_color_list
				new_color_list = {}
				full_row_num += 1
				self.stats.line += 1
				row_index += 1
			row_index -= 1
		if full_row_num == 0:
			self.stats.init_combo_stats()
		elif full_row_num > 0:
			if self.stats.in_combo:
				self.stats.combo += 1
			elif not self.stats.in_combo:
				self.stats.in_combo = True
		self.stats.update_score(self.ai_settings, full_row_num,
			len(self.piece_list))
		self.stats.update_level(self.ai_settings)
					
	def draw_self(self):
		for piece in self.piece_list:
			self.b_screen.set_pixel(piece[0], piece[1], 
				True, self.color_list[piece])
