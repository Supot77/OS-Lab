Laboratory 6: Virtual Memory, Page Replacement, and Thrashing

Attribute
Specification
Duration
120 Minutes
Platform
GitHub Codespaces (Ubuntu Linux)
Language
Python
1. Lab Objectives
By the end of this laboratory session, students will be able to:
Understand the concept of Virtual Memory and Swapping (moving pages between RAM and Disk).
Implement and compare OS Page Replacement algorithms: FIFO (First-In, First-Out) and LRU (Least Recently Used).
Identify the performance degradation caused by Thrashing.
Explain how AI Engineers handle Out-Of-Memory (OOM) scenarios to avoid OS swapping.
2. Phase 1: Theory Recap & Workspace Setup (20 Minutes)
In Lab 5, we learned that the OS loads parts of an AI model into Physical RAM Frames. But what if your AI model requires 32GB of RAM, and your system only has 16GB? The OS uses Virtual Memory. When the RAM is completely full, the OS must evict (swap out) an existing page to the Hard Drive to make room for the new one. The algorithm the OS uses to choose the "victim" page is called a Page Replacement Algorithm. Choosing the wrong page causes too many Page Faults, severely slowing down the system.
Step 1.1: Create Your Workspace
Open your GitHub Codespaces environment.

Open the terminal and create a new directory for this week's lab:

`
mkdir lab06
cd lab06
3. Phase 2: Page Replacement Algorithms (40 Minutes)
`

We will write a simulator for the OS Memory Management Unit (MMU) to compare two classic algorithms:
FIFO (First-In, First-Out): Evicts the page that was loaded into RAM the earliest. Simple, but blind to actual usage.
LRU (Least Recently Used): Evicts the page that has not been accessed for the longest time. Requires the OS to track usage history.
Step 2.1: Write the Simulator Script
Create a file named page_replacement.py:

`
# page_replacement.py

def simulate_fifo(reference_string, num_frames):
    frames = []
    page_faults = 0
    
    print(f"\n--- Running FIFO Algorithm (Frames: {num_frames}) ---")
    for page in reference_string:
        if page not in frames:
            page_faults += 1
            if len(frames) >= num_frames:
                # FIFO: Remove the first element (oldest)
                victim = frames.pop(0) 
                print(f"Page Fault! Evicted Page {victim}. Loaded Page {page}")
            else:
                print(f"Page Fault! Loaded Page {page} (Empty Frame)")
            frames.append(page)
        else:
            print(f"Page Hit! Page {page} is already in RAM.")
            
    print(f">> Total FIFO Page Faults: {page_faults}")
    return page_faults

def simulate_lru(reference_string, num_frames):
    frames = []
    page_faults = 0
    
    print(f"\n--- Running LRU Algorithm (Frames: {num_frames}) ---")
    for page in reference_string:
        if page not in frames:
            page_faults += 1
            if len(frames) >= num_frames:
                # LRU: Remove the first element (least recently used)
                victim = frames.pop(0)
                print(f"Page Fault! Evicted Page {victim}. Loaded Page {page}")
            else:
                print(f"Page Fault! Loaded Page {page} (Empty Frame)")
            frames.append(page)
        else:
            print(f"Page Hit! Page {page} is already in RAM.")
            # LRU Update: Move the accessed page to the end of the list (most recently used)
            frames.remove(page)
            frames.append(page)
            
    print(f">> Total LRU Page Faults: {page_faults}")
    return page_faults

def main():
    # Reference string exhibiting temporal locality (William Stallings, Fig 8.14)
    # Expected page faults with 3 frames: FIFO = 9 faults, LRU = 7 faults
    ai_memory_requests = [2, 3, 2, 1, 5, 2, 4, 5, 3, 2, 5, 2]
    total_physical_frames = 3
    
    simulate_fifo(ai_memory_requests, total_physical_frames)
    simulate_lru(ai_memory_requests, total_physical_frames)

if __name__ == "__main__":
    main()
Step 2.2: Execute and Observe
`

Run the script:

