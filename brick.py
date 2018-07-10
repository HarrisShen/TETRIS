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
		self.set_screen()
		
		self.stats = stats
		self.clock = clock
		self.fund = fund

		self.nxt_shape_num = random.randint(0,6)
		self.create_new()
	
	def	set_screen(self):
		self.b_screen.set_screen_pos(self.ai_settings.gs_pixel_o)
		self.b_screen.set_screen_scale(self.ai_settings.gs_width_p,
			self.ai_settings.gs_height_p)

	def create_new(self):
		self.set_pos()
		# list of positions of all pieces from one block
		self.piece_pos = []
		self.shape_num = self.nxt_shape_num
		self.nxt_shape_num = random.randint(0,6)
		self.shape = self.ai_settings.shape_list[self.shape_num]
		self.color = self.ai_settings.color_list[self.shape_num]
		self.get_piece_pos()
		
		self.cnt = 0
		self.touch = False
		
		self.free_fall = False
		
		self.set_dir_key()
		self.moving_cnt = self.ai_settings.ctl_rotating_speed	
		self.holding_cnt = -1	
		
	def set_pos(self, x=4, y=0):
		self.pos = (x, y)
		self.x = self.pos[0]
		self.y = self.pos[1]
		
	def get_piece_pos(self):
		self.piece_pos.clear()
		for piece in self.shape:
			self.piece_pos.append((piece[0]+self.x, piece[1]+self.y))
					
	def set_dir_key(self, ctrl=False):
		self.moving_left = ctrl
		self.moving_right = ctrl
		self.moving_down = ctrl
		self.rotating = ctrl		 
		
	def draw_brick(self):
		for piece in self.piece_pos:
			self.b_screen.set_pixel(piece[0], piece[1], True,
				self.color)
			
	def brick_fall(self):
		adj_factor = self.clock.get_fps()/1000
		if self.free_fall:
			speed = self.ai_settings.game_ff_speed*adj_factor
		else:
			speed = self.ai_settings.game_speed*adj_factor
		if self.cnt >= speed:
			if self.touch:
				self.fund.add_pieces(self.piece_pos, self.color)
				self.fund.clear_full()
				self.create_new()
				self.if_touch()
				if self.if_touch_base():
					self.stats.game_over = True
					self.stats.game_active = False
					self.stats.game_status = True
					self.stats.update_high()
			else:
				self.set_pos(self.x, self.y+1)
				self.get_piece_pos()
				self.if_touch()
			
			self.cnt = 0
		elif self.cnt < speed:
			self.cnt += 1
	
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

	def update_pos(self):
		if self.moving_left:
			if self.moving_cnt >= self.ai_settings.ctl_moving_speed:
				if self.holding_cnt > 0:
					self.holding_cnt -= 1
				elif self.holding_cnt <= 0:
					if not self.touch_side():
						self.set_pos(self.x-1, self.y)
						self.get_piece_pos()
						self.if_touch()
					if self.holding_cnt == -1:
						self.holding_cnt = 4
				self.moving_cnt = 0
			else:
				self.moving_cnt += 1
		if self.moving_right:
			if self.moving_cnt >= self.ai_settings.ctl_moving_speed:
				if self.holding_cnt > 0:
					self.holding_cnt -= 1
				elif self.holding_cnt <= 0:
					if not self.touch_side(left_side=False):
						self.set_pos(self.x+1, self.y)
						self.get_piece_pos()
						self.if_touch()
					if self.holding_cnt == -1:
						self.holding_cnt = 4
				self.moving_cnt = 0
			else:
				self.moving_cnt += 1
		if self.moving_down:
			if self.moving_cnt >= self.ai_settings.ctl_moving_speed:
				if self.holding_cnt > 0:
					self.holding_cnt -= 1
				elif self.holding_cnt <= 0:
					self.if_touch()
					if not self.touch:
						self.set_pos(self.x, self.y+1)
						self.get_piece_pos()
						self.if_touch()
					if self.holding_cnt == -1:
						self.holding_cnt = 2
				self.moving_cnt = 0
			else:
				self.moving_cnt += 1			
		if self.rotating:
			if self.moving_cnt == self.ai_settings.ctl_rotating_speed:
				if self.holding_cnt > 0:
					self.holding_cnt -= 1
				elif self.holding_cnt <= 0:
					if self.rotatable():
						self.rotate()
						self.if_touch()
					if self.holding_cnt == -1:
						self.holding_cnt = 2
				self.moving_cnt = 0
			else:
				self.moving_cnt += 1
				
	def draw_fund(self):
		for base_piece in self.fund.piece_list:
			self.b_screen.set_pixel(base_piece[0], base_piece[1], 
				True, self.fund.color_list[base_piece])
			
	def update(self):
		self.b_screen.clear_screen()
		self.update_pos()
		self.brick_fall()
		self.draw_phantom_brick()
		self.draw_brick()
		self.draw_fund()
			
	def get_local_time(self):
		return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
		
	def get_phantom_brick(self):
		pb_y = self.y
		pb_x = self.x
		
		while pb_y <= self.ai_settings.gs_height_p:
			pb_piece_pos = []
			for piece in self.shape:
				pb_piece_pos.append((piece[0]+pb_x, piece[1]+pb_y))
				
			flag = True
			for piece in pb_piece_pos:
				if self.fund.column_list[piece[0]]:
					if piece[1] in self.fund.column_list[piece[0]]:
						flag = False
						break
				else:
					if piece[1] >= self.ai_settings.gs_height_p:
						flag = False
						break
			
			if flag:
				pb_y += 1
			else:
				pb_y -= 1
				self.pb_y = pb_y
				self.pb_piece_pos = []
				for piece in self.shape:
					self.pb_piece_pos.append((piece[0]+pb_x,
						piece[1]+pb_y))
				break
	
	def draw_phantom_brick(self):
		if self.ai_settings.fall_pos:
			self.get_phantom_brick()
			for piece in self.pb_piece_pos:
				self.b_screen.set_pixel(piece[0], piece[1], True,
					self.color, width=1)
