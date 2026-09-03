# COE67-222: Operating Systems - Lab 01

Welcome to Lab 1: Cloud OS Environment and System Profiling.

## How to start:
1. Click the green **"Use this template"** button.
2. Select **"Create a new repository"**.
3. Name your repository `OS-Lab01-StudentID`.
4. Once created, click the **"Code"** button, go to the **"Codespaces"** tab, and click **"Create codespace on main"**.
5. Follow the Lab Manual provided by the instructor.

## Local Python setup

Create and activate a virtual environment from the repository root:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Run the hardware profiler with:

```bash
python profiler.py
```

Run `stress_test.py` only when you are ready to observe CPU usage. Stop it with `Ctrl+C`.
