"""New adapter for chatExport format"""

import json
from typing import List
from src.adapters.base import TelegramAdapter
from src.models import Message

class ChatExportAdapter(TelegramAdapter):
    """Adapter for parsing chat export files in the new format"""
    
    def parse(self, path: str) -> List[Message]:
        """Parse chat export JSON and return list of messages"""
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        messages = []
        # The chatExport has a different structure - directly get messages
        for msg_data in data.get('messages', []):
            # Extract relevant fields (same structure as Telegram JSON)
            message = Message(
                id=msg_data.get('id'),
                date=msg_data.get('date'),
                from_user=msg_data.get('from', ''),
                text=msg_data.get('text', '')
            )
            messages.append(message)
        
        return messages