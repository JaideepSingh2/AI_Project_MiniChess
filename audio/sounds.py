import pygame
import os 

class SoundManager:
    def __init__(self):
            script_dir = os.path.dirname(os.path.abspath(__file__))
            
            # Load sound files with absolute paths
            self.move_sound = pygame.mixer.Sound(os.path.join(script_dir, "move.wav"))
            self.check_sound = pygame.mixer.Sound(os.path.join(script_dir, "check.wav"))
            self.checkmate_sound = pygame.mixer.Sound(os.path.join(script_dir, "checkmate.wav"))
            self.stalemate_sound = pygame.mixer.Sound(os.path.join(script_dir, "stalemate.wav"))
            
            print("Sound system initialized successfully")

    def play_move_sound(self):
        self.move_sound.play()

    def play_check_sound(self):
        self.check_sound.play()

    def play_checkmate_sound(self):
        self.checkmate_sound.play()

    def play_stalemate_sound(self):
        self.stalemate_sound.play()