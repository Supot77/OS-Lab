Laboratory 9: File Systems, Metadata, and OS Security
Duration: 120 Minutes Platform: GitHub Codespaces (Ubuntu Linux) Language: Python
1. Lab Objectives
By the end of this laboratory session, students will be able to:
Understand the concept of Inodes and how the OS stores File Metadata.
Utilize POSIX System Calls (os.stat) to extract low-level file information.
Apply OS-level security permissions (os.chmod) to restrict Read/Write/Execute access.
Explain how AI Engineers use OS security to protect valuable machine learning model weights in shared clusters.
2. Phase 1: Theory Recap & Workspace Setup (20 Minutes)
When you save a file in Linux, the Operating System does not just save the data. It creates an Inode (Index Node). The Inode stores crucial metadata: who owns the file, how big it is, where the data blocks are on the hard drive, and most importantly, the Access Control List (Permissions).
Linux permissions are divided into three groups: Owner (User), Group, and Others. Each group can have Read (r=4), Write (w=2), and Execute (x=1) permissions. For example, a permission of 755 means the Owner has full rights (4+2+1=7), while everyone else can only read and execute (4+1=5).
Step 1.1: Create Your Workspace
Open your GitHub Codespaces environment.
Open the terminal and create a new directory for this week's lab:

`
mkdir lab09
cd lab09
3. Phase 2: Inspecting File Metadata (Inodes) (30 Minutes)
`

We will use the OS system call stat() to ask the OS kernel for the Inode details of a specific file, completely bypassing Python's high-level file reading functions.
Step 2.1: Write the Metadata Inspector
Create a file named inode_inspector.py and write the following code:

`
# inode_inspector.py
import os
import stat
import time

def inspect_file(filename):
    print(f"--- OS Inode Inspection for: {filename} ---")
    
    # OS System Call: stat() gets the file's metadata from the filesystem
    file_stats = os.stat(filename)
    
    # Extracting Metadata
    inode_number = file_stats.st_ino
    file_size_bytes = file_stats.st_size
    
    # Formatting timestamps
    created_time = time.ctime(file_stats.st_ctime)
    modified_time = time.ctime(file_stats.st_mtime)
    
    # Decoding POSIX Permissions
    # stat.filemode converts raw bits into human-readable format (e.g., -rw-r--r--)
    permissions = stat.filemode(file_stats.st_mode)
    
    print(f"Inode Number:     {inode_number}")
    print(f"File Size:        {file_size_bytes} bytes")
    print(f"Created On:       {created_time}")
    print(f"Last Modified:    {modified_time}")
    print(f"OS Permissions:   {permissions}")

def main():
    test_file = "dataset_sample.csv"
    
    # Create a dummy file
    with open(test_file, "w") as f:
        f.write("id,feature_1,feature_2,label\n")
        f.write("1,0.5,0.8,cat\n")
        
    inspect_file(test_file)

if __name__ == "__main__":
    main()
Step 2.2: Execute and Observe
`

Run python inode_inspector.py. You will see the unique Inode number assigned by the Linux kernel. Notice the default OS permissions. Usually, it is -rw-rw-r-- (or 664), meaning you and your group can read/write, but others can only read.
4. Phase 3: Modifying Permissions & OS Security (30 Minutes)
Now, let's see what happens when the OS blocks an application from modifying a file. We will use the chmod() system call to change the security bits.
Step 3.1: Write the Security Script
Create a file named os_security.py and write the following code:

`
# os_security.py
import os
import stat

def main():
    secure_file = "secret_config.json"
    
    # Clean up any read-only file from previous runs
    if os.path.exists(secure_file):
        os.chmod(secure_file, 0o666)
        os.remove(secure_file)
        
    # 1. Create a file normally
    with open(secure_file, "w") as f:
        f.write("{'api_key': '12345XYZ'}")
    print(f"Created {secure_file}.")
    
    # 2. Lock down the file using OS chmod (Change Mode)
    # 0o400 in Octal: User can Read (4). Group (0) and Others (0) have no access.
    print("Locking file permissions to Read-Only (0o400)...")
    os.chmod(secure_file, 0o400) 
    print(f"New Permissions: {stat.filemode(os.stat(secure_file).st_mode)}")
    
    # 3. Try to maliciously overwrite the file
    print("\nAttempting to overwrite the file...")
    try:
        with open(secure_file, "a") as f:
            f.write("\nMALICIOUS HACKER DATA")
        print("Success! Data written.")
    except PermissionError as e:
        print(f">>> [OS KERNEL BLOCKED] PermissionError: {e}")
        print(">>> The Operating System successfully protected the file!")

if __name__ == "__main__":
    main()
Step 3.2: Execute and Observe
`

