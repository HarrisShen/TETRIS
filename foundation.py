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
		
		self.color = (255,255,255)
		
		self.piece_list = []
		# the lower the row, the higher the y-index
		self.high_row = self.ai_settings.gs_height-1
	
	def add_pieces(self, piece_l=[]):
		self.piece_list += piece_l
		for piece in piece_l:
			if piece[1] < self.high_row:
				self.highrow = piece[1]
		
	def clear_full(self):
		# detect full rows and clear them
		new_piece_list = []
		row_index = self.y_max - 1
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
						new_piece_list.append((piece[0], piece[1]+1))
					elif piece[1] > row_index:
						new_piece_list.append(piece)
				self.piece_list = new_piece_list
				new_piece_list = []		
				row_index += 1
				self.stats.score += 1
			row_index -= 1
				
	def draw_self(self):
		for piece in self.piece_list:
			self.b_screen.set_pixel(piece[0], piece[1], True)
			
