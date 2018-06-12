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

def run_game():
	pygame.init()
	ai_settings = Settings()
	screen = pygame.display.set_mode(
		(ai_settings.screen_width, ai_settings.screen_height))
	pygame.display.set_caption('TETRIS')
	
	game_screen = BigScreen(ai_settings, screen)
	
	stats = GameStats()
	
	fund = Foundation(ai_settings, screen, stats)
	
	brick = Brick(ai_settings, screen, game_screen, stats, fund)
	
	msg_b = MsgBoard(ai_settings, screen, stats, brick)
	
	play_button = Button(ai_settings, screen, stats, 'START', 180)
	
	while True:
		gf.check_events(ai_settings, screen, brick, play_button)
		if brick.stats.game_active:
			brick.update()
			msg_b.show_nxt_brick()
		gf.update_screen(ai_settings, screen, game_screen, brick, msg_b,
			play_button)
	
run_game()
