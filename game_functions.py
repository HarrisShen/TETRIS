import sys
import time

import pygame

from big_pixel import BigPixel
from big_screen import BigScreen
from brick import Brick

def check_events(ai_settings, screen, b_screen, stats, fund, brick,
	msg_b, button_list, option):
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
		elif event.type == pygame.MOUSEBUTTONDOWN:
			button1, button2, button3 = pygame.mouse.get_pressed()
			if button1:
				mouse_x, mouse_y = pygame.mouse.get_pos()
				check_mouse_events(mouse_x, mouse_y, ai_settings,
					screen, b_screen, stats, fund, brick, msg_b,
					button_list, option)
		elif event.type == pygame.KEYDOWN:
			check_keydown_events(event, ai_settings, screen, stats,
				fund, brick, msg_b)
		elif event.type == pygame.KEYUP:
			check_keyup_events(event, ai_settings, brick)
			
def check_mouse_events(mouse_x, mouse_y, ai_settings, screen, b_screen,
	stats, fund, brick, msg_b, button_list, option):
	button_clicked = 0
	for button_i in range(len(button_list)):
		if button_list[button_i].rect.collidepoint(mouse_x, mouse_y):
			button_clicked = button_i + 1
	if button_clicked == 1:
		if stats.game_option:
			stats.game_option = False
		else:
			if not stats.game_over:
				stats.game_active = not stats.game_active
				stats.game_status = not stats.game_status
				msg_b.nb_screen.clear_screen()
				ai_settings.next_up = not ai_settings.next_up
			elif stats.game_over:
				reset_game(ai_settings, screen, stats, fund, brick)
	elif button_clicked == 2:
		if not stats.game_over:
			reset_game(ai_settings, screen, stats, fund, brick)
		elif stats.game_over:
			stats.game_option = True
			stats.game_active = False
			stats.game_over = True
			stats.game_status = False
			b_screen.clear_screen()
			msg_b.nb_screen.clear_screen()
	elif button_clicked == 3:
		if stats.game_over:
			sys.exit()
		else:
			stats.game_active = False
			stats.game_over = True
			stats.game_status = False
			b_screen.clear_screen()
			msg_b.nb_screen.clear_screen()
	elif button_clicked == 0:
		if stats.game_option:
			for button_i in range(len(option.cube)):
				if option.cube[button_i].collidepoint(mouse_x, mouse_y):
					ai_settings.update_settings(int(button_i/2),
						button_i%2)
					option.update_option(ai_settings)
		
def check_keydown_events(event, ai_settings, screen, stats, fund, brick,
	msg_b):
	if event.key == pygame.K_q:
		if not stats.game_active:
			sys.exit()
	elif event.key == pygame.K_RETURN:
		if not stats.game_over:
			stats.game_active = not stats.game_active
			stats.game_status = not stats.game_status
			msg_b.nb_screen.clear_screen()
			ai_settings.next_up = not ai_settings.next_up
		elif stats.game_over:
			reset_game(ai_settings, screen, stats, fund, brick)
	elif stats.game_active:
		if event.key == pygame.K_SPACE:
			brick.free_fall = True
		elif not brick.free_fall:
			if event.key == pygame.K_LEFT or event.key == pygame.K_a:
				brick.moving_left = True
			elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
				brick.moving_right = True
			elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
				brick.moving_down = True
			elif event.key == pygame.K_UP or event.key == pygame.K_w:
				brick.rotating = True
		
def check_keyup_events(event, ai_settings, brick):
	if event.key == pygame.K_LEFT or event.key == pygame.K_a:
		brick.moving_left = False
		brick.moving_cnt =\
			ai_settings.ctl_rotating_speed
		brick.holding_cnt = -1
	elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
		brick.moving_right = False
		brick.moving_cnt =\
			ai_settings.ctl_rotating_speed
		brick.holding_cnt = -1
	elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
		brick.moving_down = False
		brick.moving_cnt =\
			ai_settings.ctl_rotating_speed
	elif event.key == pygame.K_UP or event.key == pygame.K_w:
		brick.rotating = False
		brick.moving_cnt =\
			ai_settings.ctl_rotating_speed
		brick.holding_cnt = -1
	
