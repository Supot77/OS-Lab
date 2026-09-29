Laboratory 10: Mini-Project - AI Cluster OS Integration (The Ultimate Capstone)

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
Integrate all core OS concepts: Process Queues, Memory Management, CPU Scheduling, and File Systems.
Observe how the OS manages diverse AI workloads (Distributed Training vs. Preprocessing vs. Inference) concurrently.
Monitor a Live System Dashboard to analyze real-time RAM and GPU allocations.
Understand the architectural design of modern AI cluster orchestrators (e.g., Kubernetes, Slurm).
2. Phase 1: Theory Recap & Diverse AI Workloads (20 Minutes)
A real-world OS doesn't just run one type of program. In an AI Data Center, the OS must juggle diverse workloads simultaneously to maximize hardware utilization:
Workload A (Distributed Training): GPU-Bound & Memory-Bound. Takes massive RAM and multiple GPUs.
Workload B (Data Preprocessing): CPU-Bound & I/O-Bound. Uses RAM and CPU, but 0 GPUs. The OS can run this in parallel with Workload A!
Workload C (Inference API): Requires Low Latency. Uses very little RAM and a single GPU to quickly answer user queries.
Step 1.1: Create Your Workspace
Open your GitHub Codespaces environment.
Open the terminal and create a new directory:


`python
mkdir lab10
cd lab10

`
3. Phase 2: Building the Ultimate AI Cluster OS (50 Minutes)
We will write a comprehensive OS Simulator. It includes a Job Queue, a Scheduler Thread, Memory checks, Deadlock Avoidance, and a Live System Dashboard (like htop).
Step 2.1: Write the Integration Script
Create a file named ultimate_cluster_os.py:


