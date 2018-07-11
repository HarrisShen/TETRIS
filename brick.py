import random
import time

import pygame

from settings import Settings
from big_pixel import BigPixel
from big_screen import BigScreen
from game_stats import GameStats
from foundation import Foundation

class Brick():
	
	def __init__(self, ai_settings, screen, b_screen, stats, clock,
		fund):
		self.ai_settings = ai_settings
		self.screen = screen
		
		self.b_screen = b_screen
		
		self.stats = stats
		self.clock = clock
		self.fund = fund

		self.nxt_shape_num = random.randint(0,6)
		self.create_new()

	def create_new(self):
		self.set_pos()
		self.shape_num = self.nxt_shape_num
		self.nxt_shape_num = random.randint(0,6)
		self.shape = self.ai_settings.shape_list[self.shape_num]
		self.color = self.ai_settings.color_list[self.shape_num]
		# generate a list of positions of all pieces from one block
		self.get_piece_pos()
		
		self.cnt = 0
		self.touch = False
		
		self.free_fall = False
		
		self.init_dir_key()
		self.moving_cnt = self.ai_settings.ctl_rotating_speed	
		self.holding_cnt = -1
		
		self.get_phantom_brick()
		
	def set_pos(self, x=4, y=0):
		self.pos = (x, y)
		self.x = self.pos[0]
		self.y = self.pos[1]
		
	def get_piece_pos(self):
		self.piece_pos = []
		for piece in self.shape:
			self.piece_pos.append((piece[0]+self.x, piece[1]+self.y))
					
	def init_dir_key(self, ctrl=False):
		self.moving_left = ctrl
		self.moving_right = ctrl
		self.moving_down = ctrl
		self.rotating = ctrl		 
		
	def draw_brick(self):
		for piece in self.piece_pos:
			self.b_screen.set_pixel(piece[0], piece[1], True,
				self.color)
	
	def if_touch_base(self):
		flag = False
		for piece in self.piece_pos:
			if (piece in self.fund.piece_list):
				flag = True
		return flag
		
	def reach_bottom(self):
		for piece in self.piece_pos:
			if piece[1] >= self.ai_settings.gs_height_p-1:
				self.touch = True
	
	def reach_base(self):
		for piece in self.piece_pos:
			if ((piece[0], piece[1]+1) in self.fund.piece_list):
				self.touch = True
					
	def if_touch(self):
		self.touch = False
		self.reach_bottom()
		self.reach_base()	
			
	def touch_side(self, left_side=True):
		flag = False
		if left_side:
			for piece in self.piece_pos:
				if piece[0] <= 0:
					flag = True
				if ((piece[0]-1, piece[1]) in self.fund.piece_list):
					flag = True
		else:
			for piece in self.piece_pos:
				if piece[0] >= 9:
					flag = True
				if ((piece[0]+1, piece[1]) in self.fund.piece_list):
					flag = True		
		return flag
		
	def rotate(self):
		new_shape = []
		r = self.ai_settings.rotate_list
		for piece in self.shape:
			new_shape.append((piece[0]*r[0] + piece[1]*r[1],
				piece[0]*r[2] + piece[1]*r[3]))
		self.shape = new_shape
		self.get_piece_pos()
	
	def rotatable(self):
		flag = True
		if self.shape_num == 5:
			flag = False
		elif self.shape_num != 5:
			r = self.ai_settings.rotate_list
			for piece in self.shape:
				new_piece = (self.x + piece[0]*r[0] + piece[1]*r[1],
					self.y + piece[0]*r[2] + piece[1]*r[3])
				if new_piece[0] < 0 or new_piece[0] > 9 or\
					new_piece[1] > 19:
					flag = False
				if new_piece in self.fund.piece_list:
					flag = False
				if not flag:
					break
		return flag
		
	def get_phantom_brick(self):
		pb_y = self.y
		
		while pb_y <= self.ai_settings.gs_height_p:
			pb_piece_pos = []
			for piece in self.shape:
				pb_piece_pos.append((piece[0]+self.x, piece[1]+pb_y))
				
			flag = True
			for piece in pb_piece_pos:
				if piece[1] in self.fund.column_list[piece[0]]:
					flag = False
					break
				elif piece[1] >= self.ai_settings.gs_height_p:
					flag = False
					break

			if flag:
				pb_y += 1
			else:
				pb_y -= 1
				self.pb_y = pb_y
				self.pb_piece_pos = []
				for piece in self.shape:
					self.pb_piece_pos.append((piece[0]+self.x,
						piece[1]+pb_y))
				break

	def draw_phantom_brick(self):
		if self.ai_settings.fall_pos:
			for piece in self.pb_piece_pos:
				self.b_screen.set_pixel(piece[0], piece[1], True,
					self.color, width=1)
