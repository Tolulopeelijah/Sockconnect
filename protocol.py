"""
Protocol module for server-client communication.
Defines message types and serialization/deserialization.
"""
import json
from enum import Enum
from typing import Dict, Any, Optional


class MessageType(Enum):
    """Message types for protocol communication."""
    # Connection messages
    CONNECT = "CONNECT"
    CONNECTED = "CONNECTED"
    DISCONNECT = "DISCONNECT"
    
    # Game messages
    GAME_START = "GAME_START"
    GAME_STATE = "GAME_STATE"
    GAME_END = "GAME_END"
    
    # Turn messages
    YOUR_TURN = "YOUR_TURN"
    MOVE = "MOVE"
    MOVE_ACCEPTED = "MOVE_ACCEPTED"
    MOVE_REJECTED = "MOVE_REJECTED"
    
    # Error messages
    ERROR = "ERROR"
    
    # Server control
    SERVER_MESSAGE = "SERVER_MESSAGE"


class Protocol:
    """Handles message serialization and deserialization."""
    
    @staticmethod
    def create_message(msg_type: MessageType, data: Optional[Dict[str, Any]] = None, 
                      error: Optional[str] = None) -> str:
        """
        Create a protocol message.
        
        Args:
            msg_type: Type of message
            data: Optional data dictionary
            error: Optional error message
            
        Returns:
            JSON-encoded message string
        """
        message = {
            "type": msg_type.value,
        }
        
        if data is not None:
            message["data"] = data
        if error is not None:
            message["error"] = error
            
        return json.dumps(message)
    
    @staticmethod
    def parse_message(message: str) -> Dict[str, Any]:
        """
        Parse a protocol message.
        
        Args:
            message: JSON-encoded message string
            
        Returns:
            Parsed message dictionary
        """
        try:
            return json.loads(message)
        except json.JSONDecodeError:
            return {
                "type": MessageType.ERROR.value,
                "error": "Invalid message format"
            }
    
    @staticmethod
    def get_message_type(message_dict: Dict[str, Any]) -> Optional[MessageType]:
        """Extract message type from parsed message."""
        msg_type_str = message_dict.get("type")
        if msg_type_str:
            try:
                return MessageType(msg_type_str)
            except ValueError:
                return None
        return None
    
    @staticmethod
    def send_message(socket, msg_type: MessageType, data: Optional[Dict[str, Any]] = None,
                    error: Optional[str] = None) -> bool:
        """
        Send a protocol message through a socket.
        
        Args:
            socket: Socket object to send through
            msg_type: Type of message
            data: Optional data dictionary
            error: Optional error message
            
        Returns:
            True if successful, False otherwise
        """
        try:
            message = Protocol.create_message(msg_type, data, error)
            # Send message length first, then message
            message_bytes = message.encode('utf-8')
            length = len(message_bytes)
            socket.sendall(length.to_bytes(4, byteorder='big'))
            socket.sendall(message_bytes)
            return True
        except Exception as e:
            print(f"Error sending message: {e}")
            return False
    
    @staticmethod
    def receive_message(socket) -> Optional[Dict[str, Any]]:
        """
        Receive a protocol message from a socket.
        
        Args:
            socket: Socket object to receive from
            
        Returns:
            Parsed message dictionary or None if error
        """
        try:
            # Receive message length first
            length_bytes = socket.recv(4)
            if len(length_bytes) < 4:
                return None
            length = int.from_bytes(length_bytes, byteorder='big')
            
            # Receive the actual message
            message_bytes = b''
            while len(message_bytes) < length:
                chunk = socket.recv(length - len(message_bytes))
                if not chunk:
                    return None
                message_bytes += chunk
            
            message = message_bytes.decode('utf-8')
            return Protocol.parse_message(message)
        except Exception as e:
            print(f"Error receiving message: {e}")
            return None

