import pygame
import sys
from typing import Optional

class SaveDialog:
    def __init__(self, screen_width: int, screen_height: int):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
        # Dialog dimensions
        self.dialog_width = 400
        self.dialog_height = 200
        self.dialog_x = (screen_width - self.dialog_width) // 2
        self.dialog_y = (screen_height - self.dialog_height) // 2
        
        # Input field
        self.input_rect = pygame.Rect(
            self.dialog_x + 20, 
            self.dialog_y + 80, 
            self.dialog_width - 40, 
            40
        )
        
        # Buttons
        button_width = 100
        button_height = 40
        button_y = self.dialog_y + self.dialog_height - 60
        
        self.save_button = pygame.Rect(
            self.dialog_x + 20, 
            button_y, 
            button_width, 
            button_height
        )
        
        self.cancel_button = pygame.Rect(
            self.dialog_x + self.dialog_width - 120, 
            button_y, 
            button_width, 
            button_height
        )
        
        self.input_text = ""
        self.input_active = True
        self.cursor_visible = True
        self.cursor_timer = 0
        
    def handle_event(self, event) -> Optional[str]:
        """
        Handle events for the save dialog
        Returns: 'save' with input text, 'cancel', or None
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                if self.input_text.strip():
                    return f"save:{self.input_text.strip()}"
            elif event.key == pygame.K_ESCAPE:
                return "cancel"
            elif event.key == pygame.K_BACKSPACE:
                self.input_text = self.input_text[:-1]
            else:
                # Add character if it's printable and not too long
                if len(self.input_text) < 30 and event.unicode.isprintable():
                    self.input_text += event.unicode
                    
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.save_button.collidepoint(event.pos):
                if self.input_text.strip():
                    return f"save:{self.input_text.strip()}"
            elif self.cancel_button.collidepoint(event.pos):
                return "cancel"
                
        return None
    
    def update(self, dt: int):
        """Update cursor blinking"""
        self.cursor_timer += dt
        if self.cursor_timer >= 500:  # Blink every 500ms
            self.cursor_visible = not self.cursor_visible
            self.cursor_timer = 0
    
    def draw(self, screen):
        """Draw the save dialog"""
        # Draw overlay
        overlay = pygame.Surface((self.screen_width, self.screen_height))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(128)
        screen.blit(overlay, (0, 0))
        
        # Draw dialog background
        dialog_rect = pygame.Rect(self.dialog_x, self.dialog_y, self.dialog_width, self.dialog_height)
        pygame.draw.rect(screen, (60, 60, 60), dialog_rect, border_radius=10)
        pygame.draw.rect(screen, (200, 200, 200), dialog_rect, 2, border_radius=10)
        
        # Draw title
        title_text = self.font.render("Save Game", True, (255, 255, 255))
        title_rect = title_text.get_rect(centerx=dialog_rect.centerx, top=dialog_rect.top + 20)
        screen.blit(title_text, title_rect)
        
        # Draw label
        label_text = self.small_font.render("Enter save name:", True, (200, 200, 200))
        screen.blit(label_text, (self.input_rect.left, self.input_rect.top - 25))
        
        # Draw input field
        input_color = (80, 80, 80) if self.input_active else (60, 60, 60)
        pygame.draw.rect(screen, input_color, self.input_rect, border_radius=5)
        pygame.draw.rect(screen, (150, 150, 150), self.input_rect, 2, border_radius=5)
        
        # Draw input text
        if self.input_text or not self.input_active:
            text_surface = self.small_font.render(self.input_text, True, (255, 255, 255))
            text_rect = text_surface.get_rect(
                left=self.input_rect.left + 10,
                centery=self.input_rect.centery
            )
            screen.blit(text_surface, text_rect)
            
            # Draw cursor
            if self.input_active and self.cursor_visible:
                cursor_x = text_rect.right + 2
                cursor_y1 = self.input_rect.centery - 10
                cursor_y2 = self.input_rect.centery + 10
                pygame.draw.line(screen, (255, 255, 255), (cursor_x, cursor_y1), (cursor_x, cursor_y2), 2)
        else:
            # Draw placeholder
            placeholder_surface = self.small_font.render("Enter game name...", True, (120, 120, 120))
            placeholder_rect = placeholder_surface.get_rect(
                left=self.input_rect.left + 10,
                centery=self.input_rect.centery
            )
            screen.blit(placeholder_surface, placeholder_rect)
        
        # Draw buttons
        mouse_pos = pygame.mouse.get_pos()
        
        # Save button
        save_hover = self.save_button.collidepoint(mouse_pos)
        save_color = (100, 150, 100) if save_hover else (70, 120, 70)
        if not self.input_text.strip():
            save_color = (50, 50, 50)  # Disabled state
            
        pygame.draw.rect(screen, save_color, self.save_button, border_radius=5)
        pygame.draw.rect(screen, (200, 200, 200), self.save_button, 2, border_radius=5)
        
        save_text = self.small_font.render("Save", True, (255, 255, 255))
        save_text_rect = save_text.get_rect(center=self.save_button.center)
        screen.blit(save_text, save_text_rect)
        
        # Cancel button
        cancel_hover = self.cancel_button.collidepoint(mouse_pos)
        cancel_color = (150, 100, 100) if cancel_hover else (120, 70, 70)
        
        pygame.draw.rect(screen, cancel_color, self.cancel_button, border_radius=5)
        pygame.draw.rect(screen, (200, 200, 200), self.cancel_button, 2, border_radius=5)
        
        cancel_text = self.small_font.render("Cancel", True, (255, 255, 255))
        cancel_text_rect = cancel_text.get_rect(center=self.cancel_button.center)
        screen.blit(cancel_text, cancel_text_rect)