import os
import sys
from content_splitter import split_content

def set_env_vars():
    """Set environment variables for development testing"""
    # Process knowledge file
    knowledge_chunks = split_content("rag_knowledge_24feb2025.txt")
    
    # Process instructions file
    instruction_chunks = split_content("prompt_instructions.txt")
    
    # Set all environment variables
    chunks_list = knowledge_chunks + instruction_chunks
    for var_name, content in chunks_list:
        os.environ[var_name] = content
        print(f"✓ Set {var_name}")

if __name__ == "__main__":
    print("\nSetting environment variables for development...\n")
    set_env_vars()
    print("\nDone! You can now test the application with environment variables.\n")
    print("To switch back to the main branch:")
    print("1. git checkout main")
    print("2. git stash (if you have uncommitted changes)\n")
