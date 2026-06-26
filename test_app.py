"""Test the actual application functionality with sample data"""

import sys
import os
import json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.adapters.telegram_json import TelegramJsonAdapter
from src.segmenter import segment_messages
from src.persist import append_jsonl
import uuid

# Read and parse sample file
adapter = TelegramJsonAdapter()
messages = adapter.parse('sample_data/sample_result.json')

print(f"Parsed {len(messages)} messages")
for i, msg in enumerate(messages):
    print(f"  {i+1}. {msg.date} - {msg.from_user}: {msg.text}")

# Segment the messages
conversations = segment_messages(messages, threshold_factor=1.0)

print(f"\nSegmented into {len(conversations)} conversations:")
for i, conv in enumerate(conversations):
    print(f"  Conversation {i+1}:")
    print(f"    Start: {conv.start_time}")
    print(f"    End: {conv.end_time}")
    print(f"    Messages: {conv.message_count}")
    print(f"    Participants: {conv.participants}")
    
    # Print first few lines of content
    lines = conv.raw_content.split('\n')
    for line in lines[:3]:  # Show first 3 lines
        print(f"      {line}")
    if len(lines) > 3:
        print("      ...")