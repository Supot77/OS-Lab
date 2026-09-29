Laboratory 7: CPU Scheduling Algorithms and Fairness

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
Understand the role of the OS Short-Term Scheduler in allocating CPU time to ready processes.
Implement and evaluate the First-Come, First-Served (FCFS) scheduling algorithm.
Implement and evaluate the Round Robin (RR) scheduling algorithm with time slicing (Time Quantum).
Apply CPU scheduling concepts to an AI Inference API to minimize user waiting time.
2. Phase 1: Theory Recap & Workspace Setup (20 Minutes)
When multiple processes are in the "Ready" state, the OS must decide which one gets the CPU next.
FCFS (First-Come, First-Served): Non-preemptive. The first process runs to completion before the next one starts. It is simple but can cause the "Convoy Effect" (short jobs get stuck behind a massive job).
Round Robin (RR): Preemptive. The OS gives each process a small slice of CPU time (Time Quantum). If the process isn't finished, the OS pauses it and moves it to the back of the queue, ensuring fairness.
Step 1.1: Create Your Workspace
Open your GitHub Codespaces environment.
Open the terminal and create a new directory for this week's lab:



`python
mkdir lab07
cd lab07


`
3. Phase 2: Building the OS Scheduler Simulator (40 Minutes)
We will write a simulator to calculate the Turnaround Time (Time from arrival to completion) and Waiting Time (Total time spent waiting in the queue) for both FCFS and Round Robin.
Step 2.1: Write the Scheduler Script
Create a file named cpu_scheduler.py:



`python
# cpu_scheduler.py

def simulate_fcfs(processes):
    print("\n--- Running FCFS Scheduler ---")
    current_time = 0
    total_wait_time = 0
    total_turnaround_time = 0

    for pid, burst_time in processes:
        wait_time = current_time
        total_wait_time += wait_time
        turnaround_time = wait_time + burst_time
        total_turnaround_time += turnaround_time
        print(f"[Time {current_time:02d}] Process {pid} starts. (Wait time: {wait_time})")

        current_time += burst_time
        print(f"[Time {current_time:02d}] Process {pid} finishes. (Turnaround time: {turnaround_time})")

    avg_wait = total_wait_time / len(processes)
    avg_turnaround = total_turnaround_time / len(processes)
    print(f">> FCFS Average Waiting Time: {avg_wait:.2f}")
    print(f">> FCFS Average Turnaround Time: {avg_turnaround:.2f}")

def simulate_round_robin(processes, quantum):
    print(f"\n--- Running Round Robin Scheduler (Quantum = {quantum}) ---")
    remaining_burst = {pid: burst for pid, burst in processes}
    wait_times = {pid: 0 for pid, burst in processes}
    last_run_time = {pid: 0 for pid, burst in processes}
    finish_times = {}

    current_time = 0
    queue = [pid for pid, burst in processes]

    while queue:
        pid = queue.pop(0)
        wait_times[pid] += (current_time - last_run_time[pid])
        time_to_run = min(quantum, remaining_burst[pid])
        print(f"[Time {current_time:02d}] Process {pid} runs for {time_to_run} units.")

        current_time += time_to_run
        remaining_burst[pid] -= time_to_run
        last_run_time[pid] = current_time

        if remaining_burst[pid] > 0:
            queue.append(pid)
        else:
            finish_times[pid] = current_time
            print(f"[Time {current_time:02d}] Process {pid} finishes.")

    total_wait = sum(wait_times.values())
    avg_wait = total_wait / len(processes)

    # All arrived at Time 0, so Turnaround Time = finish_time
    turnaround_times = {pid: finish_times[pid] for pid, _ in processes}
    avg_turnaround = sum(turnaround_times.values()) / len(processes)

    print(f">> Round Robin Average Waiting Time: {avg_wait:.2f}")
    print(f">> Round Robin Average Turnaround Time: {avg_turnaround:.2f}")

def main():
    # Format: (Process_ID, CPU_Burst_Time)
    # Assume all arrive at Time 0
    os_ready_queue = [
        ("P1", 10), # A massive CPU-heavy task
        ("P2", 2),  # A tiny task
        ("P3", 3)   # A small task
    ]

    simulate_fcfs(os_ready_queue)
    simulate_round_robin(os_ready_queue, quantum=3)

if __name__ == "__main__":
    main()

`
Step 2.2: Execute and Observe
Run the script: python cpu_scheduler.py Observation: In FCFS, P2 and P3 have to wait a very long time because P1 hogs the CPU (The Convoy Effect). In Round Robin, P2 and P3 get a slice of the CPU early on, finishing much faster and significantly reducing the average waiting time.
4. Phase 3: AI Industry Connection - LLM Inference Server (30 Minutes)
When you deploy a Large Language Model (like ChatGPT), multiple users send requests to your server at the same time.
User A asks: "Write a 10-page essay on Operating Systems." (Heavy task - requires generating 1000 tokens).
User B asks: "What is 1+1?" (Light task - requires generating 2 tokens).
If your AI server uses a strict FCFS queue, User B will be completely blocked for 30 seconds just waiting for User A's essay to finish. This is unacceptable for user experience. Modern AI Inference Engines use OS Round Robin / Iteration-Level Scheduling (Continuous Batching) to generate 1 token for User A, then 1 token for User B, ensuring short queries finish instantly.
Step 4.1: Write the AI Server Scheduler
Create a file named ai_inference_scheduler.py:


