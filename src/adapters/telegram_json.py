"""Telegram JSON adapter for result.json exports"""

import json
from typing import List
from src.adapters.base import TelegramAdapter
from src.models import Message

class TelegramJsonAdapter(TelegramAdapter):
    """Adapter for parsing Telegram Desktop's result.json export format"""
    
    def parse(self, path: str) -> List[Message]:
        """Parse result.json and return list of messages"""
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        messages = []
        for msg_data in data.get('messages', []):
            # Extract relevant fields
            message = Message(
                id=msg_data.get('id'),
                date=msg_data.get('date'),
                from_user=msg_data.get('from', ''),
                text=msg_data.get('text', '')
            )
            messages.append(message)
        
        return messages