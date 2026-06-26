"""Segmentation module for msg_split"""

import statistics
from typing import List
from datetime import datetime, timedelta
from src.models import Message, Conversation

def calculate_time_gaps(messages: List[Message]) -> List[float]:
    """Calculate time gaps (in seconds) between consecutive messages"""
    gaps = []
    
    if len(messages) < 2:
        return gaps
    
    for i in range(1, len(messages)):
        prev_msg = messages[i-1]
        curr_msg = messages[i]
        
        # Convert dates to datetime objects
        prev_dt = datetime.fromisoformat(prev_msg.date.replace('Z', '+00:00'))
        curr_dt = datetime.fromisoformat(curr_msg.date.replace('Z', '+00:00'))
        
        gap_seconds = (curr_dt - prev_dt).total_seconds()
        gaps.append(gap_seconds)
    
    return gaps

def calculate_segmentation_threshold(gaps: List[float], factor: float = 1.0) -> float:
    """Calculate threshold for segmentation using median + factor * std_dev"""
    if not gaps:
        # Return a default value if no gaps
        return 30 * 60  # 30 minutes fallback
    
    # Calculate median and standard deviation
    median = statistics.median(gaps)
    
    # Only calculate std if we have enough data points
    if len(gaps) > 1:
        std_dev = statistics.stdev(gaps) if len(gaps) > 1 else 0.0
        threshold = median + (factor * std_dev)
    else:
        threshold = median
    
    return threshold

def segment_messages(messages: List[Message], 
                     threshold_factor: float = 1.0,
                     min_messages: int = 3) -> List[Conversation]:
    """Segment messages into conversations based on calculated thresholds"""
    if not messages:
        return []
    
    # For very small datasets, group all messages into one conversation
    if len(messages) < min_messages:
        conv_text = '\n'.join([f"{msg.from_user}: {msg.text}" for msg in messages])
        conversation = Conversation(
            conversation_id="",
            participants=[messages[0].from_user] if messages else [],
            start_time=messages[0].date,
            end_time=messages[-1].date,
            message_count=len(messages),
            raw_content=conv_text
        )
        return [conversation]
    
    conversations = []
    current_conv_messages = [messages[0]]  # Start with first message
    start_time = messages[0].date
    
    # Calculate time gaps between consecutive messages
    gaps = calculate_time_gaps(messages)
    
    # Calculate threshold using median + factor * std_dev  
    threshold = calculate_segmentation_threshold(gaps, threshold_factor)
    
    for i in range(1, len(messages)):
        prev_msg = messages[i-1]
        curr_msg = messages[i]
        
        # Calculate gap between current messages
        prev_dt = datetime.fromisoformat(prev_msg.date.replace('Z', '+00:00'))
        curr_dt = datetime.fromisoformat(curr_msg.date.replace('Z', '+00:00'))
        gap_seconds = (curr_dt - prev_dt).total_seconds()
        
        # If gap exceeds threshold, start new conversation
        if gap_seconds > threshold:
            # Finalize current conversation
            conv_text = '\n'.join([f"{msg.from_user}: {msg.text}" for msg in current_conv_messages])
            
            conversation = Conversation(
                conversation_id="",
                participants=[current_conv_messages[0].from_user] if current_conv_messages else [],
                start_time=start_time,
                end_time=current_conv_messages[-1].date,
                message_count=len(current_conv_messages),
                raw_content=conv_text
            )
            conversations.append(conversation)
            
            # Start new conversation with current message
            current_conv_messages = [curr_msg]
            start_time = curr_msg.date
        else:
            # Add to current conversation
            current_conv_messages.append(curr_msg)
    
    # Don't forget the last conversation
    if current_conv_messages:
        conv_text = '\n'.join([f"{msg.from_user}: {msg.text}" for msg in current_conv_messages])
        conversation = Conversation(
            conversation_id="",
            participants=[current_conv_messages[0].from_user] if current_conv_messages else [],
            start_time=start_time,
            end_time=current_conv_messages[-1].date,
            message_count=len(current_conv_messages),
            raw_content=conv_text
        )
        conversations.append(conversation)
    
    return conversations