`python
# ultimate_cluster_os.py
import threading
import time
import os
import queue

class AIClusterOS:
    def __init__(self, total_ram_gb, num_gpus):
        # 1. System Resources
        self.total_ram_gb = total_ram_gb
        self.available_ram_gb = total_ram_gb
        self.ram_lock = threading.Lock()

        self.gpu_locks = {i: threading.Lock() for i in range(num_gpus)}
        self.gpu_status = {i: "IDLE" for i in range(num_gpus)}

        # 2. OS Queues and State
        self.job_queue = queue.Queue()
        self.active_jobs = []
        self.is_running = True

        # 3. Start Background Threads (OS Kernel & Dashboard)
        self.dash_thread = threading.Thread(target=self._dashboard_loop, daemon=True)
        self.dash_thread.start()

        self.scheduler_thread = threading.Thread(target=self._os_scheduler_loop)
        self.scheduler_thread.start()

    def _dashboard_loop(self):
        """Simulates 'htop' or 'nvidia-smi' updating every 1.5 seconds"""
        while self.is_running:
            time.sleep(1.5)
            print("\n" + "="*50)
            print(f"[LIVE DASHBOARD] RAM Available: {self.available_ram_gb}/{self.total_ram_gb} GB")
            gpu_str = " | ".join([f"GPU {i}: {self.gpu_status[i]}" for i in self.gpu_locks])
            print(f"[LIVE DASHBOARD] {gpu_str}")
            print(f"[LIVE DASHBOARD] Queue Size: {self.job_queue.qsize()} | Active Jobs: {len(self.active_jobs)}")
            print("="*50 + "\n")

    def submit_job(self, job_name, dataset_path, req_ram, req_gpus, duration):
        """User API: Submits job to the OS queue instantly."""
        self.job_queue.put((job_name, dataset_path, req_ram, req_gpus, duration))
        print(f"📥 [API] Submitted: {job_name} -> Queued.")

    def _os_scheduler_loop(self):
        """OS Kernel: constantly pulls jobs from the queue to process."""
        while self.is_running or not self.job_queue.empty():
            try:
                job_data = self.job_queue.get(timeout=1)
                # Spawn an OS worker thread to manage this specific job's resources
                worker = threading.Thread(target=self._execute_job, args=job_data)
                worker.start()
            except queue.Empty:
                continue

    def _execute_job(self, job_name, dataset_path, req_ram, req_gpus, duration):
        """The lifecycle of a single process in the OS."""
        # 1. FILE SYSTEM SECURITY (Lab 9)
        if not os.path.exists(dataset_path):
            print(f"❌ [{job_name}] FAILED: Dataset '{dataset_path}' not found or Permission Denied.")
            self.job_queue.task_done()
            return

        self.active_jobs.append(job_name)

        # 2. MEMORY MANAGEMENT (Wait until RAM is available to prevent Thrashing) (Lab 5 & 6)
        print(f"⏳ [{job_name}] Waiting for {req_ram}GB RAM...")
        while True:
            with self.ram_lock:
                if self.available_ram_gb >= req_ram:
                    self.available_ram_gb -= req_ram
                    break
            time.sleep(0.5) # Wait and check again

        print(f"🧠 [{job_name}] Allocated {req_ram}GB RAM.")

        # 3. DEADLOCK AVOIDANCE (Resource Hierarchy) (Lab 4)
        sorted_gpus = sorted(req_gpus)
        if sorted_gpus:
            print(f"⏳ [{job_name}] Waiting for GPUs {sorted_gpus}...")

        for gpu in sorted_gpus:
            self.gpu_locks[gpu].acquire()
            self.gpu_status[gpu] = f"BUSY ({job_name})"

        if sorted_gpus:
            print(f"🟢 [{job_name}] Acquired GPUs {sorted_gpus}. Running!")
        else:
            print(f"🟢 [{job_name}] Running on CPU only!")

        # 4. EXECUTION (Lab 7)
        time.sleep(duration)
        print(f"✅ [{job_name}] Finished successfully.")

        # 5. RELEASE RESOURCES
        for gpu in reversed(sorted_gpus):
            self.gpu_status[gpu] = "IDLE"
            self.gpu_locks[gpu].release()

        with self.ram_lock:
            self.available_ram_gb += req_ram

        self.active_jobs.remove(job_name)
        self.job_queue.task_done()

    def shutdown(self):
        """Waits for all queued jobs to finish before turning off."""
        self.job_queue.join()
        self.is_running = False
        self.scheduler_thread.join()
        time.sleep(2.0) # Let dashboard print final state
        print("\n=== Cluster OS Shutdown Gracefully ===")

def main():
    # Setup: Create a dummy secure dataset file
    with open("secure_dataset.csv", "w") as f:
        f.write("dummy data")

    print("=== Booting AI Cluster OS (64GB RAM, 4 GPUs) ===")
    os_system = AIClusterOS(total_ram_gb=64, num_gpus=4)

    # -------------------------------------------------------------
    # SIMULATING DIVERSE CONCURRENT AI WORKLOADS
    # -------------------------------------------------------------

    # Workload A: Distributed Training (Heavy RAM, Multiple GPUs, Long)
    os_system.submit_job("Workload_A_LLaMA", "secure_dataset.csv", req_ram=40, req_gpus=[2, 1, 0], duration=8)
    time.sleep(1) # Wait a bit before next submission

    # Workload B: Data Preprocessing (CPU/IO Bound, Medium RAM, 0 GPUs)
    # OBSERVE: This will run IN PARALLEL with Workload A because it needs no GPUs!
    os_system.submit_job("Workload_B_Preproc", "secure_dataset.csv", req_ram=16, req_gpus=[], duration=6)
    time.sleep(1)

    # Workload C: Fast API Inference (Low RAM, 1 GPU, Fast)
    # OBSERVE: This will sneak into the unused GPU 3 while Workload A hogs GPUs 0, 1, 2!
    os_system.submit_job("Workload_C_Infer", "secure_dataset.csv", req_ram=2, req_gpus=[3], duration=3)
    time.sleep(1)

    # Malicious/Error Job: Requesting a file that doesn't exist
    os_system.submit_job("Workload_D_Hacker", "secret_keys.txt", req_ram=1, req_gpus=[], duration=1)

    # Wait for the system to process everything
    os_system.shutdown()

    # Cleanup
    os.remove("secure_dataset.csv")

if __name__ == "__main__":
    main()

`
#### Step 2.2: Execute and Observe (The "Wow" Factor)
Run the script: python ultimate_cluster_os.py
Observation Task (Watch the Live Dashboard closely!):
Watch Workload A grab 40GB of RAM and lock GPUs 0, 1, and 2.
Watch Workload B skip the GPU line completely and run on the CPU alongside Workload A, utilizing the remaining RAM perfectly.
Watch Workload C slide into the only remaining GPU (GPU 3) and finish quickly, demonstrating how OS scheduling maximizes hardware utilization.
See Workload D get rejected instantly by the OS File System security check.
4. Phase 3: Final Analysis & Conclusion (50 Minutes)
Save your final project to GitHub:


`python
git add .
git commit -m "Completed Lab 10 - Ultimate AI Cluster OS"
git push

`
5. Report Assignment
Create a file named Lab10_Report.txt, copy the template below, answer the comprehensive questions, and push it to your repository.


`python
======================================================
COE67-222 Operating Systems - Lab 10 Report (Final)
Name:
Student ID:
======================================================

1. The Role of the Operating System:
In this mini-project, our Python script simulated the major responsibilities of an Operating System.
Match the specific code behavior in `ultimate_cluster_os.py` to the corresponding OS concept you learned throughout the semester:

- File System & Permissions (Lab 9):
  [Explain which line of code simulated this and why Workload D failed]

- Memory Management (Labs 5/6):
  [Explain how the OS prevented Thrashing by using the `while` loop for RAM allocation]

- Concurrency & Deadlocks (Labs 3/4):
  [Explain how the OS sorted the requested GPUs to avoid Circular Wait deadlocks]

2. Hardware Utilization:
Look at the output of your Live Dashboard. Explain how the OS successfully ran Workload A (LLaMA Training), Workload B (Preprocessing), and Workload C (Inference) AT THE SAME TIME without crashing. Why didn't they block each other?

3. Course Reflection (AI Engineering Context):
You are now applying for a role as a Machine Learning Operations (MLOps) Engineer.
Write a short paragraph explaining how understanding Operating Systems (Process queues, RAM/Virtual Memory limits, Deadlock avoidance, File systems) gives you an advantage over a programmer who only knows how to write basic Python/PyTorch scripts.

`

