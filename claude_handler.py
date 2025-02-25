import os
import json
import anthropic
from logger import setup_logger

logger = setup_logger()

def create_claude_assistant():
    """Create and configure Claude assistant"""
    config_path = "claude_assistant_config.json"
    try:
        if not os.path.exists(config_path):
            # Read the full knowledge document
            with open("rag_knowledge_24feb2025.txt", "r", encoding="utf-8") as f:
                knowledge_content = f.read()

            assistant_config = {
                "knowledgeContent": knowledge_content,
                "instructions": (
                    "Provide clear, concise, and professional responses inspired by Joanna Stern's tone and style.\n"
                    # Rest of instructions...
                ),
                # Use latest model as per blueprint
                "model": "claude-3-5-sonnet-20241022"
            }
            with open(config_path, "w", encoding="utf-8") as f:
                json.dump(assistant_config, f, indent=2)
        else:
            with open(config_path, "r", encoding="utf-8") as f:
                assistant_config = json.load(f)
        return assistant_config
    except Exception as e:
        logger.error(f"Error creating Claude assistant: {e}")
        raise

def query_claude(question, assistant_config):
    """Query Claude with a question"""
    try:
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable is not set")

        client = anthropic.Anthropic(api_key=api_key)

        # Create message with system prompt in the correct format
        message = client.messages.create(
            model=assistant_config["model"],
            max_tokens=300,
            system=f"Below is a knowledge document with information about Howard. Use this document to answer the user's question:\n\n{assistant_config['knowledgeContent']}\n\n{assistant_config['instructions']}",
            messages=[
                {
                    "role": "user",
                    "content": question
                }
            ]
        )
        return message.content[0].text

    except Exception as e:
        logger.error(f"Error querying Claude: {e}")
        raise