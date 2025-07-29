from piece import King

class GameRules:
    def __init__(self, board):
        self.board = board
        self.current_turn = 'black'
        #invert colours
        self.move_history = []

    def switch_turn(self):
        self.current_turn = 'black' if self.current_turn == 'white' else 'white'

    def is_in_check(self, color):
        
        king = next((piece for piece in self.board.pieces if isinstance(piece, King) and piece.color == color), None)
        if not king:
            return False

        king_pos = king.position
        opponent_pieces = [p for p in self.board.pieces if p.color != color]

        for piece in opponent_pieces:
            if king_pos in piece.get_possible_moves(self.board):
                return True
        return False

    def is_move_legal(self, piece, destination):
        initial_position = piece.position
        target_piece = self.board.get_piece_at(destination)
        
        piece.position = destination
        if target_piece:
            self.board.pieces.remove(target_piece)
        
        in_check = self.is_in_check(piece.color)
        
        piece.position = initial_position
        if target_piece:
            self.board.pieces.append(target_piece)
        
        return not in_check

    def is_checkmate(self, color):
        if not self.is_in_check(color):
            return False

        pieces = [p for p in self.board.pieces if p.color == color]
        for piece in pieces:
            possible_moves = piece.get_possible_moves(self.board)
            for move in possible_moves:
                if self.is_move_legal(piece, move):
                    return False 
        return True

    def is_stalemate(self, color):
        if self.is_in_check(color):
            return False

        pieces = [p for p in self.board.pieces if p.color == color]
        for piece in pieces:
            possible_moves = piece.get_possible_moves(self.board)
            for move in possible_moves:
                if self.is_move_legal(piece, move):
                    return False 
        return True

    def is_game_over(self):
        if self.is_checkmate(self.current_turn):
            # return f"Checkmate! {self.current_turn} wins."
            return f"Checkmate!"
        elif self.is_stalemate(self.current_turn):
            return "Stalemate!"
        return None
    
    def position_to_notation(self, pos):
        column = chr(pos[1] + ord('a'))  # 'a' to 'h'
        row = str(8 - pos[0])  # '1' to '8'
        return f"{column}{row}"
    
    def record_move(self, piece, from_pos, to_pos, captured_piece=None):
        if (piece.color == 'white'):
            tempcolor = 'black'
        else:
            tempcolor = 'white'
        move = {
            'piece': piece.type,
            'color': tempcolor, # replace with piece.color for original
            'from': self.position_to_notation(from_pos),
            'to': self.position_to_notation(to_pos),
            'captured': captured_piece.type if captured_piece else None
        }
        self.move_history.append(move)

