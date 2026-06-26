# msg_split - Telegram Conversation Log Splitter

## Overview
This application splits Telegram conversation logs into individual conversations based on time gaps between messages. It implements a dynamic segmentation algorithm using median and standard deviation of time intervals.

## Features
1. **Idempotent Processing**: Reads previous state to avoid reprocessing
2. **Dynamic Threshold Calculation**: Uses median + factor × std deviation to set conversation boundaries  
3. **JSONL Output**: Each conversation is written as a separate JSON line
4. **CLI Interface**: Simple command-line tool for processing logs

## Architecture
- `models.py`: Data structures (Message, Conversation)
- `adapters/telegram_json.py`: Parses Telegram Desktop's result.json
- `ingestor.py`: Manages state and filters new messages
- `segmenter.py`: Core algorithm for time-based conversation splitting
- `persist.py`: Read/write JSONL operations
- `__main__.py`: CLI entry point

## Usage
```
python -m msg_split --input <telegram_log.json> [--output conversaciones.jsonl] [--factor 1.0] [--min-messages 3]
```

## Sample Output (JSONL format)
```json
{"conversation_id":"a1b2c3d4-e5f6-7890-abcd-ef1234567890","participants":["User1"],"start_time":"2023-01-01T10:00:00Z","end_time":"2023-01-01T10:05:00Z","message_count":3,"raw_content":"User1: Hello everyone!\nUser2: Hi User1!\nUser1: How are you?","summary":null}
{"conversation_id":"b2c3d4e5-f6a7-8901-bcde-f12345678901","participants":["User3"],"start_time":"2023-01-01T11:30:00Z","end_time":"2023-01-01T11:35:00Z","message_count":2,"raw_content":"User3: Hey there!\nUser4: What's up?","summary":null}
```

## Algorithm Details
- Time gaps between consecutive messages are calculated in seconds
- Threshold = median_gap + (threshold_factor × standard_deviation)
- If gap > threshold, a new conversation begins
- If gap ≤ threshold, message is added to current conversation

The application handles edge cases like:
- Empty inputs
- Single message conversations 
- Very short conversations