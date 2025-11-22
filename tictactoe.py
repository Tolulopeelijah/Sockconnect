"""
Tic-Tac-Toe game logic implementation.
Implements the GameInterface for use with the server-client protocol.
"""
from game_interface import GameInterface
from typing import Dict, Any, Optional, Tuple


class TicTacToeGame(GameInterface):
    """Tic-Tac-Toe game implementation."""
    
    def __init__(self):
        self.symbols = ['X', 'O']
    
    def get_game_name(self) -> str:
        """Return the name of the game."""
        return 'Tic-Tac-Toe'
    
    def get_min_players(self) -> int:
        """Return the minimum number of players required."""
        return 2
    
    def get_max_players(self) -> int:
        """Return the maximum number of players allowed."""
        return 2
    
    def initialize_game(self, num_players: int) -> Dict[str, Any]:
        """
        Initialize a new game instance.
        
        Args:
            num_players: Number of players in the game
            
        Returns:
            Dictionary with initial game state
        """
        if num_players != 2:
            raise ValueError("Tic-Tac-Toe requires exactly 2 players")
        
        return {
            'board': ['#'] * 9,
            'current_player': 0,
            'move_count': 0,
            'players': num_players
        }
    
    def validate_move(self, game_state: Dict[str, Any], player_id: int, 
                     move: Any) -> Tuple[bool, Optional[str]]:
        """
        Validate a move from a player.
        
        Args:
            game_state: Current game state
            player_id: ID of the player making the move (0-indexed)
            move: The move to validate (should be 1-9)
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        board = game_state['board']
        
        # Check if it's the player's turn
        if game_state['current_player'] != player_id:
            return False, "It's not your turn"
        
        # Try to convert move to integer
        try:
            move_int = int(move)
        except (ValueError, TypeError):
            return False, "Move must be a number between 1 and 9"
        
        # Check if move is in valid range
        if move_int < 1 or move_int > 9:
            return False, "Move must be a number between 1 and 9"
        
        # Check if position is empty (convert to 0-indexed)
        position = move_int - 1
        if board[position] != '#':
            return False, f"Position {move_int} is already taken"
        
        return True, None
    
    def apply_move(self, game_state: Dict[str, Any], player_id: int, 
                   move: Any) -> Dict[str, Any]:
        """
        Apply a move to the game state.
        
        Args:
            game_state: Current game state
            player_id: ID of the player making the move (0-indexed)
            move: The move to apply
            
        Returns:
            Updated game state dictionary
        """
        new_state = game_state.copy()
        board = new_state['board'].copy()
        
        # Convert move to position (1-indexed to 0-indexed)
        position = int(move) - 1
        symbol = self.symbols[player_id]
        
        # Apply the move
        board[position] = symbol
        new_state['board'] = board
        new_state['move_count'] = new_state['move_count'] + 1
        new_state['current_player'] = (player_id + 1) % 2
        
        return new_state
    
    def check_game_over(self, game_state: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Check if the game is over and determine the result.
        
        Args:
            game_state: Current game state
            
        Returns:
            None if game is not over, otherwise a dictionary with game result
        """
        board = game_state['board']
        winning_positions = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
            [0, 4, 8], [2, 4, 6]              # Diagonals
        ]
        
        # Check for winner
        for positions in winning_positions:
            symbols = [board[pos] for pos in positions]
            if symbols[0] != '#' and all(s == symbols[0] for s in symbols):
                winner_symbol = symbols[0]
                winner_id = self.symbols.index(winner_symbol)
                return {
                    'over': True,
                    'winner': winner_id,
                    'draw': False,
                    'message': f"Player {winner_id + 1} ({winner_symbol}) wins!"
                }
        
        # Check for draw
        if '#' not in board:
            return {
                'over': True,
                'winner': None,
                'draw': True,
                'message': "The game is a draw!"
            }
        
        return None
    
    def get_current_player(self, game_state: Dict[str, Any]) -> int:
        """
        Get the ID of the player whose turn it is.
        
        Args:
            game_state: Current game state
            
        Returns:
            Player ID (0-indexed)
        """
        return game_state['current_player']
    
    def get_game_state_for_player(self, game_state: Dict[str, Any], 
                                  player_id: int) -> Dict[str, Any]:
        """
        Get the game state visible to a specific player.
        For Tic-Tac-Toe, all players see the same state.
        
        Args:
            game_state: Full game state
            player_id: ID of the player requesting state
            
        Returns:
            Game state dictionary for the player
        """
        # Tic-Tac-Toe has no hidden information, return full state
        return game_state.copy()
    
    def format_state_for_display(self, game_state: Dict[str, Any]) -> str:
        """
        Format the game state as a string for display.
        
        Args:
            game_state: Current game state
            
        Returns:
            Formatted string representation
        """
        board = game_state['board']
        lines = ['\n' + '-'*13]
        for row in range(3):
            line = '| '
            for col in range(3):
                pos = row * 3 + col
                val = board[pos] if board[pos] != '#' else str(pos + 1)
                line += f"{val} | "
            lines.append(line)
            if row < 2:
                lines.append('-'*13)
        lines.append('-'*13)
        return '\n'.join(lines)
    
    def get_move_help(self) -> str:
        """
        Get help text explaining how to make moves.
        
        Returns:
            Help string
        """
        return (
            "Enter a number from 1-9 to place your mark.\n"
            "Board positions:\n"
            "1 | 2 | 3\n"
            "4 | 5 | 6\n"
            "7 | 8 | 9"
        )


# Create a global instance for backward compatibility
_game_instance = TicTacToeGame()

# Backward compatibility functions (deprecated, use TicTacToeGame class instead)
def display(board):
    """Display the board (backward compatibility)."""
    state = {'board': board}
    print(_game_instance.format_state_for_display(state))

def validate(board, move) -> bool:
    """Validate a move (backward compatibility)."""
    state = {'board': board, 'current_player': 0, 'move_count': 0, 'players': 2}
    is_valid, _ = _game_instance.validate_move(state, 0, move)
    return is_valid

def check_win(board) -> Optional[str]:
    """Check for win condition (backward compatibility)."""
    state = {'board': board, 'current_player': 0, 'move_count': 0, 'players': 2}
    result = _game_instance.check_game_over(state)
    if result:
        if result['draw']:
            return 'draw'
        elif result['winner'] == 0:
            return 'X'
        elif result['winner'] == 1:
            return 'O'
    return None

def update(board, move, player):
    """Update the board (backward compatibility)."""
    state = {'board': board, 'current_player': 0, 'move_count': 0, 'players': 2}
    player_id = 0 if player == 'X' else 1
    new_state = _game_instance.apply_move(state, player_id, move)
    board[:] = new_state['board']  # Update board in place
    return None