Run python os_security.py. Even though your Python script is the one that created the file, the moment you told the OS to change the permission to 0o400 (Read-Only), the OS strictly enforced it. The subsequent write attempt was blocked at the kernel level, throwing a PermissionError.
5. Phase 4: AI Industry Connection - Securing Model Weights (20 Minutes)
Training a Large Language Model (LLM) like GPT-4 costs tens of millions of dollars in GPU compute time. The final product of this massive effort is a simple file containing the Neural Network weights (e.g., model_v1.pth).
In enterprise environments, data scientists share giant GPU clusters (HPC). If an engineer accidentally points their training script to overwrite the production model_v1.pth file instead of creating a new one, millions of dollars of work are instantly destroyed.
AI Engineers rely on OS-level File Security (not just Python try-except blocks) to protect these assets. They change the model files to Read-Only (0o444) and change the ownership (chown) to a strict Admin group. The OS acts as the ultimate gatekeeper—if a buggy AI script tries to open the weights in "w" (write) mode, the Linux Kernel kills the operation instantly.
Step 4.1: Simulate AI Asset Protection
Create a file named ai_weight_protection.py and write the following code:

`
# ai_weight_protection.py
import os

def simulate_hpc_cluster():
    weight_file = "production_resnet50.pth"
    
    # Clean up any read-only file from previous runs
    if os.path.exists(weight_file):
        os.chmod(weight_file, 0o666)
        os.remove(weight_file)
        
    # Simulate downloading the trained model
    print("Downloading 250MB Production Model Weights...")
    with open(weight_file, "w") as f:
        f.write("0101010101010101010") # Fake binary weight data
    
    # AI Ops: Securing the asset
    print("AI Ops: Securing model weights at the OS level (Read-Only)...")
    os.chmod(weight_file, 0o444) # Everyone can read, NO ONE can write
    
    # Simulate a Junior Developer running a buggy training script
    print("\n[Junior Dev] Running script: training_job.py")
    print("[Junior Dev] 'Oops, I opened the production model in Write mode!'")
    
    try:
        # The buggy code
        model = open(weight_file, "w") 
        model.write("Initializing random weights... Overwriting!")
        model.close()
    except PermissionError:
        print(">>> [DISASTER AVERTED] OS Kernel denied write access.")
        print(">>> The multi-million dollar model is safe.")

if __name__ == "__main__":
    simulate_hpc_cluster()
Run python ai_weight_protection.py to see the OS save the day.
`

6. Phase 5: Analysis & Conclusion (20 Minutes)
Save your work to GitHub before proceeding:

`
git add .
git commit -m "Completed Lab 9 coding"
git push
Lab Report Assignment
`

Create a file named Lab09_Report.txt, copy the template below, answer the questions, and push it to your repository.

`
======================================================
COE67-222 Operating Systems - Lab 09 Report
Name: 
Student ID: 
======================================================1. Inodes and Metadata:
In the `inode_inspector.py` script, we printed the "Inode Number". If you rename the file using the Linux `mv` command, will the Inode Number change? Why or why not? (Hint: Think about how the OS separates the file name from the actual data).

2. POSIX Permissions:
If you want to set a file's permission so that the Owner has Read/Write/Execute (7), the Group has Read/Execute (5), and Others have absolutely no access (0), what would be the 3-digit octal number you pass into `os.chmod()`? 

3. The AI Context:
Why is it safer to rely on Operating System file permissions (like `os.chmod(0o444)`) to protect production model weights rather than relying solely on application-level logic or Python try-except blocks?

`

