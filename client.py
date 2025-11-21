"""
Game client that works with the protocol-based server.
Handles all protocol messages and provides a user interface.
"""
import socket
import sys
from typing import Optional
from protocol import Protocol, MessageType


class GameClient:
    """Client for connecting to and playing games on the server."""
    
    def __init__(self, host: str = 'localhost', port: int = 8000):
        """
        Initialize the game client.
        
        Args:
            host: Server host address
            port: Server port number
        """
        self.host = host
        self.port = port
        self.socket = None
        self.player_id = None
        self.game_name = None
        self.running = False
        self.game_state = None
    
    def connect(self) -> bool:
        """
        Connect to the game server.
        
        Returns:
            True if connection successful, False otherwise
        """
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.host, self.port))
            self.running = True
            print(f"Connected to server at {self.host}:{self.port}")
            return True
        except Exception as e:
            print(f"Error connecting to server: {e}")
            return False
    
    def disconnect(self):
        """Disconnect from the server."""
        self.running = False
        if self.socket:
            try:
                Protocol.send_message(self.socket, MessageType.DISCONNECT)
            except:
                pass
            try:
                self.socket.close()
            except:
                pass
    
    def run(self):
        """Run the client main loop."""
        if not self.connect():
            return
        
        try:
            # Main message loop
            while self.running:
                message = Protocol.receive_message(self.socket)
                if message is None:
                    print("Connection lost")
                    break
                
                self._handle_message(message)
                
        except KeyboardInterrupt:
            print("\nDisconnecting...")
        except Exception as e:
            print(f"Error: {e}")
        finally:
            self.disconnect()
    
    def _handle_message(self, message: dict):
        """Handle incoming protocol messages."""
        msg_type = Protocol.get_message_type(message)
        data = message.get('data', {})
        error = message.get('error')
        
        if error:
            print(f"Error: {error}")
        
        if msg_type == MessageType.CONNECTED:
            self.player_id = data.get('player_id')
            self.game_name = data.get('game_name')
            current_players = data.get('current_players', 0)
            max_players = data.get('max_players', 0)
            print(f"Connected! You are player {self.player_id + 1}")
            print(f"Game: {self.game_name}")
            print(f"Waiting for players... ({current_players}/{max_players})")
        
        elif msg_type == MessageType.GAME_START:
            self.player_id = data.get('player_id')
            self.game_name = data.get('game_name')
            self.game_state = data.get('initial_state')
            help_text = data.get('help', '')
            
            print(f"\n{'='*50}")
            print(f"Game Started: {self.game_name}")
            print(f"You are Player {self.player_id + 1}")
            print(f"{'='*50}")
            if help_text:
                print(f"\n{help_text}\n")
        
        elif msg_type == MessageType.YOUR_TURN:
            self.game_state = data.get('game_state')
            board_display = data.get('board_display', '')
            
            if board_display:
                print(board_display)
            print("\n>>> It's YOUR turn! <<<")
            
            # Get move from user
            self._get_and_send_move()
        
        elif msg_type == MessageType.GAME_STATE:
            self.game_state = data.get('game_state')
            board_display = data.get('board_display', '')
            current_player = data.get('current_player')
            
            if board_display:
                print(board_display)
            print(f"\nWaiting for Player {current_player + 1} to move...")
        
        elif msg_type == MessageType.MOVE_ACCEPTED:
            self.game_state = data.get('game_state')
            board_display = data.get('board_display', '')
            
            if board_display:
                print(board_display)
            print("Move accepted!")
        
        elif msg_type == MessageType.MOVE_REJECTED:
            error_msg = error or "Invalid move"
            print(f"Move rejected: {error_msg}")
            print("Please try again.")
            
            # If it was our turn, ask for another move
            if self.game_state and self.game_state.get('current_player') == self.player_id:
                self._get_and_send_move()
        
        elif msg_type == MessageType.GAME_END:
            won = data.get('won', False)
            draw = data.get('draw', False)
            message = data.get('message', 'Game over')
            
            print(f"\n{'='*50}")
            print(f"GAME OVER")
            print(f"{'='*50}")
            print(message)
            
            if draw:
                print("It's a tie!")
            elif won:
                print("🎉 Congratulations! You won! 🎉")
            else:
                print("Better luck next time!")
            print(f"{'='*50}\n")
            
            self.running = False
        
        elif msg_type == MessageType.ERROR:
            error_msg = error or "Unknown error occurred"
            print(f"Error: {error_msg}")
            if "disconnected" in error_msg.lower() or "ended" in error_msg.lower():
                self.running = False
        
        elif msg_type == MessageType.SERVER_MESSAGE:
            server_msg = data.get('message', '')
            if server_msg:
                print(f"[SERVER] {server_msg}")
        
        else:
            print(f"Unknown message type: {msg_type}")
    
    def _get_and_send_move(self):
        """Get a move from the user and send it to the server."""
        while True:
            try:
                move = input("Enter your move (or 'exit' to quit): ").strip()
                
                if move.lower() == 'exit':
                    self.disconnect()
                    self.running = False
                    return
                
                if not move:
                    continue
                
                # Send move to server
                Protocol.send_message(self.socket, MessageType.MOVE, {
                    'move': move
                })
                break
                
            except (EOFError, KeyboardInterrupt):
                print("\nDisconnecting...")
                self.disconnect()
                self.running = False
                return
            except Exception as e:
                print(f"Error sending move: {e}")
                break


def main():
    """Main entry point for the client."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Connect to game server')
    parser.add_argument('--host', default='localhost', help='Server host address')
    parser.add_argument('--port', type=int, default=8000, help='Server port number')
    
    args = parser.parse_args()
    
    client = GameClient(host=args.host, port=args.port)
    client.run()


if __name__ == "__main__":
    main()
