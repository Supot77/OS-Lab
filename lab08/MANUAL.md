Laboratory 8: I/O Management and Disk Scheduling

Attribute
Specification
Instructor
Asst.Prof.Dr. Chirawat Wattanapanich
Duration
120 Minutes
Platform
GitHub Codespaces (Ubuntu Linux)
Language
Python
1. Lab Objectives
By the end of this laboratory session, students will be able to:
Understand the performance differences between Sequential I/O and Random I/O.
Explain how the OS schedules disk access using algorithms like FCFS and SCAN (Elevator).
Calculate the total disk head movement (Seek Time) for different scheduling algorithms.
Apply I/O Management principles to AI Data Engineering by optimizing dataset file structures.
2. Phase 1: Theory Recap & Workspace Setup (20 Minutes)
The CPU and RAM are incredibly fast (nanoseconds), but Secondary Storage (HDD/SSD) is relatively slow (milliseconds). When a process waits for the disk to read or write data, it enters the "I/O Wait" state. If the Operating System does not manage I/O efficiently, the entire system slows down.
To minimize mechanical movement (or SSD block lookups), the OS tries to sort incoming read/write requests so that the disk head moves in a single, smooth direction, rather than jumping back and forth.
Step 1.1: Create Your Workspace
Open your GitHub Codespaces environment.
Open the terminal and create a new directory for this week's lab:

`
mkdir lab08
cd lab08
3. Phase 2: Disk Scheduling Algorithms (40 Minutes)
`

Imagine a Hard Disk Drive (HDD) with tracks numbered from 0 to 199. Several processes are asking the OS to read data from different tracks: [98, 183, 37, 122, 14, 124, 65, 67]. The disk head is currently at track 53.
We will compare two OS scheduling algorithms:
FCFS (First-Come, First-Served): The OS processes requests exactly in the order they arrive.
SCAN (Elevator Algorithm): The OS moves the disk head in one direction (e.g., UP) servicing all requests in its path until it reaches the end, then reverses direction.
Step 2.1: Write the Disk Scheduler Simulator
Create a file named disk_scheduler.py:

`
# disk_scheduler.py

def simulate_fcfs(requests, initial_position):
    print("\n--- FCFS Disk Scheduling ---")
    current_pos = initial_position
    total_head_movement = 0
    path = [current_pos]
    
    for req in requests:
        movement = abs(current_pos - req)
        total_head_movement += movement
        current_pos = req
        path.append(current_pos)
        
    print(f"Path: {' -> '.join(map(str, path))}")
    print(f">> Total Head Movement (Seek Time): {total_head_movement} cylinders")

def simulate_scan(requests, initial_position, max_cylinder=199):
    print("\n--- SCAN (Elevator) Disk Scheduling ---")
    # Sort requests
    sorted_requests = sorted(requests)
    
    # Split requests into two queues based on current position
    # Assuming we are moving UP towards max_cylinder first
    left = [req for req in sorted_requests if req < initial_position]
    right = [req for req in sorted_requests if req >= initial_position]
    
    current_pos = initial_position
    total_head_movement = 0
    path = [current_pos]
    
    # Move UP
    for req in right:
        total_head_movement += abs(current_pos - req)
        current_pos = req
        path.append(current_pos)
        
    # Go to the end of the disk (OS Elevator rule)
    if current_pos != max_cylinder:
        total_head_movement += abs(current_pos - max_cylinder)
        current_pos = max_cylinder
        path.append(current_pos)
        
    # Reverse direction and move DOWN
    # Left requests must be reversed because we are moving backwards
    for req in reversed(left):
        total_head_movement += abs(current_pos - req)
        current_pos = req
        path.append(current_pos)
        
    print(f"Path: {' -> '.join(map(str, path))}")
    print(f">> Total Head Movement (Seek Time): {total_head_movement} cylinders")

def main():
    # I/O requests for disk tracks
    io_requests = [98, 183, 37, 122, 14, 124, 65, 67]
    start_pos = 53
    
    print(f"Initial Head Position: {start_pos}")
    print(f"Incoming OS I/O Requests: {io_requests}")
    
    simulate_fcfs(io_requests, start_pos)
    simulate_scan(io_requests, start_pos)

if __name__ == "__main__":
    main()
Step 2.2: Execute and Observe
`

