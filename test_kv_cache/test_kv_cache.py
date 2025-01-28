# kv_cache_smollm.py
import ollama
import json
from typing import Dict, Any
from pathlib import Path

class SmolLMCache:
    def __init__(self):
        # Check if Ollama is running and smollm is available
        try:
            self.ollama = ollama.Client()
            # Quick test to see if model is available
            self.ollama.embeddings(model='smollm:135m', prompt='test')
        except Exception as e:
            print(f"Error initializing: {e}")
            print("Make sure to run: ollama run smollm:135m")
            raise

        self.cache: Dict[str, Any] = {}
        self.cache_file = Path('kv_cache.json')
        self.load_cache()  # Load existing cache if available

    def generate_with_cache(self, prompt: str) -> str:
        cache_key = prompt

        if cache_key in self.cache:
            print("Using cached KV")
            response = self.ollama.generate(
                model='smollm:135m',
                prompt=prompt,
                context=self.cache[cache_key]
            )
            return response['response']
            
        print("No cache hit - computing new")
        response = self.ollama.generate(
            model='smollm:135m', 
            prompt=prompt,
            options={
                'num_ctx': 2048,
                'temperature': 0.7
            }
        )
        
        self.cache[cache_key] = response['context']
        self.save_cache()  # Auto-save after new entries
        return response['response']

    def save_cache(self):
        """Save cache to disk"""
        with open(self.cache_file, 'w') as f:
            json.dump(self.cache, f)
            
    def load_cache(self):
        """Load cache from disk"""
        if self.cache_file.exists():
            with open(self.cache_file, 'r') as f:
                self.cache = json.load(f)
        else:
            self.cache = {}

def main():
    # Make sure ollama is running first with:
    # ollama run smollm:135m
    
    try:
        model = SmolLMCache()
    except Exception as e:
        print(f"Failed to initialize: {e}")
        return

    # Print the kv cache
    print("KV Cache:", model.cache)

    # Test prompts
    prompts = [
        "What is deep learning?",
        "What is deep learning?",  # Should use cache
        "What is machine learning?",  # New computation
    ]

    for i, prompt in enumerate(prompts, 1):
        print(f"\n--- Run {i} ---")
        print(f"Prompt: {prompt}")
        try:
            response = model.generate_with_cache(prompt)
            print(f"Response: {response}")
        except Exception as e:
            print(f"Error generating response: {e}")

if __name__ == "__main__":
    main()
