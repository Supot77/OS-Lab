Laboratory 5: Memory Management - Paging and Address Translation

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
Differentiate between Logical Addresses (what the program sees) and Physical Addresses (where data actually lives in RAM).
Explain how the OS uses "Paging" to store large Machine Learning models in fragmented physical memory.
Write a Python simulation of an OS Page Table to perform Address Translation.
Utilize OS-level Memory-Mapped Files (mmap) to handle AI models that exceed available physical RAM.
2. Phase 1: Theory Recap & Workspace Setup (20 Minutes)
When you load a massive Artificial Intelligence model (like a Large Language Model) into Python, your code sees the model as one giant, continuous array of numbers (Logical Memory). However, the physical OS RAM is often fragmented. The OS solves this by chopping the AI model into small chunks called Pages, and storing them in available RAM slots called Frames. The OS keeps a map called a Page Table to translate between the two.
Step 1.1: Create Your Workspace
Open your GitHub Codespaces environment.
Open the terminal and create a new directory for this week's lab:
Run the following commands in your terminal:

`
mkdir lab05
cd lab05

pip install psutil

`

3. Phase 2: The OS View of Memory Allocation (30 Minutes)
Let's see how the OS handles allocating a large block of memory for an AI model's weight matrix.
Step 2.1: Write the Memory Allocation Script
Create a file named memory_allocation.py:
Add the following code to memory_allocation.py:

`
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

Step 2.2: Execute and Observe
`

Run the script:

`
python memory_allocation.py
Observation: Notice the massive jump in RAM usage. Even though you created one single list in Python (Logical memory), the underlying Linux OS had to allocate thousands of physical memory pages to store these 10 million numbers.
`

4. Phase 3: OS-Aware Optimization - Page Table Simulation (30 Minutes)
Because Python hides the physical memory addresses from us, we will build a System Simulator. We will write the algorithm that the OS Memory Management Unit (MMU) uses to translate a Logical Address (e.g., Neuron Index 5050) into a Physical RAM Address.
The Math of Paging:
Page Number = Logical Address // Page Size
Offset = Logical Address % Page Size
Physical Address = (Frame Number * Page Size) + Offset
Step 3.1: Write the Address Translation Simulator
Create a file named page_table_sim.py:
Add the following code to page_table_sim.py:

`
# page_table_sim.py

# System Constants
PAGE_SIZE = 1000  # In a real OS, this is usually 4096 Bytes (4KB)

# The OS Page Table: Maps [Page Number] -> [Physical Frame Number]
# Because RAM is fragmented, frames are not strictly in order!
os_page_table = {
    0: 12,  # Page 0 is stored in Frame 12
    1: 45,  # Page 1 is stored in Frame 45
    2: 8,   # Page 2 is stored in Frame 8
    3: 102, # Page 3 is stored in Frame 102
    4: 15,  # Page 4 is stored in Frame 15
    5: 33   # Page 5 is stored in Frame 33
}

def translate_address(logical_address):
    """Simulates the OS Memory Management Unit (MMU)"""
    print(f"\n[MMU] Requesting Logical Address: {logical_address}")

    # 1. Calculate Page Number and Offset
    page_number = logical_address // PAGE_SIZE
    offset = logical_address % PAGE_SIZE

    print(f"      -> Computed Page Number: {page_number}")
    print(f"      -> Computed Offset: {offset}")

    # 2. Page Table Lookup
    if page_number not in os_page_table:
        print("      -> [OS ERROR] Page Fault! Data not in RAM (Segmentation Fault).")
        return None

    frame_number = os_page_table[page_number]
    print(f"      -> Page Table Lookup: Found in Frame {frame_number}")

    # 3. Compute Final Physical Address
    physical_address = (frame_number * PAGE_SIZE) + offset
    print(f"      -> [SUCCESS] Translated Physical Address: {physical_address}")
    return physical_address

def main():
    print("--- AI Model Address Translation Simulator ---")

    # Scenario A: Fetching the weight of Neuron at index 250
    translate_address(250)

    # Scenario B: Fetching the weight of Neuron at index 3450
    translate_address(3450)

    # Scenario C: Trying to access an index out of bounds
    translate_address(9999)

if __name__ == "__main__":
    main()

Step 3.2: Execute and Observe
`

