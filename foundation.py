import pygame

from big_pixel import BigPixel
from big_screen import BigScreen

class Foundation():
	
	def __init__(self, ai_settings, screen, b_screen, stats):
		self.ai_settings = ai_settings
		self.x_max = ai_settings.gs_width_p
		self.y_max = ai_settings.gs_height_p
		self.screen = screen
		self.b_screen = b_screen
		self.stats = stats
		
		self.create_new()
	
	def create_new(self):
		self.piece_list = []
		
		self.column_list = []
		for x in range(self.x_max):
			self.column_list.append([])
			
		self.color_list = {}
			
		self.full_row_list = []
		self.full_row_num = 0
		
		self.clearing = False
		
		self.cnt = 0
		self.col_cnt = 0	
	
	def add_pieces(self, piece_l=[], piece_color=(255,255,255)):
		self.piece_list += piece_l
		
		for piece in piece_l:
			self.color_list[piece] = piece_color
			self.column_list[piece[0]].append(piece[1])
		
	def find_full(self):
		# find if any row is full
		row_index = self.y_max-1
		while row_index >= 0:
			cnt = 0
			for piece in self.piece_list:
				if piece[1] == row_index:
					cnt += 1
			if cnt == self.x_max:
				self.clearing = True
				self.full_row_list.append(row_index)
			row_index -= 1
		self.full_row_num = len(self.full_row_list)
			
	def clear_full(self):
		# clear full rows
		new_piece_list = []
		new_color_list = {}
		new_column_list = []
		for i in range(self.x_max):
			new_column_list.append([])
		
		row_adj_list = {}
		for i in range(self.y_max):
			cnt = 0
			if i in self.full_row_list:
				row_adj_list[i] = -1
			else:
				for row in self.full_row_list:
					if i < row:
						cnt += 1
				row_adj_list[i] = cnt
		
		for piece in self.piece_list:
			if piece[1] in self.full_row_list:
				continue
			else:
				if piece[1] >= 0:
					new_piece = (piece[0], piece[1]+\
						row_adj_list[piece[1]])
					new_piece_list.append(new_piece)
					new_color_list[new_piece] = self.color_list[piece]
					new_column_list[new_piece[0]].append(new_piece[1])

		self.piece_list = new_piece_list
		new_piece_list = []
		self.column_list = new_column_list
		new_column_list = []
		for i in range(self.x_max):
			new_column_list.append([])
		self.color_list = new_color_list
		new_color_list = {}
		self.stats.line += self.full_row_num

		if self.full_row_num == 0:
			self.stats.init_combo_stats()
		elif self.full_row_num > 0:
			if self.stats.in_combo:
				self.stats.combo += 1
			elif not self.stats.in_combo:
				self.stats.in_combo = True
		self.stats.update_score(self.ai_settings, self.full_row_num,
			len(self.piece_list))
		self.stats.update_level(self.ai_settings)
		
		self.full_row_list = []
		self.full_row_num = 0
					
	def draw_self(self):
		for piece in self.piece_list:
			self.b_screen.set_pixel(piece[0], piece[1], 
				True, self.color_list[piece])
