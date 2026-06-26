"""Test ingestor module"""

import pytest
from src.models import Message
from src.ingestor import filter_new_messages

def test_filter_new_messages():
    """Test filtering of new messages based on timestamp"""
    # Create sample messages with timestamps
    msg1 = Message(1, "2023-01-01T10:00:00Z", "User1", "Message 1")
    msg2 = Message(2, "2023-01-01T10:05:00Z", "User2", "Message 2")  
    msg3 = Message(3, "2023-01-01T10:10:00Z", "User1", "Message 3")
    
    messages = [msg1, msg2, msg3]
    
    # Filter with a timestamp that would exclude first message
    filtered = filter_new_messages(messages, "2023-01-01T10:02:00Z")
    
    assert len(filtered) == 2
    assert filtered[0].date == "2023-01-01T10:05:00Z"
    assert filtered[1].date == "2023-01-01T10:10:00Z"

if __name__ == "__main__":
    pytest.main([__file__])