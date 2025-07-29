import pygame
from code_logic.game_rules import GameRules as gr

class StatusDisplay:
    def __init__(self, board_width, board_height, sidebar_width):
        self.board_width = board_width
        self.board_height = board_height
        self.sidebar_width = sidebar_width
        self.stats_sidebar_width = sidebar_width
        self.font = pygame.font.Font(None, 24)  # Replace 24 with the desired font size

        
        self.status_height = 140
        self.padding = 10
        
        self.x_position = board_width + self.padding
        self.y_position = (board_height // 2) - (self.status_height // 2) - 50
        
        self.ai_stats = {
            'depth': 0,
            'positions_evaluated': 0,
            'evaluation_time': 0,
            'positions_per_second': 0
        }
        self.ai_stats_height = 160
        # self.ai_stats_x_position = self.x_position - sidebar_width + self.padding  # Shift stats to the right
        self.ai_stats_x_position = self.x_position
        # self.ai_stats_y_position = self.y_position + self.status_height - 200
        self.ai_stats_y_position = 0
        
        self.title_font_size = 22
        self.message_font_size = 18
        self.action_font_size = 16
        self.stats_font_size = 16
        self.title_font = pygame.font.SysFont("Arial", self.title_font_size, bold=True)
        self.message_font = pygame.font.SysFont("Segoe UI", self.message_font_size, bold=True)
        self.action_font = pygame.font.SysFont("Segoe UI", self.action_font_size, bold=True)
        self.stats_font = pygame.font.SysFont("Consolas", self.stats_font_size)
        
        self.colors = {
            'normal': {
                'bg': (248, 250, 252),
                'border': (226, 232, 240),
                'text': (15, 23, 42)
            },
            'check': {
                'bg': (254, 243, 199),
                'border': (251, 191, 36),
                'text': (146, 64, 14)
            },
            'checkmate': {
                'bg': (254, 226, 226),
                'border': (239, 68, 68),
                'text': (153, 27, 27)
            },
            'stalemate': {
                'bg': (241, 245, 249),
                'border': (148, 163, 184),
                'text': (51, 65, 85)
            },
            'stats': {
                'bg': (243, 244, 246),
                'border': (209, 213, 219),
                'text': (17, 24, 39)
            }
        }
        
        self.current_message = ""
        self.checking_piece = ""  
        self.current_turn = ""
        self.message_type = "normal"
        self.display_time = 4000
        self.message_start_time = 0
        self.should_display = False
        
    def update_ai_stats(self, depth, positions_evaluated, evaluation_time):
        self.ai_stats['depth'] = depth
        self.ai_stats['positions_evaluated'] = positions_evaluated
        self.ai_stats['evaluation_time'] = evaluation_time
        if evaluation_time > 0:
            self.ai_stats['positions_per_second'] = int(positions_evaluated / evaluation_time)
        else:
            self.ai_stats['positions_per_second'] = 0

    def draw_ai_stats(self, screen):
        stats_rect = pygame.Rect(
            self.ai_stats_x_position,
            self.ai_stats_y_position,
            self.stats_sidebar_width - self.padding * 2,
            self.ai_stats_height
        )
        
        color_scheme = self.colors['stats']
        
        shadow_rect = stats_rect.copy()
        shadow_rect.move_ip(2, 2)
        pygame.draw.rect(screen, (0, 0, 0, 30), shadow_rect, border_radius=10)
        
        pygame.draw.rect(screen, color_scheme['bg'], stats_rect, border_radius=10)
        pygame.draw.rect(screen, color_scheme['border'], stats_rect, 2, border_radius=10)
        
        title_surface = self.title_font.render("AI Statistics", True, color_scheme['text'])
        title_rect = title_surface.get_rect(
            centerx=stats_rect.centerx,
            top=stats_rect.top + self.padding
        )
        screen.blit(title_surface, title_rect)
        
        # Draw separator
        separator_y = title_rect.bottom + 5
        pygame.draw.line(
            screen,
            color_scheme['border'],
            (stats_rect.left + self.padding, separator_y),
            (stats_rect.right - self.padding, separator_y),
            1
        )
        
        # Draw statistics
        stats_start_y = separator_y + 15
        line_height = self.stats_font.get_linesize() + 5
        
        stats_items = [
            ("Search Depth", f"{self.ai_stats['depth']}"),
            ("Positions", f"{self.ai_stats['positions_evaluated']:,}"),
            ("Time", f"{self.ai_stats['evaluation_time']:.2f} sec"),
            ("Positions/sec", f"{self.ai_stats['positions_per_second']:,}")
        ]
        
        for i, (label, value) in enumerate(stats_items):
            # Draw label
            label_surface = self.stats_font.render(label + ":", True, color_scheme['text'])
            screen.blit(label_surface, (stats_rect.left + self.padding * 2, stats_start_y + (i * line_height)))
            
            # Draw value (right-aligned)
            value_surface = self.stats_font.render(value, True, color_scheme['text'])
            value_rect = value_surface.get_rect(
                right=stats_rect.right - self.padding * 2,
                top=stats_start_y + (i * line_height)
            )
            screen.blit(value_surface, value_rect)
    
    def draw_move_history(self, screen, move_history):
        line_height = 20  
        box_height = 10 * line_height + 20  
        box_width = self.sidebar_width - 20
        x = self.board_width + 10
        y = self.board_height - box_height - 20  

        background_rect = pygame.Rect(x, y, box_width, box_height)
        pygame.draw.rect(screen, (255, 255, 0), background_rect, border_radius=10)  
        pygame.draw.rect(screen, (0, 0, 0), background_rect, 2, border_radius=10)  

        header = self.font.render("Move History", True, (0, 0, 0))  
        screen.blit(header, (x + 10, y + 10))  
        max_moves = 9
        visible_moves = move_history[-max_moves:] 
        text_y = y + 40  

        for move in visible_moves:  
            move_text = f"{move['color']} {move['piece']} {move['from']}"
            text_surface = self.font.render(move_text, True, (0, 0, 0))  
            screen.blit(text_surface, (x + 10, text_y))  
            text_y += line_height  



    def update_status(self, message, message_type="normal", checking_piece=None, current_turn=None):
        if message != self.current_message or message_type == "check":
            self.current_message = message
            self.message_type = message_type
            
            self.checking_piece = checking_piece  
            self.message_start_time = pygame.time.get_ticks()
            self.should_display = True
            self.current_turn = current_turn

    def draw(self, screen):
        self.draw_ai_stats(screen)
        if not self.should_display or not self.current_message:
            return

        current_time = pygame.time.get_ticks()
        elapsed = current_time - self.message_start_time

        if elapsed > self.display_time and self.message_type not in ['checkmate', 'stalemate']:
            self.should_display = False
            self.current_message = ""
            return

        status_rect = pygame.Rect(
            self.x_position,
            self.y_position,
            self.sidebar_width - (self.padding * 2),
            self.status_height + 20
        )

        color_scheme = self.colors[self.message_type]
        shadow_rect = status_rect.copy()
        shadow_rect.move_ip(2, 2)
        pygame.draw.rect(screen, (0, 0, 0, 30), shadow_rect, border_radius=10)

        pygame.draw.rect(screen, color_scheme['bg'], status_rect, border_radius=10)
        pygame.draw.rect(screen, color_scheme['border'], status_rect, 2, border_radius=10)

        title_text = self.get_title_text()
        title_surface = self.title_font.render(title_text, True, color_scheme['text'])
        title_rect = title_surface.get_rect(
            centerx=status_rect.centerx,
            top=status_rect.top
        )
        # screen.blit(title_surface, title_rect) #this is just the check message

        separator_y = title_rect.bottom + 5
        pygame.draw.line(
            screen,
            color_scheme['border'],
            (status_rect.left + self.padding, separator_y),
            (status_rect.right - self.padding, separator_y),
            1
        )

        # reduces height for check/checkmate to make room for action text
        message_box_height = status_rect.height - separator_y - (self.padding * 3)
        if self.message_type in ['checkmate', 'check']:
            message_box_height -= self.action_font.get_linesize() * 2

        message_box_rect = pygame.Rect(
            status_rect.left + self.padding * 2,
            # status_rect.top + separator_y + self.padding,
            separator_y + self.padding * 10,
            status_rect.width - (self.padding * 4),
            message_box_height - 11 * self.padding
        )

        message_height = self.draw_wrapped_text(
            screen,
            self.current_message,
            self.message_font,
            color_scheme['text'],
            message_box_rect
        )

        # the above line is where the _colour_ is in check + checkmate, _colour_ wins message is shown, way above where it should be

        if self.message_type == 'checkmate':

            # pygame.draw.line(
            # screen,
            # color_scheme['border'],
            # (status_rect.left + self.padding, separator_y + 20),
            # (status_rect.right - self.padding, separator_y + 20),
            # 1
            # )
            
            action_box_rect = pygame.Rect(
                status_rect.left + self.padding,
                message_box_rect.top + self.padding,
                status_rect.width - (self.padding * 2),
                self.action_font.get_linesize() - 100
            )

            # self.draw_wrapped_text(
            #     screen,
            #     "Go back to main menu to start a new game",
            #     self.action_font,
            #     color_scheme['text'],
            #     action_box_rect
            # )

            self.draw_wrapped_text(
                screen,
                f"{self.current_turn.capitalize()} wins! Go back to main menu to start a new game",
                self.action_font,
                color_scheme['text'],
                action_box_rect
            )

            

        elif self.message_type == 'check' and self.checking_piece:
            # pygame.draw.line(
            # screen,
            # color_scheme['border'],
            # (status_rect.left + self.padding, separator_y),
            # (status_rect.right - self.padding, separator_y),
            # 1
            # )

            action_box_rect = pygame.Rect(
                status_rect.left + self.padding,
                message_box_rect.top + self.padding,
                status_rect.width - (self.padding * 2),
                self.action_font.get_linesize() - 100
            )

            self.draw_wrapped_text(
                screen,
                f"King is being checked by {self.checking_piece}",
                self.action_font,
                color_scheme['text'],
                action_box_rect
            )

            
    def get_title_text(self):
        titles = {
            'normal': 'Game Status',
            'check': 'Check!',
            'checkmate': 'Checkmate!',
            'stalemate': 'Stalemate'
        }
        return titles.get(self.message_type, 'Game Status')

    def draw_wrapped_text(self, surface, text, font, color, rect):
        words = text.split()
        lines = []
        current_line = []
        
        max_width = rect.width - self.padding * 2
        
        for word in words:
            test_line = ' '.join(current_line + [word])
            test_surface = font.render(test_line, True, color)
            
            if test_surface.get_width() <= max_width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]
        
        if current_line:
            lines.append(' '.join(current_line))
        
        line_spacing = 1.2  
        total_height = len(lines) * (font.get_linesize() * line_spacing)
        current_y = rect.top + (rect.height - total_height) // 2 
        
        for line in lines:
            text_surface = font.render(line, True, color)
            text_rect = text_surface.get_rect(
                centerx=rect.centerx,
                top=current_y
            )
            surface.blit(text_surface, text_rect)
            current_y += font.get_linesize() * line_spacing
        return total_height

    def clear(self):
        self.current_message = ""
        self.checking_piece = ""
        self.should_display = False