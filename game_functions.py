import sys
import time

import pygame

from big_pixel import BigPixel
from big_screen import BigScreen
from brick import Brick

def check_events(ai_settings, screen, brick, msg_b, first_button,
	second_button, quit_button, option):
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
		elif event.type == pygame.MOUSEBUTTONDOWN:
			button1, button2, button3 = pygame.mouse.get_pressed()
			if button1:
				mouse_x, mouse_y = pygame.mouse.get_pos()
				check_mouse_events(mouse_x, mouse_y, ai_settings, 
					screen, brick, msg_b, first_button, second_button,
					quit_button, option)
		elif event.type == pygame.KEYDOWN:
			check_keydown_events(event, ai_settings, screen, brick,
				msg_b)
		elif event.type == pygame.KEYUP:
			check_keyup_events(event, brick)
			
def check_mouse_events(mouse_x, mouse_y, ai_settings, screen, brick,
	msg_b, first_button, second_button, quit_button, option):
	if first_button.rect.collidepoint(mouse_x, mouse_y):
		if brick.stats.game_option:
			brick.stats.game_option = False
		else:
			if not brick.stats.game_over:
				brick.stats.game_active = not brick.stats.game_active
				brick.stats.game_status = not brick.stats.game_status
				msg_b.nb_screen.clear_screen()
				ai_settings.next_up = not ai_settings.next_up
			elif brick.stats.game_over:
				reset_game(ai_settings, screen, brick)
	elif second_button.rect.collidepoint(mouse_x, mouse_y):
		if not brick.stats.game_over:
			reset_game(ai_settings, screen, brick)
		elif brick.stats.game_over:
			brick.stats.game_option = True
			brick.stats.game_active = False
			brick.stats.game_over = True
			brick.stats.game_status = False
			brick.b_screen.clear_screen()
			msg_b.nb_screen.clear_screen()
	elif quit_button.rect.collidepoint(mouse_x, mouse_y):
		if brick.stats.game_over:
			sys.exit()
		else:
			brick.stats.game_active = False
			brick.stats.game_over = True
			brick.stats.game_status = False
			brick.b_screen.clear_screen()
			msg_b.nb_screen.clear_screen()
	elif brick.stats.game_option:
		for button_i in range(len(option.cube)):
			if option.cube[button_i].collidepoint(mouse_x,
				mouse_y):
				ai_settings.update_settings(int(button_i/2), button_i%2)
				option.update_option(ai_settings)
		
def check_keydown_events(event, ai_settings, screen, brick, msg_b):
	if event.key == pygame.K_q:
		if not brick.stats.game_active:
			sys.exit()
	elif event.key == pygame.K_RETURN:
		if not brick.stats.game_over:
			brick.stats.game_active = not brick.stats.game_active
			brick.stats.game_status = not brick.stats.game_status
			msg_b.nb_screen.clear_screen()
			ai_settings.next_up = not ai_settings.next_up
		elif brick.stats.game_over:
			reset_game(ai_settings, screen, brick)
	elif brick.stats.game_active:
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
		
def check_keyup_events(event, brick):
	if event.key == pygame.K_LEFT or event.key == pygame.K_a:
		brick.moving_left = False
		brick.moving_cnt =\
			brick.ai_settings.ctl_rotating_speed
	elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
		brick.moving_right = False
		brick.moving_cnt =\
			brick.ai_settings.ctl_rotating_speed
	elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
		brick.moving_down = False
		brick.moving_cnt =\
			brick.ai_settings.ctl_rotating_speed
	elif event.key == pygame.K_UP or event.key == pygame.K_w:
		brick.rotating = False
		brick.moving_cnt =\
			brick.ai_settings.ctl_rotating_speed
											
def update_screen(ai_settings, screen, b_screen, brick, mb,
	first_button, second_button, quit_button, stat_button, option):
	screen.fill(ai_settings.bg_color)
	brick.b_screen.draw_screen()
	mb.nb_screen.draw_screen()
	draw_main_frame(ai_settings, screen)
	draw_next_brick_frame(ai_settings, screen)
	mb.show_info(ai_settings)
	
	update_first_button(brick, first_button)
	update_second_button(brick, second_button)
	update_quit_button(brick, quit_button)
	first_button.draw_button()
	second_button.draw_button()
	quit_button.draw_button()
	
	if brick.stats.game_option:
		option.draw_options()
		
	if brick.stats.game_status:
		update_status(brick, stat_button)
		stat_button.draw_button()
	
	pygame.display.flip()

def update_first_button(brick, first_button):
	if brick.stats.game_option:
		first_button.update_msg(['OK'])
	else:
		if brick.stats.game_over:
			first_button.update_msg(['START'])
		else:
			if brick.stats.game_active:
				first_button.update_msg(['PAUSE'])
			else:
				first_button.update_msg(['RESUME'])
			
def update_second_button(brick, second_button):
	if brick.stats.game_option:
		second_button.update_msg([])
	else:
		if brick.stats.game_over:
			second_button.update_msg(['OPTIONS'])
		else:
			second_button.update_msg(['RESET'])
		
def update_quit_button(brick, quit_button):
	if brick.stats.game_option:
		quit_button.update_msg([])
	else:
		if brick.stats.game_over:
			quit_button.update_msg(['EXIT'])
		else:
			quit_button.update_msg(['QUIT'])
			
def update_status(brick, stat_button):
	if brick.stats.game_over:
		stat_button.set_size(width=65, height=55)
		stat_button.set_center(stat_button.ai_settings.gs_center)
		stat_button.update_msg(['GAME','OVER'])
	else:
		stat_button.set_size(height=30)
		stat_button.set_center(stat_button.ai_settings.gs_center)
		stat_button.update_msg(['PAUSED'])
	
def reset_game(ai_settings, screen, brick):
	ai_settings.init_dynamic_settings()
	brick.stats.init_dynamic_stats()
	
	brick.create_new()
	brick.fund.create_new()
	
	brick.stats.game_active = True
	brick.stats.game_over = False
	brick.stats.game_status = False
	
def draw_main_frame(ai_settings, screen):
	t_line = pygame.Rect(4, 4, 139, 3)
	pygame.draw.rect(screen, ai_settings.frame_color, t_line)
	b_line = pygame.Rect(4, 270, 139, 3)
	pygame.draw.rect(screen, ai_settings.frame_color, b_line)
	l_line = pygame.Rect(4, 4, 3, 269)
	pygame.draw.rect(screen, ai_settings.frame_color, l_line)
	r_line = pygame.Rect(140, 4 , 3, 269)
	pygame.draw.rect(screen, ai_settings.frame_color, r_line)

def draw_next_brick_frame(ai_settings, screen):
	t_line = pygame.Rect(0, 0, 100, 3)
	t_line.top = 4
	t_line.centerx = 217
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

def write_in_data(filename, data):
	with open(filename, 'a') as file_object:
		file_object.write(str(data)+'\n')
		
def get_local_time():
	return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
