import os
import pickle
import json
from datetime import datetime
from typing import List, Dict, Optional, Tuple

class SaveManager:
    def __init__(self, save_directory="saved_games"):
        self.save_directory = save_directory
        self.metadata_file = os.path.join(save_directory, "game_metadata.json")
        self._ensure_save_directory()
        
    def _ensure_save_directory(self):
        """Create save directory if it doesn't exist"""
        if not os.path.exists(self.save_directory):
            os.makedirs(self.save_directory)
            
    def _load_metadata(self) -> Dict:
        """Load game metadata from JSON file"""
        if os.path.exists(self.metadata_file):
            try:
                with open(self.metadata_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                return {"games": []}
        return {"games": []}
    
    def _save_metadata(self, metadata: Dict):
        """Save game metadata to JSON file"""
        with open(self.metadata_file, 'w') as f:
            json.dump(metadata, f, indent=2)
    
    def save_game(self, chess_board, game_rules, game_mode: str, save_name: str = None) -> Tuple[bool, str]:
        """
        Save a game with metadata
        Returns: (success: bool, message: str)
        """
        try:
            metadata = self._load_metadata()
            
            # Generate save name if not provided
            if not save_name:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                save_name = f"game_{timestamp}"
            
            # Clean save name for filename
            filename = f"{save_name.replace(' ', '_').replace('/', '_')}.pkl"
            file_path = os.path.join(self.save_directory, filename)
            
            # Check if save name already exists
            existing_game = next((g for g in metadata["games"] if g["name"] == save_name), None)
            if existing_game:
                return False, f"A game with name '{save_name}' already exists"
            
            # Create game state compatible with your existing structure
            game_state = {
                'board': [(p.type, p.color, p.position) for p in chess_board.pieces],
                'current_turn': game_rules.current_turn,
                'game_mode': game_mode,
                'move_history': game_rules.move_history
            }
            
            # Save game file
            with open(file_path, 'wb') as f:
                pickle.dump(game_state, f)
            
            # Update metadata
            game_info = {
                "name": save_name,
                "filename": filename,
                "game_mode": game_mode,
                "current_turn": game_rules.current_turn,
                "save_date": datetime.now().isoformat(),
                "move_count": len(game_rules.move_history)
            }
            
            metadata["games"].append(game_info)
            self._save_metadata(metadata)
            
            return True, f"Game '{save_name}' saved successfully"
            
        except Exception as e:
            return False, f"Failed to save game: {str(e)}"
    
    def load_game(self, save_name: str, chess_board, game_rules) -> Tuple[bool, str, str]:
        """
        Load a game by save name
        Returns: (success: bool, message: str, game_mode: str)
        """
        try:
            metadata = self._load_metadata()
            game_info = next((g for g in metadata["games"] if g["name"] == save_name), None)
            
            if not game_info:
                return False, f"Game '{save_name}' not found", ""
            
            file_path = os.path.join(self.save_directory, game_info["filename"])
            
            if not os.path.exists(file_path):
                return False, f"Save file not found for '{save_name}'", ""
            
            with open(file_path, 'rb') as f:
                game_state = pickle.load(f)
            
            # Restore game state
            chess_board.pieces = [
                chess_board.create_piece(piece_type, color, position)
                for piece_type, color, position in game_state['board']
            ]
            game_rules.current_turn = game_state['current_turn']
            game_rules.move_history = game_state.get('move_history', [])
            
            return True, f"Game '{save_name}' loaded successfully", game_state.get('game_mode', 'Human_vs_Human')
            
        except Exception as e:
            return False, f"Failed to load game: {str(e)}", ""
    
    def get_saved_games(self) -> List[Dict]:
        """Get list of all saved games with metadata"""
        metadata = self._load_metadata()
        return metadata.get("games", [])
    
    def delete_game(self, save_name: str) -> Tuple[bool, str]:
        """Delete a saved game"""
        try:
            metadata = self._load_metadata()
            game_info = next((g for g in metadata["games"] if g["name"] == save_name), None)
            
            if not game_info:
                return False, f"Game '{save_name}' not found"
            
            # Remove file
            file_path = os.path.join(self.save_directory, game_info["filename"])
            if os.path.exists(file_path):
                os.remove(file_path)
            
            # Update metadata
            metadata["games"] = [g for g in metadata["games"] if g["name"] != save_name]
            self._save_metadata(metadata)
            
            return True, f"Game '{save_name}' deleted successfully"
            
        except Exception as e:
            return False, f"Failed to delete game: {str(e)}"