`
python page_replacement.py
Observation: Compare the total Page Faults. You should notice that LRU performs better (fewer faults) because it adapts to the AI's memory access pattern, whereas FIFO blindly kicks out pages even if the AI is about to need them again in the very next step.
`

4. Phase 3: AI Industry Connection - Thrashing and CPU Offloading (30 Minutes)
When an OS spends more time swapping pages between RAM and Disk than actually executing code, the system is Thrashing.
In the AI industry, if you set your PyTorch batch_size too high, your model will exceed the physical RAM (or VRAM). If you rely on the OS to automatically swap data to the SSD, your training speed will drop from hours to years. Instead of relying on OS swapping, AI engineers use explicit memory management techniques like Gradient Checkpointing or CPU Offloading (e.g., DeepSpeed Zero).
Let's simulate the catastrophic performance drop caused by Thrashing.
Step 3.1: Write the Thrashing Simulation Script
Create a file named ai_thrashing.py:

`
# ai_thrashing.py
import time
import os

def fast_ram_access(iterations):
    """Simulates AI training when everything fits in Physical RAM"""
    simulated_ram = [0.0] * 1000
    start_time = time.time()
    
    for _ in range(iterations):
        for i in range(len(simulated_ram)):
            simulated_ram[i] += 1.5 # Fast Memory CPU operation
            
    return time.time() - start_time

def slow_swap_thrashing_access(iterations, filename="swap_file.bin"):
    """Simulates Thrashing: OS is constantly reading/writing to the Disk Swap file"""
    # Create a dummy swap file
    with open(filename, "wb") as f:
        f.write(b'\x00' * 1000)
        
    start_time = time.time()
    
    for _ in range(iterations):
        # Thrashing: Constant Disk I/O because RAM is full
        with open(filename, "r+b") as f:
            data = bytearray(f.read())
            for i in range(len(data)):
                data[i] = (data[i] + 1) % 255
            f.seek(0)
            f.write(data)
            
    os.remove(filename) # Cleanup
    return time.time() - start_time

def main():
    print("--- Simulating AI Training Batch (10,000 Iterations) ---")
    iterations = 10000
    
    print("\n1. Scenario: Batch fits in RAM (No Page Faults)")
    ram_time = fast_ram_access(iterations)
    print(f"   -> Processing Time: {ram_time:.4f} seconds")
    
    print("\n2. Scenario: Out of Memory - OS is Thrashing (Swapping to Disk)")
    swap_time = slow_swap_thrashing_access(iterations)
    print(f"   -> Processing Time: {swap_time:.4f} seconds")
    
    performance_drop = swap_time / ram_time
    print(f"\n>>> SYSTEM IMPACT: Thrashing made the system {performance_drop:.0f} TIMES slower!")

if __name__ == "__main__":
    main()
Step 3.2: Execute and Analyze
`

Run the script:

`
python ai_thrashing.py
The results perfectly illustrate why AI Engineers fear Out-Of-Memory (OOM) errors. The OS swap mechanism is designed to prevent crashes, but Disk I/O is astronomically slower than physical RAM. If your system thrashes, your model effectively stops training.
`

5. Phase 4: Analysis & Conclusion (30 Minutes)
Save your work to GitHub before proceeding:

`
git add .
git commit -m "Completed Lab 6 coding"
git push
Lab Report Assignment
`

Create a file named Lab06_Report.txt, copy the template below, answer the questions, and push it to your repository.

`
======================================================
COE67-222 Operating Systems - Lab 06 Report
Name: 
Student ID: 
======================================================

1. FIFO vs LRU (Phase 2):
In the `page_replacement.py` script, why did the LRU algorithm perform better (have fewer page faults) than the FIFO algorithm for the given reference string? Explain how LRU decides which page to evict.

2. Understanding Thrashing (Phase 3):
Based on your observation of `ai_thrashing.py`, define "Thrashing" in your own words. Why is the processing time significantly higher in Scenario 2?

3. AI Engineering Decision:
If you are training an AI model and your system begins to thrash because the RAM is full, lowering the `batch_size` in your Python code is a common solution. How does lowering the `batch_size` help the Operating System resolve the Thrashing problem?

`
