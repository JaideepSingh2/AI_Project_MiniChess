import pygame

class SoundManager:
    def __init__(self):
        pygame.mixer.init()
        self.move_sound = pygame.mixer.Sound("move.wav")
        self.check_sound = pygame.mixer.Sound("check.wav")
        self.checkmate_sound = pygame.mixer.Sound("checkmate.wav")
        self.stalemate_sound = pygame.mixer.Sound("stalemate.wav")

    def play_move_sound(self):
        self.move_sound.play()

    def play_check_sound(self):
        self.check_sound.play()

    def play_checkmate_sound(self):
        self.checkmate_sound.play()

    def play_stalemate_sound(self):
        self.stalemate_sound.play()