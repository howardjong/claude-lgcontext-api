
import os
from claude_handler import create_claude_assistant, query_claude

def test_claude_response():
    # Force rebuild of config to use latest knowledge file
    if os.path.exists("claude_assistant_config.json"):
        os.remove("claude_assistant_config.json")
    claude_config = create_claude_assistant()
    
    # Test question
    test_question = "What can you tell me about Howard's technical expertise?"
    
    # Query Claude
    response = query_claude(test_question, claude_config)
    print("\nTest Question:", test_question)
    print("\nClaude Response:", response)

if __name__ == "__main__":
    test_claude_response()
