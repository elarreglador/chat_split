"""Persistence module for msg_split"""

import json
from typing import List
from src.models import Conversation

def read_jsonl(filename: str) -> List[Conversation]:
    """Read conversations from JSONL file"""
    conversations = []
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    data = json.loads(line)
                    conversations.append(Conversation(**data))
    except FileNotFoundError:
        pass  # Return empty list if file doesn't exist
    
    return conversations

def append_jsonl(filename: str, conversations: List[Conversation]) -> None:
    """Append conversations to JSONL file"""
    with open(filename, 'a', encoding='utf-8') as f:
        for conv in conversations:
            f.write(json.dumps(conv.__dict__, ensure_ascii=False) + '\n')