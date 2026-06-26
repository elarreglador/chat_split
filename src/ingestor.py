"""Ingestion module for msg_split"""

import os
from typing import List
from src.models import Message, Conversation
from src.persist import read_jsonl

def read_previous_state(filename: str = "conversaciones.jsonl") -> List[Conversation]:
    """Read previous state from JSONL file"""
    if not os.path.exists(filename):
        return []
    return read_jsonl(filename)

def filter_new_messages(messages: List[Message], 
                       last_end_time: str) -> List[Message]:
    """Filter messages that are newer than last end_time"""
    if not last_end_time:
        return messages
    
    filtered = []
    for msg in messages:
        # Skip messages with equal or older timestamps
        if msg.date > last_end_time:
            filtered.append(msg)
    
    return filtered

def get_last_end_time(conversations: List[Conversation]) -> str:
    """Get the latest end_time from previous conversations"""
    if not conversations:
        return ""
    
    # Get the most recent conversation's end time
    latest = max(conversations, key=lambda c: c.end_time)
    return latest.end_time