Run the simulation script:

`
python page_table_sim.py
Carefully trace the math for Scenario B (Logical Address 3450). See how the OS chops the number by the PAGE_SIZE to find where the data actually lives in the fragmented physical hardware.
`

5. Phase 4: AI Industry Connection - Loading Massive LLMs (20 Minutes)
In modern AI engineering, Large Language Models (LLMs) like LLaMA often weigh over 50GB. What if your server only has 16GB of physical RAM?
AI Engineers use an OS feature called Memory-Mapped Files (mmap). Instead of loading the entire 50GB file into RAM (which would crash the system), mmap tricks the Python program into thinking the file is in RAM by creating entries in the Page Table that point to the hard drive.
When your AI code requests a specific weight, the OS triggers a Page Fault, pauses the program, loads only that 4KB page from the disk into a physical RAM frame, and resumes.
Step 4.1: Simulate Memory Mapping
Create a file named ai_mmap_model.py:
Add the following code to ai_mmap_model.py:

`
# ai_mmap_model.py
import mmap
import os
import psutil

def print_memory():
    process = psutil.Process(os.getpid())
    print(f"[OS Monitor] Physical RAM Usage: {process.memory_info().rss / (1024*1024):.2f} MB")

def main():
    file_path = "fake_llm_weights.bin"

    # 1. Create a fake 50MB model weight file on the hard drive
    print("Creating a 50MB fake LLM file on Disk...")
    with open(file_path, "wb") as f:
        f.write(b'\x00' * (50 * 1024 * 1024))

    print_memory()

    # 2. Use OS mmap to map the file to Virtual Memory (Page Table)
    print("\nMapping the 50MB file into Virtual Memory...")
    with open(file_path, "r+b") as f:
        # We map it, but the OS doesn't load it into physical RAM yet!
        mm = mmap.mmap(f.fileno(), 0)
        print_memory()

        # 3. Triggering a Page Fault
        print("\nAccessing weight at index 25,000,000 (Triggers OS Page Fault)...")

        weight = mm[25000000]
        print(f"Weight value accessed successfully: {weight}")

        mm.close()

    os.remove(file_path) # Cleanup

if __name__ == "__main__":
    main()

Step 4.2: Execute and Analyze
`

Run the script:

`
python ai_mmap_model.py
Notice that the Physical RAM Usage barely changes, even though we mapped a 50MB file! The OS elegantly managed the memory via the Page Table, fetching only the exact byte we requested. This OS-level trick is the backbone of libraries like HuggingFace Safetensors.
`

6. Phase 5: Analysis & Conclusion (20 Minutes)
Save your work to GitHub before proceeding:
Run the following git commands to submit your progress:

`
git add .
git commit -m "Completed Lab 5 coding"
git push
Lab Report Assignment
`

Create a file named Lab05_Report.txt, copy the template below, answer the questions, and push it to your repository.
Use the following template for your report:

`
======================================================
COE67-222 Operating Systems - Lab 05 Report
Name: 
Student ID: 
======================================================
1. Address Translation Math (Phase 3):
Assume an OS has a PAGE_SIZE of 4096 bytes. 
If an AI model requests data at Logical Address 10000, calculate:
- The Page Number: [____]
- The Offset: [____]
(Show your calculation steps briefly).

2. Physical Memory Fragmentation:
In our `page_table_sim.py`, Page 0 was stored in Frame 12, and Page 1 was in Frame 45. 

Why does the OS store continuous logical data in scattered/fragmented physical frames instead of putting them right next to each other? What problem does this solve?

3. The AI Context (mmap):
In Phase 4, we mapped a 50MB file to memory, but the physical RAM usage did not increase significantly. Explain how the OS Virtual Memory and Page Table achieve this, and what actually happens at the OS level when index 25,000,000 is accessed.

`
