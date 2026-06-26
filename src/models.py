"""Data models for msg_split"""

from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

@dataclass
class Message:
    """Represents a single message in Telegram log"""
    id: int
    date: str  # ISO format string
    from_user: str
    text: str
    
    def to_datetime(self) -> datetime:
        """Convert date string to datetime object"""
        return datetime.fromisoformat(self.date.replace('Z', '+00:00'))

@dataclass
class Conversation:
    """Represents a conversation segment"""
    conversation_id: str
    participants: List[str]
    start_time: str  # ISO format string
    end_time: str  # ISO format string
    message_count: int
    raw_content: str
    summary: Optional[str] = None