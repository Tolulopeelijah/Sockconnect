"""
Abstract interface for game logic implementations.
Any game logic module should implement these methods.
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List, Tuple


class GameInterface(ABC):
    """Abstract base class for game logic implementations."""
    
    @abstractmethod
    def get_game_name(self) -> str:
        """Return the name of the game."""
        pass
    
    @abstractmethod
    def get_min_players(self) -> int:
        """Return the minimum number of players required."""
        pass
    
    @abstractmethod
    def get_max_players(self) -> int:
        """Return the maximum number of players allowed."""
        pass
    
    @abstractmethod
    def initialize_game(self, num_players: int) -> Dict[str, Any]:
        """
        Initialize a new game instance.
        
        Args:
            num_players: Number of players in the game
            
        Returns:
            Dictionary with initial game state
        """
        pass
    
    @abstractmethod
    def validate_move(self, game_state: Dict[str, Any], player_id: int, 
                     move: Any) -> Tuple[bool, Optional[str]]:
        """
        Validate a move from a player.
        
        Args:
            game_state: Current game state
            player_id: ID of the player making the move (0-indexed)
            move: The move to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        pass
    
    @abstractmethod
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
        pass
    
    @abstractmethod
    def check_game_over(self, game_state: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Check if the game is over and determine the result.
        
        Args:
            game_state: Current game state
            
        Returns:
            None if game is not over, otherwise a dictionary with:
            - 'over': True
            - 'winner': player_id of winner (or None for draw)
            - 'draw': True if it's a draw
            - 'message': Result message
        """
        pass
    
    @abstractmethod
    def get_current_player(self, game_state: Dict[str, Any]) -> int:
        """
        Get the ID of the player whose turn it is.
        
        Args:
            game_state: Current game state
            
        Returns:
            Player ID (0-indexed)
        """
        pass
    
    @abstractmethod
    def get_game_state_for_player(self, game_state: Dict[str, Any], 
                                  player_id: int) -> Dict[str, Any]:
        """
        Get the game state visible to a specific player.
        This allows for games with hidden information.
        
        Args:
            game_state: Full game state
            player_id: ID of the player requesting state
            
        Returns:
            Game state dictionary for the player
        """
        pass
    
    @abstractmethod
    def format_state_for_display(self, game_state: Dict[str, Any]) -> str:
        """
        Format the game state as a string for display.
        
        Args:
            game_state: Current game state
            
        Returns:
            Formatted string representation
        """
        pass
    
    @abstractmethod
    def get_move_help(self) -> str:
        """
        Get help text explaining how to make moves.
        
        Returns:
            Help string
        """
        pass

