"""
Game server that works with any game logic implementing GameInterface.
Uses the protocol module for structured communication.
"""
import socket
import threading
import sys
from typing import List, Tuple, Optional, Dict
from protocol import Protocol, MessageType
from game_interface import GameInterface


class GameServer:
    """Server that manages game sessions with multiple players."""
    
    def __init__(self, host: str = 'localhost', port: int = 8000, 
                 game_logic: GameInterface = None):
        """
        Initialize the game server.
        
        Args:
            host: Host address to bind to
            port: Port number to listen on
            game_logic: GameInterface implementation to use
        """
        if game_logic is None:
            from game_logic import TicTacToeGame
            game_logic = TicTacToeGame()
        
        self.host = host
        self.port = port
        self.game_logic = game_logic
        self.server_socket = None
        self.running = False
        self.logging = True
        
    def log(self, message: str):
        """Log a message if logging is enabled."""
        if self.logging:
            print(f"[SERVER] {message}")
    
    def start(self):
        """Start the server and wait for connections."""
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        try:
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(5)
            self.running = True
            self.log(f"Server started on {self.host}:{self.port}")
            self.log(f"Waiting for players to connect...")
            self.log(f"Game: {self.game_logic.get_game_name()}")
            self.log(f"Players required: {self.game_logic.get_min_players()}-{self.game_logic.get_max_players()}")
            
            # Start server control thread
            control_thread = threading.Thread(target=self._handle_server_commands, daemon=True)
            control_thread.start()
            
            # Wait for players and start game
            self._wait_for_players_and_start_game()
            
        except Exception as e:
            self.log(f"Error starting server: {e}")
            raise
        finally:
            self.stop()
    
    def stop(self):
        """Stop the server and close connections."""
        self.running = False
        if self.server_socket:
            try:
                self.server_socket.close()
            except:
                pass
        self.log("Server stopped")
    
    def _handle_server_commands(self):
        """Handle server control commands in a separate thread."""
        while self.running:
            try:
                cmd = input()
                if cmd.lower() == 'exit':
                    self.log("Shutting down server...")
                    self.running = False
                    if self.server_socket:
                        self.server_socket.close()
                    break
            except (EOFError, KeyboardInterrupt):
                break
    
    def _wait_for_players_and_start_game(self):
        """Wait for required number of players and start a game session."""
        min_players = self.game_logic.get_min_players()
        max_players = self.game_logic.get_max_players()
        
        players: List[Tuple[socket.socket, str]] = []
        
        self.log(f"Waiting for {min_players} to {max_players} players...")
        
        # Accept players
        while len(players) < max_players and self.running:
            try:
                self.server_socket.settimeout(1.0)  # Check for shutdown every second
                client_socket, address = self.server_socket.accept()
                self.log(f"Player {len(players) + 1} connected from {address}")
                
                # Send connection confirmation
                Protocol.send_message(client_socket, MessageType.CONNECTED, {
                    'player_id': len(players),
                    'game_name': self.game_logic.get_game_name(),
                    'min_players': min_players,
                    'max_players': max_players,
                    'current_players': len(players) + 1
                })
                
                players.append((client_socket, address))
                
                # Start game when we have minimum players
                if len(players) >= min_players:
                    self.log(f"Starting game with {len(players)} players")
                    self._run_game_session(players)
                    break
                    
            except socket.timeout:
                continue
            except Exception as e:
                self.log(f"Error accepting connection: {e}")
                break
    
    def _run_game_session(self, players: List[Tuple[socket.socket, str]]):
        """Run a game session with the connected players."""
        try:
            # Initialize game
            game_state = self.game_logic.initialize_game(len(players))
            
            # Send game start message to all players
            for idx, (client_socket, _) in enumerate(players):
                player_state = self.game_logic.get_game_state_for_player(game_state, idx)
                Protocol.send_message(client_socket, MessageType.GAME_START, {
                    'player_id': idx,
                    'game_name': self.game_logic.get_game_name(),
                    'initial_state': player_state,
                    'help': self.game_logic.get_move_help()
                })
            
            self.log("Game started!")
            self.log(self.game_logic.format_state_for_display(game_state))
            
            # Game loop
            while self.running:
                # Check if game is over
                game_result = self.game_logic.check_game_over(game_state)
                if game_result:
                    self._handle_game_end(players, game_result)
                    break
                
                # Get current player
                current_player_id = self.game_logic.get_current_player(game_state)
                current_player_socket, _ = players[current_player_id]
                
                # Notify current player it's their turn
                player_state = self.game_logic.get_game_state_for_player(
                    game_state, current_player_id
                )
                Protocol.send_message(current_player_socket, MessageType.YOUR_TURN, {
                    'game_state': player_state,
                    'board_display': self.game_logic.format_state_for_display(game_state)
                })
                
                # Notify other players
                for idx, (client_socket, _) in enumerate(players):
                    if idx != current_player_id:
                        player_state = self.game_logic.get_game_state_for_player(
                            game_state, idx
                        )
                        Protocol.send_message(client_socket, MessageType.GAME_STATE, {
                            'game_state': player_state,
                            'board_display': self.game_logic.format_state_for_display(game_state),
                            'current_player': current_player_id
                        })
                
                # Wait for move from current player
                move_received = False
                while not move_received and self.running:
                    message = Protocol.receive_message(current_player_socket)
                    if message is None:
                        self.log(f"Player {current_player_id + 1} disconnected")
                        self._handle_player_disconnect(players, current_player_id)
                        return
                    
                    msg_type = Protocol.get_message_type(message)
                    
                    if msg_type == MessageType.MOVE:
                        move = message.get('data', {}).get('move')
                        if move is None:
                            Protocol.send_message(current_player_socket, 
                                                MessageType.MOVE_REJECTED,
                                                error="No move provided")
                            continue
                        
                        # Validate move
                        is_valid, error_msg = self.game_logic.validate_move(
                            game_state, current_player_id, move
                        )
                        
                        if is_valid:
                            # Apply move
                            game_state = self.game_logic.apply_move(
                                game_state, current_player_id, move
                            )
                            
                            self.log(f"Player {current_player_id + 1} played: {move}")
                            self.log(self.game_logic.format_state_for_display(game_state))
                            
                            # Send acceptance to player
                            player_state = self.game_logic.get_game_state_for_player(
                                game_state, current_player_id
                            )
                            Protocol.send_message(current_player_socket, 
                                                MessageType.MOVE_ACCEPTED, {
                                'game_state': player_state,
                                'board_display': self.game_logic.format_state_for_display(game_state)
                            })
                            
                            # Update all players with new state
                            for idx, (client_socket, _) in enumerate(players):
                                if idx != current_player_id:
                                    player_state = self.game_logic.get_game_state_for_player(
                                        game_state, idx
                                    )
                                    Protocol.send_message(client_socket, 
                                                        MessageType.GAME_STATE, {
                                        'game_state': player_state,
                                        'board_display': self.game_logic.format_state_for_display(game_state)
                                    })
                            
                            move_received = True
                        else:
                            # Send rejection
                            Protocol.send_message(current_player_socket, 
                                                MessageType.MOVE_REJECTED,
                                                error=error_msg or "Invalid move")
                    
                    elif msg_type == MessageType.DISCONNECT:
                        self.log(f"Player {current_player_id + 1} disconnected")
                        self._handle_player_disconnect(players, current_player_id)
                        return
                    
                    else:
                        Protocol.send_message(current_player_socket, 
                                            MessageType.ERROR,
                                            error="Unexpected message type")
            
        except Exception as e:
            self.log(f"Error in game session: {e}")
            import traceback
            traceback.print_exc()
        finally:
            # Close all connections
            for client_socket, _ in players:
                try:
                    client_socket.close()
                except:
                    pass
    
    def _handle_game_end(self, players: List[Tuple[socket.socket, str]], 
                        game_result: Dict):
        """Handle game end and notify all players."""
        self.log(game_result['message'])
        
        for idx, (client_socket, _) in enumerate(players):
            result_data = {
                'winner': game_result.get('winner'),
                'draw': game_result.get('draw', False),
                'message': game_result['message']
            }
            
            if game_result.get('draw'):
                result_data['won'] = False
            else:
                result_data['won'] = (game_result.get('winner') == idx)
            
            Protocol.send_message(client_socket, MessageType.GAME_END, result_data)
    
    def _handle_player_disconnect(self, players: List[Tuple[socket.socket, str]], 
                                 disconnected_player_id: int):
        """Handle a player disconnecting."""
        # Notify remaining players
        for idx, (client_socket, _) in enumerate(players):
            if idx != disconnected_player_id:
                try:
                    Protocol.send_message(client_socket, MessageType.ERROR,
                                        error=f"Player {disconnected_player_id + 1} disconnected. Game ended.")
                except:
                    pass
        
        # Close all connections
        for client_socket, _ in players:
            try:
                client_socket.close()
            except:
                pass


def main():
    """Main entry point for the server."""
    # You can change the game logic here
    from game_logic import TicTacToeGame
    game = TicTacToeGame()
    
    server = GameServer(host='localhost', port=8000, game_logic=game)
    try:
        server.start()
    except KeyboardInterrupt:
        server.log("\nServer interrupted by user")
        server.stop()
        sys.exit(0)


if __name__ == "__main__":
    main()
