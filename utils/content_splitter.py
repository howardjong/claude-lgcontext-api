import os
import math

def split_content(file_path, chunk_size=3500):
    """Split file content into chunks for environment variables"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        total_length = len(content)
        num_chunks = math.ceil(total_length / chunk_size)
        
        print(f"\nFile: {file_path}")
        print(f"Total characters: {total_length}")
        print(f"Will be split into {num_chunks} chunks\n")
        
        chunks = []
        for i in range(num_chunks):
            start = i * chunk_size
            end = start + chunk_size
            chunk = content[start:end]
            var_name = f"RAG_KNOWLEDGE_CONTENT_{i+1}" if "rag_knowledge" in file_path else "PROMPT_INSTRUCTIONS"
            chunks.append((var_name, chunk))
            print(f"Chunk {i+1}: {len(chunk)} characters")
            
        return chunks
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return []
    except Exception as e:
        print(f"Error processing file: {e}")
        return []

if __name__ == "__main__":
    # Process knowledge file
    knowledge_chunks = split_content("rag_knowledge_24feb2025.txt")
    
    # Process instructions file (single chunk)
    instruction_chunks = split_content("prompt_instructions.txt")
    
    print("\nCopy these environment variable commands:\n")
    for var_name, content in knowledge_chunks + instruction_chunks:
        print(f"# Set {var_name}")
        print(f"export {var_name}='{content}'\n")
