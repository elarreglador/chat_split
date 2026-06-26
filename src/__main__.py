"""CLI entry point for chat_split"""

import argparse
import uuid
from typing import List
from src.models import Message, Conversation
from src.adapters.telegram_json import TelegramJsonAdapter
from src.adapters.chat_export import ChatExportAdapter
from src.ingestor import read_previous_state, filter_new_messages, get_last_end_time
from src.segmenter import segment_messages
from src.persist import append_jsonl

def main():
    parser = argparse.ArgumentParser(description='Split Telegram log into conversations')
    parser.add_argument('--input', required=True, help='Input Telegram log file')
    parser.add_argument('--output', default='conversaciones.jsonl', help='Output JSONL file')
    parser.add_argument('--factor', type=float, default=1.0, help='Threshold factor (default: 1.0)')
    parser.add_argument('--min-messages', type=int, default=3, help='Minimum messages per conversation')
    parser.add_argument('--adapter', choices=['telegram', 'chat_export'], 
                       default='telegram', help='Input format adapter (default: telegram)')
    
    args = parser.parse_args()
    
    # Read previous state
    previous_conversations = read_previous_state(args.output)
    last_end_time = get_last_end_time(previous_conversations)
    
    # Parse input file using appropriate adapter
    if args.adapter == 'telegram':
        adapter = TelegramJsonAdapter()
    else:  # chat_export
        adapter = ChatExportAdapter()
        
    all_messages = adapter.parse(args.input)
    
    # Filter new messages that are newer than last end_time
    new_messages = filter_new_messages(all_messages, last_end_time)
    
    # If there are no new messages, exit early
    if not new_messages:
        print("No new messages to process")
        return
    
    # Segment messages into conversations
    conversations = segment_messages(
        new_messages, 
        threshold_factor=args.factor,
        min_messages=args.min_messages
    )
    
    # Add UUIDs to conversations and write to file
    for conv in conversations:
        conv.conversation_id = str(uuid.uuid4())
    
    # Append new conversations to output file
    append_jsonl(args.output, conversations)
    
    print(f"Processed {len(new_messages)} messages into {len(conversations)} conversations")
    print(f"Output written to {args.output}")

if __name__ == "__main__":
    main()