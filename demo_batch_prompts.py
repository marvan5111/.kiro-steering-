import json
import sys
import os
import time

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from reasoning.engine import ReasoningEngine

def main():
    engine = ReasoningEngine()
    start_time = time.time()
    results = engine.process_batch_prompts('prompts.json')
    end_time = time.time()
    total_time = end_time - start_time
    success_count = sum(1 for r in results if r['response'])
    print("Batch Prompts Processing Results:")
    print(f"Total prompts: {len(results)}")
    print(f"Successful: {success_count}")
    print(f"Failed: {len(results) - success_count}")
    print(f"Total time: {total_time:.2f} seconds")
    print(f"Average time per prompt: {total_time / len(results):.2f} seconds")
    for result in results:
        status = "Success" if result['response'] else "Failed"
        print(f"Prompt {result['prompt_index']}: {status} - Response length: {len(result['response']['outputText']) if result['response'] else 0}")

if __name__ == "__main__":
    main()
