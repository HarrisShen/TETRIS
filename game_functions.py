import sys

import pygame
from big_pixel import BigPixel
from big_screen import BigScreen
from brick import Brick

def check_events(ai_settings, screen, brick):
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
		elif event.type == pygame.KEYDOWN:
			check_keydown_events(event, brick)
		elif event.type == pygame.KEYUP:
			check_keyup_events(event, brick)
			
def check_keydown_events(event, brick):
	if event.key == pygame.K_q:
		sys.exit()
	elif event.key == pygame.K_RETURN:
		brick.stats.game_active = not brick.stats.game_active
		if not brick.stats.game_active and\
			not brick.stats.game_over:
			print('Paused. Score:' + str(brick.stats.score))
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
											
def update_screen(ai_settings, screen, b_screen, brick, mb):
	screen.fill(ai_settings.bg_color)
	brick.b_screen.draw_screen()
	draw_main_frame(ai_settings, screen)
	mb.show_nxt_brick()
	pygame.display.flip()
	
def draw_main_frame(ai_settings, screen):
	u_line = pygame.Rect(4, 4, 139, 3)
	pygame.draw.rect(screen, ai_settings.frame_color, u_line)
	b_line = pygame.Rect(4, 270, 139, 3)
	pygame.draw.rect(screen, ai_settings.frame_color, b_line)
	l_line = pygame.Rect(4, 4, 3, 269)
	pygame.draw.rect(screen, ai_settings.frame_color, l_line)
	r_line = pygame.Rect(140, 4 , 3, 269)
	pygame.draw.rect(screen, ai_settings.frame_color, r_line)
