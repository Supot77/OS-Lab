# memory_allocation.py
import os
import psutil
import time

def print_memory_usage():
    """Fetches the actual RAM usage of this Python process from the OS"""
    process = psutil.Process(os.getpid())
    mem_mb = process.memory_info().rss / (1024 * 1024)
    print(f"[OS Monitor] Current Physical RAM Usage: {mem_mb:.2f} MB")

def main():
    print(f"--- AI Model Memory Allocation (PID: {os.getpid()}) ---")
    print_memory_usage()

    print("\nLoading a large Neural Network layer into memory...")
    # Creating a massive array of 10 million floating-point numbers
    # In Python, this requests a large continuous logical memory block from the OS
    time.sleep(2)
    ai_model_weights = [0.0] * 10_000_000

    print("Model Loaded successfully!")
    print_memory_usage()

    # Keeping the program alive so you can inspect it
    print("\nProgram is sleeping. Open another terminal and run 'htop'")
    time.sleep(30)

if __name__ == "__main__":
    main()