def	set_screen(ai_settings, b_screen):
	b_screen.set_screen_pos(ai_settings.gs_pixel_o)
	b_screen.set_screen_scale(ai_settings.gs_width_p,
		ai_settings.gs_height_p)
										
def update_screen(ai_settings, screen, b_screen, stats, clock, fund,
	brick, mb, button_list, stat_button, option):
	screen.fill(ai_settings.bg_color)

	draw_main_frame(ai_settings, screen)
	draw_next_brick_frame(ai_settings, screen)
	mb.show_info(ai_settings)
	
	update_button(stats, button_list)
	for button in button_list:
		button.draw_button()
		
	b_screen.draw_screen()
	
	if stats.game_option:
		option.draw_options()
	
	if stats.game_active:
		b_screen.clear_screen()
		if not fund.clearing:
			brick_fall(ai_settings, stats, clock, fund, brick)
			update_pos(ai_settings, brick)
			brick.draw_phantom_brick()
			brick.draw_brick()
		else:
			full_clear(ai_settings, b_screen, clock, fund, brick)
		fund.draw_self()
		mb.show_nxt_brick(ai_settings)
	
	if stats.game_status:
		update_status(brick, stat_button)
		stat_button.draw_button()
	
	mb.nb_screen.draw_screen()
	
	pygame.display.flip()

def update_button(stats, button_list):
	if stats.game_option:
		button_list[0].update_msg(['OK'])
		button_list[1].update_msg([])
		button_list[2].update_msg([])
	else:
		if stats.game_over:
			button_list[0].update_msg(['START'])
			button_list[1].update_msg(['OPTIONS'])
			button_list[2].update_msg(['EXIT'])
		else:
			button_list[1].update_msg(['RESET'])
			button_list[2].update_msg(['QUIT'])
			if stats.game_active:
				button_list[0].update_msg(['PAUSE'])
			else:
				button_list[0].update_msg(['RESUME'])
			
def update_status(brick, stat_button):
	if brick.stats.game_over:
		stat_button.set_size(width=65, height=55)
		stat_button.set_center(stat_button.ai_settings.gs_center)
		stat_button.update_msg(['GAME','OVER'])
	else:
		stat_button.set_size(height=30)
		stat_button.set_center(stat_button.ai_settings.gs_center)
		stat_button.update_msg(['PAUSED'])
	
def reset_game(ai_settings, screen, stats, fund, brick):
	ai_settings.init_dynamic_settings()
	stats.init_dynamic_stats()
	
	brick.create_new()
	fund.create_new()
	brick.get_phantom_brick()
	
	stats.game_active = True
	stats.game_over = False
	stats.game_status = False
	
def draw_main_frame(ai_settings, screen):
	t_line = pygame.Rect(14, 14, 139, 3)
	pygame.draw.rect(screen, ai_settings.frame_color, t_line)
	b_line = pygame.Rect(14, 280, 139, 3)
	pygame.draw.rect(screen, ai_settings.frame_color, b_line)
	l_line = pygame.Rect(14, 14, 3, 269)
	pygame.draw.rect(screen, ai_settings.frame_color, l_line)
	r_line = pygame.Rect(150, 14, 3, 269)
	pygame.draw.rect(screen, ai_settings.frame_color, r_line)

def draw_next_brick_frame(ai_settings, screen):
	t_line = pygame.Rect(0, 0, 100, 3)
	t_line.top = 14
	t_line.centerx = 227
	pygame.draw.rect(screen, ai_settings.frame_color, t_line)
	l_line = pygame.Rect(0, 0, 3, 85)
	l_line.top = t_line.top
	l_line.left = t_line.left
	pygame.draw.rect(screen, ai_settings.frame_color, l_line)
	r_line = pygame.Rect(0, 0, 3, 85)
	r_line.top = t_line.top
	r_line.right = t_line.right
	pygame.draw.rect(screen, ai_settings.frame_color, r_line)	
	b_line = pygame.Rect(0, 0, 100, 3)
	b_line.left = t_line.left
	b_line.bottom = l_line.bottom
	pygame.draw.rect(screen, ai_settings.frame_color, b_line)

