from .piece import King, Queen, Rook, Bishop, Knight, Pawn
import time

class ChessAI:
    def __init__(self, board, game_rules, depth=3):
        self.board = board
        self.game_rules = game_rules
        self.depth = depth
        
        self.piece_values = {
            'pawn': 100,
            'knight': 320,
            'bishop': 330,
            'rook': 500,
            'queen': 900,
            'king': 20000
        }
        
        self.pawn_table = [
            [0,  0,  0,  0,  0,  0,  0,  0],
            [50, 50, 50, 50, 50, 50, 50, 50],
            [10, 10, 20, 30, 30, 20, 10, 10],
            [5,  5, 10, 25, 25, 10,  5,  5],
            [0,  0,  0, 20, 20,  0,  0,  0],
            [5, -5,-10,  0,  0,-10, -5,  5],
            [5, 10, 10,-20,-20, 10, 10,  5],
            [0,  0,  0,  0,  0,  0,  0,  0]
        ]
        
        self.knight_table = [
            [-50,-40,-30,-30,-30,-30,-40,-50],
            [-40,-20,  0,  0,  0,  0,-20,-40],
            [-30,  0, 10, 15, 15, 10,  0,-30],
            [-30,  5, 15, 20, 20, 15,  5,-30],
            [-30,  0, 15, 20, 20, 15,  0,-30],
            [-30,  5, 10, 15, 15, 10,  5,-30],
            [-40,-20,  0,  5,  5,  0,-20,-40],
            [-50,-40,-30,-30,-30,-30,-40,-50]
        ]
        
        self.bishop_table = [
            [-20,-10,-10,-10,-10,-10,-10,-20],
            [-10,  0,  0,  0,  0,  0,  0,-10],
            [-10,  0,  5, 10, 10,  5,  0,-10],
            [-10,  5,  5, 10, 10,  5,  5,-10],
            [-10,  0, 10, 10, 10, 10,  0,-10],
            [-10, 10, 10, 10, 10, 10, 10,-10],
            [-10,  5,  0,  0,  0,  0,  5,-10],
            [-20,-10,-10,-10,-10,-10,-10,-20]
        ]
        
        self.rook_table = [
            [0,  0,  0,  0,  0,  0,  0,  0],
            [5, 10, 10, 10, 10, 10, 10,  5],
            [-5,  0,  0,  0,  0,  0,  0, -5],
            [-5,  0,  0,  0,  0,  0,  0, -5],
            [-5,  0,  0,  0,  0,  0,  0, -5],
            [-5,  0,  0,  0,  0,  0,  0, -5],
            [-5,  0,  0,  0,  0,  0,  0, -5],
            [0,  0,  0,  5,  5,  0,  0,  0]
        ]
        
        self.queen_table = [
            [-20,-10,-10, -5, -5,-10,-10,-20],
            [-10,  0,  0,  0,  0,  0,  0,-10],
            [-10,  0,  5,  5,  5,  5,  0,-10],
            [-5,  0,  5,  5,  5,  5,  0, -5],
            [0,  0,  5,  5,  5,  5,  0, -5],
            [-10,  5,  5,  5,  5,  5,  0,-10],
            [-10,  0,  5,  0,  0,  0,  0,-10],
            [-20,-10,-10, -5, -5,-10,-10,-20]
        ]
        
        self.king_table = [
            [-30,-40,-40,-50,-50,-40,-40,-30],
            [-30,-40,-40,-50,-50,-40,-40,-30],
            [-30,-40,-40,-50,-50,-40,-40,-30],
            [-30,-40,-40,-50,-50,-40,-40,-30],
            [-20,-30,-30,-40,-40,-30,-30,-20],
            [-10,-20,-20,-20,-20,-20,-20,-10],
            [20, 20,  0,  0,  0,  0, 20, 20],
            [20, 30, 10,  0,  0, 10, 30, 20]
        ]

    def create_virtual_board(self):
        """Create a virtual board state for AI calculations"""
        virtual_pieces = []
        for piece in self.board.pieces:
            virtual_piece = {
                'type': piece.type,
                'color': piece.color,
                'position': piece.position,
                'moved_once': getattr(piece, 'moved_once', None)
            }
            virtual_pieces.append(virtual_piece)
        return virtual_pieces

    def get_virtual_piece_at(self, virtual_board, position):
        """Get piece at position in virtual board"""
        for piece in virtual_board:
            if piece['position'] == position:
                return piece
        return None

    def make_virtual_move(self, virtual_board, piece, move):
        """Make a move on virtual board and return what was captured"""
        captured_piece = self.get_virtual_piece_at(virtual_board, move)
        if captured_piece:
            virtual_board.remove(captured_piece)
        
        old_position = piece['position']
        piece['position'] = move
        
        old_moved_once = piece.get('moved_once')
        if piece['type'] == 'pawn':
            piece['moved_once'] = True
            
        return captured_piece, old_position, old_moved_once

    def undo_virtual_move(self, virtual_board, piece, old_position, captured_piece, old_moved_once):
        """Undo a move on virtual board"""
        piece['position'] = old_position
        
        if captured_piece:
            virtual_board.append(captured_piece)
            
        if old_moved_once is not None:
            piece['moved_once'] = old_moved_once

    def get_virtual_possible_moves(self, virtual_board, piece):
        """Get possible moves for a piece on virtual board"""
        # Create a temporary real piece to use existing move logic
        piece_classes = {
            'rook': Rook, 'knight': Knight, 'bishop': Bishop,
            'queen': Queen, 'king': King, 'pawn': Pawn
        }
        
        # Create temporary piece
        piece_class = piece_classes[piece['type']]
        temp_piece = piece_class(None, None, piece['color'], piece['position'])
        if piece['type'] == 'pawn' and piece.get('moved_once') is not None:
            temp_piece.moved_once = piece['moved_once']
        
        # Create temporary board wrapper
        class VirtualBoardWrapper:
            def __init__(self, virtual_pieces):
                self.virtual_pieces = virtual_pieces
                
            def get_piece_at(self, position):
                for p in self.virtual_pieces:
                    if p['position'] == position:
                        # Return a simple object with color attribute
                        class SimplePiece:
                            def __init__(self, color):
                                self.color = color
                        return SimplePiece(p['color'])
                return None
                
            def is_empty_square(self, row, col):
                return self.get_piece_at((row, col)) is None
                
            def is_opponent_piece(self, row, col, current_color):
                piece = self.get_piece_at((row, col))
                return piece is not None and piece.color != current_color
        
        virtual_board_wrapper = VirtualBoardWrapper(virtual_board)
        return temp_piece.get_possible_moves(virtual_board_wrapper)

    def is_virtual_move_legal(self, virtual_board, piece, destination):
        """Check if move is legal on virtual board"""
        # Create temporary game state
        old_position = piece['position']
        captured_piece = self.get_virtual_piece_at(virtual_board, destination)
        
        # Make temporary move
        if captured_piece:
            virtual_board.remove(captured_piece)
        piece['position'] = destination
        
        # Check if king is in check
        king_piece = None
        for p in virtual_board:
            if p['type'] == 'king' and p['color'] == piece['color']:
                king_piece = p
                break
                
        in_check = False
        if king_piece:
            king_pos = king_piece['position']
            opponent_pieces = [p for p in virtual_board if p['color'] != piece['color']]
            
            for opp_piece in opponent_pieces:
                possible_moves = self.get_virtual_possible_moves(virtual_board, opp_piece)
                if king_pos in possible_moves:
                    in_check = True
                    break
        
        # Undo temporary move
        piece['position'] = old_position
        if captured_piece:
            virtual_board.append(captured_piece)
            
        return not in_check

    def get_best_move(self, color):
        """Returns the best move for the given color using minimax with alpha-beta pruning."""
        self.positions_evaluated = 0
        start_time = time.time()
        
        best_value = float('-inf') if color == 'white' else float('inf')
        best_move = None
        alpha = float('-inf')
        beta = float('inf')
        
        # Create virtual board for calculations
        virtual_board = self.create_virtual_board()
        pieces = [p for p in virtual_board if p['color'] == color]
        
        for piece in pieces:
            possible_moves = self.get_virtual_possible_moves(virtual_board, piece)
            for move in possible_moves:
                if self.is_virtual_move_legal(virtual_board, piece, move):
                    self.positions_evaluated += 1
                    
                    # Make virtual move
                    captured_piece, old_position, old_moved_once = self.make_virtual_move(virtual_board, piece, move)
                    
                    if color == 'white':
                        value = self.minimax_virtual(virtual_board, self.depth - 1, alpha, beta, False)
                        if value > best_value:
                            best_value = value
                            # Find the real piece that corresponds to this virtual piece
                            real_piece = None
                            for real_p in self.board.pieces:
                                if (real_p.type == piece['type'] and 
                                    real_p.color == piece['color'] and 
                                    real_p.position == old_position):
                                    real_piece = real_p
                                    break
                            best_move = (real_piece, move)
                        alpha = max(alpha, value)
                    else:
                        value = self.minimax_virtual(virtual_board, self.depth - 1, alpha, beta, True)
                        if value < best_value:
                            best_value = value
                            # Find the real piece that corresponds to this virtual piece
                            real_piece = None
                            for real_p in self.board.pieces:
                                if (real_p.type == piece['type'] and 
                                    real_p.color == piece['color'] and 
                                    real_p.position == old_position):
                                    real_piece = real_p
                                    break
                            best_move = (real_piece, move)
                        beta = min(beta, value)
                    
                    # Undo virtual move
                    self.undo_virtual_move(virtual_board, piece, old_position, captured_piece, old_moved_once)
                    
                    if alpha >= beta:
                        break
        
        evaluation_time = time.time() - start_time
        
        if hasattr(self, 'status_display'):
            self.status_display.update_ai_stats(
                self.depth,
                self.positions_evaluated,
                evaluation_time
            )
        
        return best_move

    def minimax_virtual(self, virtual_board, depth, alpha, beta, maximizing_player):
        """Minimax algorithm using virtual board"""
        if depth == 0:
            return self.evaluate_virtual_position(virtual_board)
        
        if maximizing_player:
            max_eval = float('-inf')
            pieces = [p for p in virtual_board if p['color'] == 'white']
            
            for piece in pieces:
                possible_moves = self.get_virtual_possible_moves(virtual_board, piece)
                for move in possible_moves:
                    if self.is_virtual_move_legal(virtual_board, piece, move):
                        # Make virtual move
                        captured_piece, old_position, old_moved_once = self.make_virtual_move(virtual_board, piece, move)
                        
                        eval = self.minimax_virtual(virtual_board, depth - 1, alpha, beta, False)
                        max_eval = max(max_eval, eval)
                        alpha = max(alpha, eval)
                        
                        # Undo virtual move
                        self.undo_virtual_move(virtual_board, piece, old_position, captured_piece, old_moved_once)
                        
                        if beta <= alpha:
                            break
                            
            return max_eval
        else:
            min_eval = float('inf')
            pieces = [p for p in virtual_board if p['color'] == 'black']
            
            for piece in pieces:
                possible_moves = self.get_virtual_possible_moves(virtual_board, piece)
                for move in possible_moves:
                    if self.is_virtual_move_legal(virtual_board, piece, move):
                        # Make virtual move
                        captured_piece, old_position, old_moved_once = self.make_virtual_move(virtual_board, piece, move)
                        
                        eval = self.minimax_virtual(virtual_board, depth - 1, alpha, beta, True)
                        min_eval = min(min_eval, eval)
                        beta = min(beta, eval)
                        
                        # Undo virtual move
                        self.undo_virtual_move(virtual_board, piece, old_position, captured_piece, old_moved_once)
                        
                        if beta <= alpha:
                            break
                            
            return min_eval

    def evaluate_virtual_position(self, virtual_board):
        """Evaluate virtual board position"""
        total_eval = 0
        
        for piece in virtual_board:
            piece_value = self.piece_values[piece['type']]
            position_value = self.get_virtual_position_value(piece)
            
            if piece['color'] == 'white':
                total_eval += piece_value + position_value
            else:
                total_eval -= piece_value + position_value
                
        return total_eval
    
    def get_virtual_position_value(self, piece):
        """Get position value for virtual piece"""
        row, col = piece['position']
        if piece['color'] == 'black':
            row = 7 - row
            
        position_tables = {
            'pawn': self.pawn_table,
            'knight': self.knight_table,
            'bishop': self.bishop_table,
            'rook': self.rook_table,
            'queen': self.queen_table,
            'king': self.king_table
        }
        
        return position_tables[piece['type']][row][col]