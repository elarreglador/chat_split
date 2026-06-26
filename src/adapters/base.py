"""Base adapter for Telegram log formats"""

from abc import ABC, abstractmethod
from typing import List
from src.models import Message

class TelegramAdapter(ABC):
    """Abstract base class forTelegram log adapters"""
    
    @abstractmethod
    def parse(self, path: str) -> List[Message]:
        """Parse Telegram log file and return list of messages"""
        pass