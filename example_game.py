"""
Example of how to create a new game logic implementation.
This shows a simple Rock-Paper-Scissors game as an example.
"""
from game_interface import GameInterface
from typing import Dict, Any, Optional, Tuple
import random


class RockPaperScissorsGame(GameInterface):
    """Simple Rock-Paper-Scissors game implementation."""
    
    CHOICES = ['rock', 'paper', 'scissors']
    
    def get_game_name(self) -> str:
        return 'Rock-Paper-Scissors'
    
    def get_min_players(self) -> int:
        return 2
    
    def get_max_players(self) -> int:
        return 2
    
    def initialize_game(self, num_players: int) -> Dict[str, Any]:
        if num_players != 2:
            raise ValueError("Rock-Paper-Scissors requires exactly 2 players")
        
        return {
            'round': 1,
            'player1_choice': None,
            'player2_choice': None,
            'player1_score': 0,
            'player2_score': 0,
            'current_player': 0,
            'players': num_players
        }
    
    def validate_move(self, game_state: Dict[str, Any], player_id: int, 
                     move: Any) -> Tuple[bool, Optional[str]]:
        if game_state['current_player'] != player_id:
            return False, "It's not your turn"
        
        move_lower = str(move).lower().strip()
        if move_lower not in self.CHOICES:
            return False, f"Move must be one of: {', '.join(self.CHOICES)}"
        
        # Check if both players have made their choice
        if player_id == 0 and game_state.get('player1_choice') is not None:
            return False, "You have already made your choice this round"
        if player_id == 1 and game_state.get('player2_choice') is not None:
            return False, "You have already made your choice this round"
        
        return True, None
    
    def apply_move(self, game_state: Dict[str, Any], player_id: int, 
                   move: Any) -> Dict[str, Any]:
        new_state = game_state.copy()
        move_lower = str(move).lower().strip()
        
        if player_id == 0:
            new_state['player1_choice'] = move_lower
        else:
            new_state['player2_choice'] = move_lower
        
        # If both players have chosen, determine winner and advance
        if (new_state['player1_choice'] and new_state['player2_choice']):
            winner = self._determine_winner(
                new_state['player1_choice'],
                new_state['player2_choice']
            )
            if winner == 0:
                new_state['player1_score'] += 1
            elif winner == 1:
                new_state['player2_score'] += 1
            
            # Reset for next round
            new_state['round'] += 1
            new_state['player1_choice'] = None
            new_state['player2_choice'] = None
        
        # Switch player
        new_state['current_player'] = (player_id + 1) % 2
        
        return new_state
    
    def _determine_winner(self, choice1: str, choice2: str) -> Optional[int]:
        """Determine winner: 0 = player1, 1 = player2, None = tie"""
        if choice1 == choice2:
            return None
        
        wins = {
            'rock': 'scissors',
            'paper': 'rock',
            'scissors': 'paper'
        }
        
        if wins[choice1] == choice2:
            return 0
        return 1
    
    def check_game_over(self, game_state: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        # Play best of 3 rounds
        if game_state['round'] > 3:
            p1_score = game_state['player1_score']
            p2_score = game_state['player2_score']
            
            if p1_score > p2_score:
                return {
                    'over': True,
                    'winner': 0,
                    'draw': False,
                    'message': f"Player 1 wins {p1_score}-{p2_score}!"
                }
            elif p2_score > p1_score:
                return {
                    'over': True,
                    'winner': 1,
                    'draw': False,
                    'message': f"Player 2 wins {p2_score}-{p1_score}!"
                }
            else:
                return {
                    'over': True,
                    'winner': None,
                    'draw': True,
                    'message': f"It's a tie! {p1_score}-{p2_score}"
                }
        return None
    
    def get_current_player(self, game_state: Dict[str, Any]) -> int:
        return game_state['current_player']
    
    def get_game_state_for_player(self, game_state: Dict[str, Any], 
                                  player_id: int) -> Dict[str, Any]:
        # Hide opponent's choice until both have chosen
        player_state = game_state.copy()
        if player_id == 0:
            if game_state.get('player2_choice') and not game_state.get('player1_choice'):
                # Opponent has chosen but we haven't - hide their choice
                player_state['player2_choice'] = '?'
        else:
            if game_state.get('player1_choice') and not game_state.get('player2_choice'):
                # Opponent has chosen but we haven't - hide their choice
                player_state['player1_choice'] = '?'
        return player_state
    
    def format_state_for_display(self, game_state: Dict[str, Any]) -> str:
        lines = [
            f"\nRound {game_state['round']}/3",
            f"Score: Player 1: {game_state['player1_score']} | Player 2: {game_state['player2_score']}"
        ]
        
        if game_state.get('player1_choice'):
            lines.append(f"Player 1 chose: {game_state['player1_choice']}")
        else:
            lines.append("Player 1: waiting...")
        
        if game_state.get('player2_choice'):
            lines.append(f"Player 2 chose: {game_state['player2_choice']}")
        else:
            lines.append("Player 2: waiting...")
        
        return '\n'.join(lines)
    
    def get_move_help(self) -> str:
        return "Enter one of: rock, paper, or scissors"


# To use this game, modify server.py:
# from example_game import RockPaperScissorsGame
# game = RockPaperScissorsGame()
# server = GameServer(host='localhost', port=8000, game_logic=game)

