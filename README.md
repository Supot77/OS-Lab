# COE67-222: Operating Systems Laboratory Repository

ยินดีต้อนรับสู่คลังปฏิบัติการรายวิชา COE67-222 Operating Systems

## 🚀 การเริ่มต้นใช้งานบน GitHub Codespaces

1. กดปุ่ม **"Code"** สีเขียวด้านบน
2. เลือกแท็บ **"Codespaces"** แล้วคลิก **"Create codespace on main"**
3. ระบบจะทำการตั้งค่า Container อัตโนมัติ (ติดตั้ง Ubuntu Linux, Python 3.11, `htop`, `psutil`, และ `numpy`)
4. เมื่อ Codespace พร้อมใช้งาน สามารถเปิด Terminal แล้วเลือกทำ Lab ที่ต้องการได้ทันที

---

## 💻 การติดตั้งบนเครื่อง Local (ทางเลือก)

```bash
python -m venv .venv
# บน Linux/macOS:
source .venv/bin/activate
# บน Windows PowerShell:
# .\.venv\Scripts\Activate.ps1

python -m pip install -r requirements.txt
```

---

## 📂 โครงสร้างของห้องปฏิบัติการ (Labs Overview)

| ห้องปฏิบัติการ | หัวข้อหลัก | ไฟล์สคริปต์ | เอกสารรายงาน |
| :--- | :--- | :--- | :--- |
| **Lab 01** | Cloud OS Environment & System Profiling | `profiler.py`, `stress_test.py` | `Lab01_Report.txt` |
| **Lab 02** | Processes, Threads & Concurrency | `runner_seq.py`, `runner_thread.py`, `runner_process.py`, `fork_zombie.py`, `task.py` | `Lab02_Report.txt` |
| **Lab 03** | Inter-Process Communication (IPC) & Synchronization | `ipc_pipe.py`, `race_condition.py`, `producer_consumer.py` | `Lab03_Report.txt` |
| **Lab 04** | Deadlocks & Starvation | `deadlock_simulation.py`, `deadlock_avoidance.py`, `starvation_sim.py`, `deadlock_detection.py`, `bankers_algo.py` | `Lab04_Report.txt` |
| **Lab 05** | Memory Management: Paging & Address Translation | `memory_allocation.py`, `page_table_sim.py`, `ai_mmap_model.py` | `Lab05_Report.txt` |
| **Lab 06** | Virtual Memory: Page Replacement & Thrashing | `page_replacement.py`, `ai_thrashing.py` | `Lab06_Report.txt` |
| **Lab 07** | CPU Scheduling Algorithms & Fairness | `cpu_scheduler.py`, `ai_inference_scheduler.py` | `Lab07_Report.txt` |
| **Lab 08** | I/O Management & Disk Scheduling | `disk_scheduler.py`, `ai_dataset_io.py` | `Lab08_Report.txt` |
| **Lab 09** | File Systems, Metadata & OS Security | `inode_inspector.py`, `os_security.py`, `ai_weight_protection.py` | `Lab09_Report.txt` |
| **Lab 10** | Mini-Project: AI Cluster OS Integration | `ultimate_cluster_os.py` | `Lab10_Report.txt` |

---

## 🧪 คำสั่งรันการทดลอง Lab 05 - Lab 10

### Lab 05: Memory Management (Paging & Address Translation)
```bash
cd lab05
python memory_allocation.py    # สังเกต RAM allocation (เปิด terminal แยกเพื่อรัน htop ได้)
python page_table_sim.py        # คำนวณ Logical Address -> Physical Address (Page Table)
python ai_mmap_model.py         # จำลอง Memory-Mapped Files (mmap)
```

### Lab 06: Virtual Memory (Page Replacement & Thrashing)
```bash
cd lab06
python page_replacement.py      # เปรียบเทียบ FIFO vs LRU Page Replacement
python ai_thrashing.py          # จำลองผลกระทบของ Thrashing เมื่อเกิด OOM
```

### Lab 07: CPU Scheduling Algorithms & Fairness
```bash
cd lab07
python cpu_scheduler.py         # จำลอง FCFS และ Round Robin (Time Quantum)
python ai_inference_scheduler.py # จำลอง AI Token Continuous Batching Scheduler
```

### Lab 08: I/O Management & Disk Scheduling
```bash
cd lab08
python disk_scheduler.py        # จำลอง FCFS vs SCAN (Elevator Algorithm)
python ai_dataset_io.py         # เปรียบเทียบ Random Small Files vs Sequential Large File
```

### Lab 09: File Systems, Metadata & OS Security
```bash
cd lab09
python inode_inspector.py       # ตรวจสอบ Inode และ POSIX Permissions ผ่าน os.stat
python os_security.py           # ทดสอบการจำกัดสิทธิ์ Read-Only ด้วย os.chmod(0o400)
python ai_weight_protection.py  # จำลองการป้องกัน AI Model Weights บน HPC Cluster (0o444)
```

### Lab 10: Mini-Project (AI Cluster OS Integration Capstone)
```bash
cd lab10
python ultimate_cluster_os.py   # รัน AI Cluster OS พร้อม Live Dashboard มอนิเตอร์ RAM & GPU
```

---

## 📝 การส่งงาน (Submission)
เมื่อทำการทดลองและตรวจสอบไฟล์รายงาน `LabXX_Report.txt` เรียบร้อยแล้ว ให้บันทึกและ push ขึ้น GitHub:
```bash
git add .
git commit -m "Complete Lab XX"
git push origin main
```
