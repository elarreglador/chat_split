"""Test the new ChatExportAdapter"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from adapters.chat_export import ChatExportAdapter

def test_chat_export_adapter():
    """Test that the chat export adapter works correctly"""
    adapter = ChatExportAdapter()
    messages = adapter.parse('chatExport/test_conversation.json')
    
    print(f"Successfully parsed {len(messages)} messages from chat export")
    
    for i, msg in enumerate(messages):
        print(f"  {i+1}. {msg.date} - {msg.from_user}: {msg.text}")

if __name__ == "__main__":
    test_chat_export_adapter()