`python
# ai_inference_scheduler.py
import time

class AIRequest:
    def __init__(self, user_id, tokens_required):
        self.user_id = user_id
        self.tokens_required = tokens_required
        self.tokens_generated = 0

def simulate_ai_fcfs(requests):
    print("\n[AI Server] Strategy: First-Come, First-Served")
    for req in requests:
        print(f"-> Starting {req.user_id} (Needs {req.tokens_required} tokens)...")
        time.sleep(0.5) # Simulating heavy GPU computation
        print(f"   [DONE] {req.user_id} finished. Responded perfectly.")

def simulate_ai_round_robin(requests):
    print("\n[AI Server] Strategy: Round Robin (Token-by-Token Continuous Batching)")
    queue = list(requests)

    while queue:
        req = queue.pop(0)

        # Generate exactly 1 token (Time Quantum = 1 Token)
        req.tokens_generated += 1

        if req.tokens_generated == req.tokens_required:
            print(f"   [DONE] {req.user_id} finished early! (Total: {req.tokens_required} tokens)")
        else:
            # Task not finished, push to the back of the queue
            queue.append(req)

        time.sleep(0.05) # Simulating fast token generation

def main():
    # User A wants 10 tokens (heavy). User B wants 2 tokens (light).
    print("--- Incoming API Requests ---")

    # Resetting objects for FCFS
    reqs_fcfs = [AIRequest("User_A_Essay", 10), AIRequest("User_B_Math", 2)]
    simulate_ai_fcfs(reqs_fcfs)

    # Resetting objects for Round Robin
    reqs_rr = [AIRequest("User_A_Essay", 10), AIRequest("User_B_Math", 2)]
    simulate_ai_round_robin(reqs_rr)

if __name__ == "__main__":
    main()

`
Step 4.2: Execute and Analyze
Run python ai_inference_scheduler.py. Notice how in the FCFS approach, User_B is stuck waiting for User_A to completely finish the 10-token essay. In the Round Robin approach, User_B gets their 2 tokens quickly and exits the system gracefully, while User_A continues processing in the background.
5. Phase 4: Analysis & Conclusion (30 Minutes)
Save your work to GitHub before proceeding:


`python
git add .
git commit -m "Completed Lab 7 coding"
git push


`
Lab Report Assignment
Create a file named Lab07_Report.txt, copy the template below, answer the questions, and push it to your repository.



`python
======================================================
COE67-222 Operating Systems - Lab 07 Report
Name:
Student ID:
======================================================

1. The Convoy Effect (Phase 2):
In the FCFS output of `cpu_scheduler.py`, what is the "Convoy Effect"? How did the presence of Process P1 affect the waiting times of P2 and P3?

2. Choosing the Time Quantum:
In Round Robin, the Time Quantum is critical.
- What happens if the OS sets the Time Quantum extremely large (e.g., Quantum = 100)? Which algorithm does RR start to behave like?
- What happens if the OS sets the Time Quantum extremely small (e.g., Quantum = 0.0001)? (Hint: Think about Context Switching overhead).

3. AI Context:
In Phase 3, we used a Round Robin approach for generating tokens in an LLM. Explain why iteration-level Round Robin scheduling prevents long user queries from starving short queries, and how it improves perceived latency (Time To First Token / TTFT) for interactive AI applications.

`