def brick_fall(ai_settings, stats, clock, fund, brick):
	adj_factor = clock.get_fps()/1000
	if brick.free_fall:
		speed = ai_settings.game_ff_speed*adj_factor
	else:
		speed = ai_settings.game_speed*adj_factor
	if brick.cnt >= speed:
		if brick.touch:
			fund.add_pieces(brick.piece_pos, brick.color)
			fund.find_full()
			if not fund.clearing:
				brick.create_new()
				brick.if_touch()
				if brick.if_touch_base():
					stats.game_over = True
					stats.game_active = False
					stats.game_status = True
					stats.update_high()
		else:
			brick.set_pos(brick.x, brick.y+1)
			brick.get_piece_pos()
			brick.if_touch()
		
		brick.cnt = 0
	elif brick.cnt < speed:
		brick.cnt += 1

def update_pos(ai_settings, brick):
	if brick.moving_left:
		if brick.moving_cnt >= ai_settings.ctl_moving_speed:
			if brick.holding_cnt > 0:
				brick.holding_cnt -= 1
			elif brick.holding_cnt <= 0:
				if not brick.touch_side():
					brick.set_pos(brick.x-1, brick.y)
					brick.get_piece_pos()
					brick.get_phantom_brick()
					brick.if_touch()
				if brick.holding_cnt == -1:
					brick.holding_cnt = 4
			brick.moving_cnt = 0
		else:
			brick.moving_cnt += 1
	if brick.moving_right:
		if brick.moving_cnt >= ai_settings.ctl_moving_speed:
			if brick.holding_cnt > 0:
				brick.holding_cnt -= 1
			elif brick.holding_cnt <= 0:
				if not brick.touch_side(left_side=False):
					brick.set_pos(brick.x+1, brick.y)
					brick.get_piece_pos()
					brick.get_phantom_brick()
					brick.if_touch()
				if brick.holding_cnt == -1:
					brick.holding_cnt = 4
			brick.moving_cnt = 0
		else:
			brick.moving_cnt += 1
	if brick.moving_down:
		if brick.moving_cnt >= ai_settings.ctl_moving_speed:
			if brick.holding_cnt > 0:
				brick.holding_cnt -= 1
			elif brick.holding_cnt <= 0:
				brick.if_touch()
				if not brick.touch:
					brick.set_pos(brick.x, brick.y+1)
					brick.get_piece_pos()
					brick.if_touch()
				if brick.holding_cnt == -1:
					brick.holding_cnt = 2
			brick.moving_cnt = 0
		else:
			brick.moving_cnt += 1			
	if brick.rotating:
		if brick.moving_cnt == ai_settings.ctl_rotating_speed:
			if brick.holding_cnt > 0:
				brick.holding_cnt -= 1
			elif brick.holding_cnt <= 0:
				if brick.rotatable():
					brick.rotate()
					brick.get_phantom_brick()
					brick.if_touch()
				if brick.holding_cnt == -1:
					brick.holding_cnt = 2
			brick.moving_cnt = 0
		else:
			brick.moving_cnt += 1
			
def full_clear(ai_settings, b_screen, clock, fund, brick):
	adj_factor = clock.get_fps()/1000
	speed = ai_settings.game_cf_speed*adj_factor
	
	if fund.cnt >= speed:
		if fund.col_cnt < ai_settings.gs_width_p:
			for row in fund.full_row_list:
				fund.color_list[(fund.col_cnt,row)] = (255,255,255)		
		fund.cnt = 0
		fund.col_cnt += 1
		if fund.col_cnt == ai_settings.gs_width_p+5:
			fund.clearing = False
			fund.col_cnt = 0
			fund.clear_full()
			brick.create_new()
			brick.if_touch()
			if brick.if_touch_base():
				stats.game_over = True
				stats.game_active = False
				stats.game_status = True
				stats.update_high()
	elif fund.cnt < speed:
		fund.cnt += 1