Run the script: python disk_scheduler.py Observation: FCFS makes the disk head jump wildly (e.g., 53 -> 98 -> 183 -> 37), resulting in massive mechanical wear and high seek time. The SCAN algorithm elegantly sorts the requests, sweeping up to 199 and then down, drastically reducing the total head movement.
4. Phase 3: AI Industry Connection - I/O Bottleneck in Datasets (30 Minutes)
When training a Convolutional Neural Network (CNN) on a dataset like ImageNet, you have over 1.2 million small JPEG files. If your Python code asks the OS to open and read 1.2 million separate files, the OS suffers massive I/O Overhead. It must find the Inode, check permissions, and move the disk head randomly for every single file. The GPU will sit idle at 0% usage, waiting for the Disk (This is called being I/O Bound).
To solve this, AI Engineers pack millions of images into one massive, continuous file (like .tfrecord in TensorFlow or .h5 in HDF5). This forces the OS to perform Sequential I/O, which is significantly faster.
Step 3.1: The Dataset I/O Benchmark
Create a file named ai_dataset_io.py:

`
# ai_dataset_io.py
import os
import time

def setup_test_files(num_files, file_size_bytes):
    print("Setting up test environments... (This might take a few seconds)")
    
    # 1. Create directory with many small files
    os.makedirs("raw_images_folder", exist_ok=True)
    for i in range(num_files):
        with open(f"raw_images_folder/img_{i}.bin", "wb") as f:
            f.write(b'\x00' * file_size_bytes)
            
    # 2. Create one large continuous dataset file (TFRecord style)
    with open("packed_dataset.tfrecord", "wb") as f:
        f.write(b'\x00' * (num_files * file_size_bytes))
        
    print("Setup complete.\n")

def test_random_small_files(num_files):

    print(f"Test 1: Reading {num_files} separate small files (Raw Images)")
    start_time = time.time()
    
    for i in range(num_files):
        # High OS Overhead: Open -> Read -> Close (Repeated 5000 times)
        with open(f"raw_images_folder/img_{i}.bin", "rb") as f:
            data = f.read()
            
    elapsed = time.time() - start_time
    print(f"-> Time Taken: {elapsed:.4f} seconds")

def test_sequential_large_file(num_files, file_size_bytes):
    print("\nTest 2: Reading 1 large packed file (TFRecord format)")
    start_time = time.time()
    
    # Low OS Overhead: Open once -> Read sequentially in chunks -> Close once
    with open("packed_dataset.tfrecord", "rb") as f:
        for i in range(num_files):
            data = f.read(file_size_bytes)
            
    elapsed = time.time() - start_time
    print(f"-> Time Taken: {elapsed:.4f} seconds")

def cleanup(num_files):
    for i in range(num_files):
        os.remove(f"raw_images_folder/img_{i}.bin")
    os.rmdir("raw_images_folder")
    os.remove("packed_dataset.tfrecord")

def main():

    NUM_FILES = 1000
    FILE_SIZE = 4096 # 4KB per file
    
    setup_test_files(NUM_FILES, FILE_SIZE)
    
    test_random_small_files(NUM_FILES)
    test_sequential_large_file(NUM_FILES, FILE_SIZE)
    
    cleanup(NUM_FILES)

if __name__ == "__main__":
    main()
Step 3.2: Execute and Analyze
`

Run python ai_dataset_io.py. Notice that even though the total amount of bytes read is exactly the same, Test 2 is noticeably faster. In a real AI training server with SSDs and millions of files, Test 1 can take hours, while Test 2 takes minutes. This proves why understanding OS I/O behavior is critical for AI performance.
5. Phase 4: Analysis & Conclusion (30 Minutes)
Save your work to GitHub before proceeding:

`
git add .
git commit -m "Completed Lab 8 coding"
git push
Lab Report Assignment
`

Create a file named Lab08_Report.txt, copy the template below, answer the questions, and push it to your repository.

`
======================================================
COE67-222 Operating Systems - Lab 08 Report
Name: 
Student ID: 
======================================================

1. Disk Scheduling (Phase 2):
Looking at the output of `disk_scheduler.py`, why did the SCAN algorithm result in a significantly lower "Total Head Movement" compared to FCFS? Explain the logic behind the Elevator behavior.

2. I/O Bound Concept:
If an Operating System is described as being "I/O Bound" during a task, what does that actually mean for the CPU? Is the CPU at 100% usage or is it mostly idle? Why?

3. AI Industry Connection (Phase 3):
Explain why storing an AI image dataset as 1,000,000 separate `.jpg` files causes high I/O overhead and GPU starvation compared to packing them into a single sequential binary format (e.g., TFRecord, WebDataset, or HDF5).

`
