"""Test segmenter module"""

import pytest
from datetime import datetime
from src.models import Message
from src.segmenter import calculate_time_gaps, calculate_segmentation_threshold, segment_messages

def test_calculate_time_gaps():
    """Test time gap calculation"""
    # Create sample messages with known timestamps
    msg1 = Message(1, "2023-01-01T10:00:00Z", "User1", "Message 1")
    msg2 = Message(2, "2023-01-01T10:05:00Z", "User2", "Message 2")  
    msg3 = Message(3, "2023-01-01T10:10:00Z", "User1", "Message 3")
    
    messages = [msg1, msg2, msg3]
    gaps = calculate_time_gaps(messages)
    
    assert len(gaps) == 2
    assert gaps[0] == 300.0  # 5 minutes in seconds
    assert gaps[1] == 300.0

def test_calculate_segmentation_threshold():
    """Test threshold calculation"""
    gaps = [300.0, 600.0, 300.0, 900.0, 300.0]  # 5 messages with various gaps
    
    # Test with factor = 1.0
    threshold = calculate_segmentation_threshold(gaps, factor=1.0)
    
    # Should be median + std_dev (median = 300, std_dev ≈ 244.95)
    assert threshold > 300.0
    
    # Test with empty gaps
    empty_threshold = calculate_segmentation_threshold([], factor=1.0)
    assert empty_threshold == 1800.0  # fallback to 30 minutes

def test_segment_messages_single():
    """Test segmenting messages into single conversation"""
    msg1 = Message(1, "2023-01-01T10:00:00Z", "User1", "Message 1")
    msg2 = Message(2, "2023-01-01T10:05:00Z", "User2", "Message 2")  
    
    messages = [msg1, msg2]
    conversations = segment_messages(messages, threshold_factor=1.0)
    
    assert len(conversations) == 1
    assert conversations[0].message_count == 2



if __name__ == "__main__":
    pytest.main([__file__])