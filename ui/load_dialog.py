import pygame
from typing import List, Dict, Optional
from datetime import datetime

class LoadDialog:
    def __init__(self, screen_width: int, screen_height: int, saved_games: List[Dict]):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.saved_games = saved_games
        self.font = pygame.font.Font(None, 32)
        self.small_font = pygame.font.Font(None, 20)
        self.tiny_font = pygame.font.Font(None, 16)
        
        # Dialog dimensions
        self.dialog_width = 600
        self.dialog_height = 500
        self.dialog_x = (screen_width - self.dialog_width) // 2
        self.dialog_y = (screen_height - self.dialog_height) // 2
        
        # Game list area
        self.list_rect = pygame.Rect(
            self.dialog_x + 20,
            self.dialog_y + 60,
            self.dialog_width - 40,
            self.dialog_height - 140
        )
        
        # Buttons
        button_width = 100
        button_height = 40
        button_y = self.dialog_y + self.dialog_height - 60
        
        self.load_button = pygame.Rect(
            self.dialog_x + 20,
            button_y,
            button_width,
            button_height
        )
        
        self.delete_button = pygame.Rect(
            self.dialog_x + 140,
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
        
        self.selected_game = None
        self.scroll_offset = 0
        self.max_visible_games = 8
        self.game_item_height = 45
    
    def update(self, dt: int):
        """Update method for consistency with other dialogs"""
        # LoadDialog doesn't need any time-based updates currently
        # But we include this method for interface consistency
        pass
        
    def handle_event(self, event) -> Optional[str]:
        """
        Handle events for the load dialog
        Returns: 'load:game_name', 'delete:game_name', 'cancel', or None
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return "cancel"
            elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                if self.selected_game:
                    return f"load:{self.selected_game['name']}"
            elif event.key == pygame.K_DELETE:
                if self.selected_game:
                    return f"delete:{self.selected_game['name']}"
                    
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.load_button.collidepoint(event.pos):
                if self.selected_game:
                    return f"load:{self.selected_game['name']}"
            elif self.delete_button.collidepoint(event.pos):
                if self.selected_game:
                    return f"delete:{self.selected_game['name']}"
            elif self.cancel_button.collidepoint(event.pos):
                return "cancel"
            elif self.list_rect.collidepoint(event.pos):
                # Handle game selection
                relative_y = event.pos[1] - self.list_rect.top
                game_index = (relative_y // self.game_item_height) + self.scroll_offset
                if 0 <= game_index < len(self.saved_games):
                    self.selected_game = self.saved_games[game_index]
                    
        elif event.type == pygame.MOUSEWHEEL:
            if self.list_rect.collidepoint(pygame.mouse.get_pos()):
                self.scroll_offset = max(0, min(
                    len(self.saved_games) - self.max_visible_games,
                    self.scroll_offset - event.y
                ))
                
        return None
    
    def _format_date(self, iso_date: str) -> str:
        """Format ISO date string to readable format"""
        try:
            dt = datetime.fromisoformat(iso_date)
            return dt.strftime("%Y-%m-%d %H:%M")
        except:
            return "Unknown"
    
    def draw(self, screen):
        """Draw the load dialog"""
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
        title_text = self.font.render("Load Game", True, (255, 255, 255))
        title_rect = title_text.get_rect(centerx=dialog_rect.centerx, top=dialog_rect.top + 20)
        screen.blit(title_text, title_rect)
        
        # Draw game list
        pygame.draw.rect(screen, (40, 40, 40), self.list_rect, border_radius=5)
        pygame.draw.rect(screen, (120, 120, 120), self.list_rect, 1, border_radius=5)
        
        if not self.saved_games:
            # No saved games message
            no_games_text = self.small_font.render("No saved games found", True, (150, 150, 150))
            no_games_rect = no_games_text.get_rect(center=self.list_rect.center)
            screen.blit(no_games_text, no_games_rect)
        else:
            # Draw game items
            visible_games = self.saved_games[self.scroll_offset:self.scroll_offset + self.max_visible_games]
            
            for i, game in enumerate(visible_games):
                item_y = self.list_rect.top + (i * self.game_item_height)
                item_rect = pygame.Rect(
                    self.list_rect.left + 5,
                    item_y + 2,
                    self.list_rect.width - 10,
                    self.game_item_height - 4
                )
                
                # Highlight selected game
                if self.selected_game and game['name'] == self.selected_game['name']:
                    pygame.draw.rect(screen, (80, 120, 80), item_rect, border_radius=3)
                    pygame.draw.rect(screen, (150, 200, 150), item_rect, 1, border_radius=3)
                
                # Game name
                name_text = self.small_font.render(game['name'], True, (255, 255, 255))
                screen.blit(name_text, (item_rect.left + 10, item_rect.top + 5))
                
                # Game mode and date
                mode_text = self.tiny_font.render(f"Mode: {game['game_mode'].replace('_', ' ')}", True, (180, 180, 180))
                screen.blit(mode_text, (item_rect.left + 10, item_rect.top + 25))
                
                date_text = self.tiny_font.render(f"Saved: {self._format_date(game['save_date'])}", True, (180, 180, 180))
                date_rect = date_text.get_rect(right=item_rect.right - 10, top=item_rect.top + 5)
                screen.blit(date_text, date_rect)
                
                move_text = self.tiny_font.render(f"Moves: {game['move_count']}", True, (180, 180, 180))
                move_rect = move_text.get_rect(right=item_rect.right - 10, top=item_rect.top + 25)
                screen.blit(move_text, move_rect)
        
        # Draw scrollbar if needed
        if len(self.saved_games) > self.max_visible_games:
            scrollbar_height = self.list_rect.height
            scrollbar_x = self.list_rect.right - 10
            scrollbar_rect = pygame.Rect(scrollbar_x, self.list_rect.top, 8, scrollbar_height)
            pygame.draw.rect(screen, (80, 80, 80), scrollbar_rect, border_radius=4)
            
            # Scrollbar thumb
            thumb_height = max(20, (self.max_visible_games / len(self.saved_games)) * scrollbar_height)
            thumb_y = self.list_rect.top + (self.scroll_offset / len(self.saved_games)) * scrollbar_height
            thumb_rect = pygame.Rect(scrollbar_x, thumb_y, 8, thumb_height)
            pygame.draw.rect(screen, (150, 150, 150), thumb_rect, border_radius=4)
        
        # Draw buttons
        mouse_pos = pygame.mouse.get_pos()
        
        # Load button
        load_hover = self.load_button.collidepoint(mouse_pos)
        load_color = (100, 150, 100) if load_hover else (70, 120, 70)
        if not self.selected_game:
            load_color = (50, 50, 50)  # Disabled state
            
        pygame.draw.rect(screen, load_color, self.load_button, border_radius=5)
        pygame.draw.rect(screen, (200, 200, 200), self.load_button, 2, border_radius=5)
        
        load_text = self.small_font.render("Load", True, (255, 255, 255))
        load_text_rect = load_text.get_rect(center=self.load_button.center)
        screen.blit(load_text, load_text_rect)
        
        # Delete button
        delete_hover = self.delete_button.collidepoint(mouse_pos)
        delete_color = (150, 100, 100) if delete_hover else (120, 70, 70)
        if not self.selected_game:
            delete_color = (50, 50, 50)  # Disabled state
            
        pygame.draw.rect(screen, delete_color, self.delete_button, border_radius=5)
        pygame.draw.rect(screen, (200, 200, 200), self.delete_button, 2, border_radius=5)
        
        delete_text = self.small_font.render("Delete", True, (255, 255, 255))
        delete_text_rect = delete_text.get_rect(center=self.delete_button.center)
        screen.blit(delete_text, delete_text_rect)
        
        # Cancel button
        cancel_hover = self.cancel_button.collidepoint(mouse_pos)
        cancel_color = (100, 100, 100) if cancel_hover else (70, 70, 70)
        
        pygame.draw.rect(screen, cancel_color, self.cancel_button, border_radius=5)
        pygame.draw.rect(screen, (200, 200, 200), self.cancel_button, 2, border_radius=5)
        
        cancel_text = self.small_font.render("Cancel", True, (255, 255, 255))
        cancel_text_rect = cancel_text.get_rect(center=self.cancel_button.center)
        screen.blit(cancel_text, cancel_text_rect)