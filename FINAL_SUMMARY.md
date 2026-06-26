# msg_split - Final Enhanced Delivery Summary

## What Was Implemented

I have successfully built a Telegram conversation log splitter application that:
1. Reads Telegram JSON exports and new chat export formats
2. Calculates time intervals between consecutive messages 
3. Dynamically determines conversation boundaries using median + std deviation
4. Outputs structured JSONL format with one conversation per line
5. Implements idempotent processing to avoid reprocessing
6. Provides a clean CLI interface

## Key Features

### Core Algorithm
- **Time Gap Calculation**: Measures seconds between consecutive messages
- **Dynamic Threshold**: Uses `median + (factor × standard_deviation)` 
- **Smart Segmentation**: Starts new conversations when gaps exceed threshold
- **State Management**: Reads previous output to avoid reprocessing

### Architecture
```
src/
├── __main__.py          # CLI interface
├── models.py            # Data structures
├── ingestor.py          # State management
├── segmenter.py         # Core algorithm
├── persist.py           # JSONL operations
└── adapters/
    ├── __init__.py      # Adapter exports
    ├── base.py          # Abstract adapter base class  
    ├── telegram_json.py # Telegram export parser
    └── chat_export.py   # Chat export parser
```

## Supported Input Formats

The msg_split tool now supports multiple input formats through different adapters:

### 1. Telegram JSON Format (Default)
Standard Telegram Desktop exports in `result.json` format.

```bash
python -m msg_split --input telegram_export.json --adapter telegram
```

### 2. Chat Export Format 
New format with conversation data in `ChatExport_YYYY-MM-DD` directory structure.

```bash
python -m msg_split --input ChatExport_2026-06-26/conversation.json --adapter chat_export
```

## Usage Examples

Basic usage:
```bash
python -m msg_split --input telegram_export.json
```

Advanced usage:
```bash
python -m msg_split --input telegram_export.json \
                    --output conversations.jsonl \
                    --factor 1.5 \
                    --min-messages 5 \
                    --adapter chat_export
```

## Testing Status
✅ All unit tests passing
✅ Sample data demonstrates correct functionality  
✅ Edge cases properly handled
✅ Idempotent processing confirmed working
✅ New chat export adapter verified with test data

The implementation fulfills all requirements from the original specification and has been reviewed for code quality and correctness.