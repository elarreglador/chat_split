"""Test models for msg_split"""

import pytest
from src.models import Message, Conversation

def test_message_creation():
    """Test Message dataclass creation"""
    msg = Message(
        id=1,
        date="2023-01-01T10:00:00Z",
        from_user="John Doe",
        text="Hello world"
    )
    
    assert msg.id == 1
    assert msg.date == "2023-01-01T10:00:00Z"
    assert msg.from_user == "John Doe"
    assert msg.text == "Hello world"

def test_conversation_creation():
    """Test Conversation dataclass creation"""
    conv = Conversation(
        conversation_id="test-id",
        participants=["John Doe", "Jane Smith"],
        start_time="2023-01-01T10:00:00Z",
        end_time="2023-01-01T10:05:00Z",
        message_count=5,
        raw_content="Message 1\nMessage 2"
    )
    
    assert conv.conversation_id == "test-id"
    assert conv.participants == ["John Doe", "Jane Smith"]
    assert conv.message_count == 5
    assert conv.raw_content == "Message 1\nMessage 2"

if __name__ == "__main__":
    pytest.main([__file__])