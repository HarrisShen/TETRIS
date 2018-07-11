import pygame

import game_functions as gf
from settings import Settings
from big_pixel import BigPixel
from big_screen import BigScreen
from game_stats import GameStats
from brick import Brick
from foundation import Foundation
from msg_board import MsgBoard
from button import Button
from option import Option

def run_game():
	pygame.init()
	ai_settings = Settings()
	screen = pygame.display.set_mode(
		(ai_settings.screen_width, ai_settings.screen_height))
	pygame.display.set_caption('TETRIS')
	
	game_screen = BigScreen(ai_settings, screen)
	gf.set_screen(ai_settings, game_screen)
	
	stats = GameStats()
	
	clock = pygame.time.Clock()
	
	fund = Foundation(ai_settings, screen, game_screen, stats)
	
	brick = Brick(ai_settings, screen, game_screen, stats, clock,
		 fund)
	
	msg_b = MsgBoard(ai_settings, screen, stats, brick, clock)
	
	button_list = []
	button_list.append(Button(ai_settings, screen, stats, [], 180,
		ai_settings.ms_centerx))
	button_list.append(Button(ai_settings, screen, stats, [], 0,
		ai_settings.ms_centerx))
	button_list[1].update_top(button_list[0].frame_rect.bottom+5)
	button_list.append(Button(ai_settings, screen, stats, ['QUIT'], 0,
		ai_settings.ms_centerx))
	button_list[2].update_top(button_list[1].frame_rect.bottom+5)
	
	option = Option(ai_settings, screen, stats)
	
	stat_button = Button(ai_settings, screen, stats, [], 0, 0)
	
	while True:
		gf.check_events(ai_settings, screen, game_screen, stats, fund,
			brick, msg_b, button_list, option)
		gf.update_screen(ai_settings, screen, game_screen, stats, clock, 
			fund, brick, msg_b, button_list, stat_button, option)
		clock.tick()
	
run_game()
