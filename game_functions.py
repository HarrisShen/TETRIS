import sys

import pygame
from big_pixel import BigPixel
from big_screen import BigScreen
from brick import Brick

def check_events(ai_settings, screen, brick, play_button):
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
		elif event.type == pygame.MOUSEBUTTONDOWN:
			button1, button2, button3 = pygame.mouse.get_pressed()
			if button1:
				mouse_x, mouse_y = pygame.mouse.get_pos()
				if not brick.stats.game_active:
					check_play_button(mouse_x, mouse_y, ai_settings,
						screen, brick, play_button)
		elif event.type == pygame.KEYDOWN:
			check_keydown_events(event, ai_settings, screen, brick)
		elif event.type == pygame.KEYUP:
			check_keyup_events(event, brick)
			
def check_play_button(mouse_x, mouse_y, ai_settings, screen, brick,
	play_button):
	if play_button.rect.collidepoint(mouse_x, mouse_y):
		brick.stats.game_active = True
		if brick.stats.game_over:
			reset_game(ai_settings, screen, brick)
		
def check_keydown_events(event, ai_settings, screen, brick):
	if event.key == pygame.K_q:
		sys.exit()
	elif event.key == pygame.K_RETURN:
		if not brick.stats.game_over:
			brick.stats.game_active = not brick.stats.game_active
		elif brick.stats.game_over:
			reset_game(ai_settings, screen, brick)
	elif brick.stats.game_active:
		if event.key == pygame.K_SPACE:
			brick.free_fall = True
		elif not brick.free_fall:
			if event.key == pygame.K_LEFT:
				brick.moving_left = True
			elif event.key == pygame.K_RIGHT:
				brick.moving_right = True
			elif event.key == pygame.K_DOWN:
				brick.moving_down = True
			elif event.key == pygame.K_UP:
				brick.rotating = True
		
def check_keyup_events(event, brick):
	if event.key == pygame.K_LEFT:
		brick.moving_left = False
		brick.moving_cnt =\
			brick.ai_settings.ctl_moving_speed
	elif event.key == pygame.K_RIGHT:
		brick.moving_right = False
		brick.moving_cnt =\
			brick.ai_settings.ctl_moving_speed
	elif event.key == pygame.K_DOWN:
		brick.moving_down = False
		brick.moving_cnt =\
			brick.ai_settings.ctl_moving_speed
	if event.key == pygame.K_UP:
		brick.rotating = False
		brick.moving_cnt =\
			brick.ai_settings.ctl_moving_speed
											
def update_screen(ai_settings, screen, b_screen, brick, mb,
	play_button):
	screen.fill(ai_settings.bg_color)
	brick.b_screen.draw_screen()
	mb.nb_screen.draw_screen()
	draw_main_frame(ai_settings, screen)
	draw_next_brick_frame(ai_settings, screen)
	mb.show_info()
	
	if not brick.stats.game_active:
		play_button.draw_button()
	
	pygame.display.flip()
	
def reset_game(ai_settings, screen, brick):
	ai_settings.init_dynamic_settings()
	brick.stats.init_dynamic_stats()
	
	brick.create_new()
	brick.fund.create_new()
	
	brick.stats.game_active = True
	
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
