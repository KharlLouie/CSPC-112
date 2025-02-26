import tkinter as tk
from tkinter import messagebox, ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

def fcfs_scheduling(processes):
    processes.sort(key=lambda x: x[1])
    schedule = []
    current_time = 0
    for pid, arrival, burst in processes:
        if current_time < arrival:
            current_time = arrival
        completion = current_time + burst
        tat = completion - arrival
        waiting = tat - burst
        schedule.append((pid, arrival, burst, completion, tat, waiting))
        current_time = completion
    return schedule

def sjf_non_preemptive(processes):
    processes.sort(key=lambda x: (x[1], x[2]))
    schedule = []
    current_time = 0
    remaining_processes = processes.copy()
    while remaining_processes:
        available = [p for p in remaining_processes if p[1] <= current_time]
        if not available:
            current_time = remaining_processes[0][1]
            available = [remaining_processes[0]]
        available.sort(key=lambda x: x[2])
        pid, arrival, burst = available[0]
        completion = current_time + burst
        tat = completion - arrival
        waiting = tat - burst
        schedule.append((pid, arrival, burst, completion, tat, waiting))
        remaining_processes.remove(available[0])
        current_time = completion
    return schedule

def sjf_preemptive(processes):
    processes.sort(key=lambda x: x[1])
    remaining_time = {p[0]: p[2] for p in processes}
    current_time = 0
    schedule = []
    gantt = []
    completed = {}
    while remaining_time:
        available = [p for p in processes if p[1] <= current_time and remaining_time.get(p[0], 0) > 0]
        if not available:
            current_time += 1
            continue
        available.sort(key=lambda x: (remaining_time[x[0]], x[1]))
        pid = available[0][0]
        gantt.append((pid, current_time, current_time + 1))
        remaining_time[pid] -= 1
        current_time += 1
        if remaining_time[pid] == 0:
            del remaining_time[pid]
            completion_time = current_time
            arrival_time = processes[pid - 1][1]
            burst_time = processes[pid - 1][2]
            tat = completion_time - arrival_time
            waiting = tat - burst_time
            schedule.append((pid, arrival_time, burst_time, completion_time, tat, waiting))
    return schedule, gantt

arrival_entries = []
burst_entries = []

def create_entries():
    global arrival_entries, burst_entries
    for widget in process_frame.winfo_children():
        widget.destroy()
    
    try:
        num_processes = int(num_processes_entry.get())
        arrival_entries = []
        burst_entries = []
        
        tk.Label(process_frame, text="Process", bg='#f0f0f0').grid(row=0, column=0)
        tk.Label(process_frame, text="Arrival Time", bg='#f0f0f0').grid(row=0, column=1)
        tk.Label(process_frame, text="Burst Time", bg='#f0f0f0').grid(row=0, column=2)
        
        for i in range(num_processes):
            tk.Label(process_frame, text=f"P{i+1}", bg='#f0f0f0').grid(row=i+1, column=0)
            arrival_entry = tk.Entry(process_frame, width=10)
            arrival_entry.grid(row=i+1, column=1)
            burst_entry = tk.Entry(process_frame, width=10)
            burst_entry.grid(row=i+1, column=2)
            
            arrival_entries.append(arrival_entry)
            burst_entries.append(burst_entry)
    except ValueError:
        messagebox.showerror("Input Error", "Please enter a valid number of processes!")



def display_gantt_chart(gantt, frame):
    fig, ax = plt.subplots(figsize=(10, 2))

    num_processes = len(set(pid for pid, _, _ in gantt))  # Count unique processes
    gray_shades = np.linspace(0.3, 0.9, num_processes)  # Generate shades from dark to light
    process_colors = {pid: str(gray) for pid, gray in zip(sorted(set(pid for pid, _, _ in gantt)), gray_shades)}

    for pid, start, end in gantt:
        ax.barh(y=0, width=end - start, left=start, color=process_colors[pid], edgecolor='black')
        ax.text((start + end) / 2, 0, f'P{pid}', va='center', ha='center', color='black', fontweight='bold')

    ax.set_xticks(np.arange(0, gantt[-1][2] + 1, 1))
    ax.set_yticks([])
    ax.set_xlabel("Time")
    ax.set_title("Gantt Chart")

    for widget in frame.winfo_children():
        widget.destroy()

    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    canvas.get_tk_widget().pack()

def run_scheduling():
    try:
        num_processes = int(num_processes_entry.get())
        processes = [(i + 1, int(arrival_entries[i].get()), int(burst_entries[i].get())) for i in range(num_processes)]
        algo = algo_choice.get()

        if algo == "FCFS":
            schedule = fcfs_scheduling(processes)
            gantt = [(p[0], p[3] - p[2], p[3]) for p in schedule]
        elif algo == "SJF (Non-Preemptive)":
            schedule = sjf_non_preemptive(processes)
            gantt = [(p[0], p[3] - p[2], p[3]) for p in schedule]
        elif algo == "SJF (Preemptive)":
            schedule, gantt = sjf_preemptive(processes)
        else:
            messagebox.showerror("Error", "Invalid Algorithm Selected")
            return

        # **Sort schedule by Process ID (PID)**
        schedule.sort(key=lambda x: x[0])

        output_text.config(state="normal")  # Enable text box for writing
        output_text.delete("1.0", tk.END)   # Clear previous content

        # Insert header
        output_text.insert(tk.END, "Process | Arrival | Burst | Completion | Turnaround | Waiting\n")
        output_text.insert(tk.END, "-" * 60 + "\n")

        # Insert sorted schedule
        for p in schedule:
            output_text.insert(tk.END, f"{p[0]:<7} | {p[1]:<7} | {p[2]:<5} | {p[3]:<10} | {p[4]:<10} | {p[5]:<7}\n")

        # Calculate and display averages
        avg_tat = sum(p[4] for p in schedule) / len(schedule)
        avg_wt = sum(p[5] for p in schedule) / len(schedule)
        output_text.insert(tk.END, f"\nAverage Turnaround Time: {avg_tat:.2f}\n")
        output_text.insert(tk.END, f"Average Waiting Time: {avg_wt:.2f}\n")

        output_text.config(state="disabled")  # Make text box read-only again
        display_gantt_chart(gantt, gantt_frame)

    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numerical values!")
root = tk.Tk()
root.title("CPU Scheduling Simulator")
root.geometry("1000x700")
root.configure(bg='#f0f0f0')

tk.Label(root, text="Number of Processes:", bg='#f0f0f0').pack()
num_processes_entry = tk.Entry(root)
num_processes_entry.pack()
tk.Button(root, text="Set Processes", command=create_entries).pack(pady=10)

tk.Label(root, text="Select Scheduling Algorithm:", bg='#f0f0f0').pack()
algo_choice = ttk.Combobox(root, values=["FCFS", "SJF (Non-Preemptive)", "SJF (Preemptive)"])
algo_choice.pack()
algo_choice.set("FCFS")

process_frame = tk.Frame(root, bg='#f0f0f0')
process_frame.pack()
tk.Button(root, text="Run Scheduling", command=run_scheduling).pack(pady=10)

output_text = tk.Text(root, height=10, width=100)
output_text.pack(pady=10)

gantt_frame = tk.Frame(root, bg='#f0f0f0')
gantt_frame.pack(fill=tk.BOTH, expand=True)

root.mainloop()

