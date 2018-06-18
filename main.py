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
	
	stats = GameStats()
	
	clock = pygame.time.Clock()
	
	fund = Foundation(ai_settings, screen, stats)
	
	brick = Brick(ai_settings, screen, game_screen, stats, clock,
		 fund)
	
	msg_b = MsgBoard(ai_settings, screen, stats, brick, clock)
	
	first_button = Button(ai_settings, screen, stats, [], 170,
		ai_settings.ms_centerx)
	second_button = Button(ai_settings, screen, stats, [], 0,
		ai_settings.ms_centerx)
	second_button.update_top(first_button.frame_rect.bottom+5)
	quit_button = Button(ai_settings, screen, stats, ['QUIT'], 0,
		ai_settings.ms_centerx)
	quit_button.update_top(second_button.frame_rect.bottom+5)
	
	option = Option(ai_settings, screen, stats)
	
	stat_button = Button(ai_settings, screen, stats, [], 0, 0)
	
	while True:
		gf.check_events(ai_settings, screen, brick, msg_b, first_button,
			second_button, quit_button, option)
		if brick.stats.game_active:
			brick.update()
			msg_b.show_nxt_brick(ai_settings)
		gf.update_screen(ai_settings, screen, game_screen, brick, msg_b,
			first_button, second_button, quit_button, stat_button,
			option)
		clock.tick()
	
run_game()
