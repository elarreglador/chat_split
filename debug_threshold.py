"""Debug segmenter threshold calculation"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.models import Message
from src.segmenter import calculate_time_gaps, calculate_segmentation_threshold

# Create test messages with a large gap between them
msg1 = Message(1, "2023-01-01T10:00:00Z", "User1", "Message 1")
msg2 = Message(2, "2023-01-01T10:05:00Z", "User2", "Message 2")
msg3 = Message(3, "2023-01-01T11:00:00Z", "User1", "Message 3")  # Large gap

messages = [msg1, msg2, msg3]

print("Messages:")
for msg in messages:
    print(f"  {msg.date} - {msg.from_user}: {msg.text}")

gaps = calculate_time_gaps(messages)
print(f"\nGaps (in seconds): {gaps}")
print(f"Number of gaps: {len(gaps)}")

threshold = calculate_segmentation_threshold(gaps, factor=10.0)
print(f"Threshold with factor 10.0: {threshold}")

# Show the calculation
import statistics
median = statistics.median(gaps)
if len(gaps) > 1:
    std_dev = statistics.stdev(gaps) if len(gaps) > 1 else 0.0
    print(f"Median: {median}")
    print(f"Std Dev: {std_dev}")
    expected_threshold = median + (10.0 * std_dev)
    print(f"Expected threshold calculation: {median} + (10.0 × {std_dev}) = {expected_threshold}")
else:
    print(f"Single gap, using median directly: {median}")

# Check if any gaps exceed threshold
for i, gap in enumerate(gaps):
    print(f"Gap between msg {i+1} and {i+2}: {gap}s")
    print(f"  Exceeds threshold? {gap > threshold}")