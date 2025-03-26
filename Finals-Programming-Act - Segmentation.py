import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt

class SegmentTable:
    def __init__(self):
        self.segments = []

    def add_segment(self, base, limit):
        self.segments.append((base, limit))
    
    def translate_logical_to_physical(self, segment_number, offset):
        if segment_number < 0 or segment_number >= len(self.segments):
            return "Segmentation fault: Invalid segment number"
        base, limit = self.segments[segment_number]
        if offset < 0 or offset >= limit:
            return "Segmentation fault: Offset out of bounds"
        return base + offset

    def visualize_memory(self):
        if not self.segments:
            messagebox.showwarning("Warning", "No segments to visualize.")
            return
        
        fig, ax = plt.subplots(figsize=(3, len(self.segments) * 1.5))
        y_positions = []
        colors = ["red", "blue", "green", "purple", "orange"]

        # Sort segments by base address while preserving their original indices
        sorted_indices = sorted(range(len(self.segments)), key=lambda i: self.segments[i][0])
        sorted_segments = [self.segments[i] for i in sorted_indices]

        for i, seg_index in enumerate(sorted_indices):
            base, limit = sorted_segments[i]
            top = base + limit
            y_positions.append(top)
            y_positions.append(base)
            
            ax.bar(0, top - base, bottom=base, color=colors[seg_index % len(colors)], 
                   edgecolor='black', width=0.5)
            ax.text(0, base + (limit / 2), f"S{seg_index}", ha='center', va='center', 
                    color='white', fontsize=8, fontweight='bold')

        ax.set_xticks([])
        ax.set_yticks(y_positions)
        ax.set_yticklabels(y_positions)
        ax.set_ylabel("Memory Address")
        ax.set_title("Segmentation Memory Layout")
        ax.invert_yaxis()
        plt.show()


def add_segment():
    try:
        base, limit = map(int, entry_segment.get().split(","))
        seg_table.add_segment(base, limit)
        listbox_segments.delete(0, tk.END)
        for i, (b, l) in enumerate(seg_table.segments):
            listbox_segments.insert(tk.END, f"Segment {i}: Base {b}, Size {l}")
        entry_segment.delete(0, tk.END)
    except ValueError:
        messagebox.showerror("Error", "Invalid input. Enter base and limit as 'base,limit'")

def translate_address():
    try:
        seg_num, offset = map(int, entry_logical.get().split(","))
        result = seg_table.translate_logical_to_physical(seg_num, offset)
        lbl_result.config(text=f"Physical Address: {result}")
    except ValueError:
        messagebox.showerror("Error", "Invalid input. Enter segment and offset as 'segment,offset'")

def visualize():
    seg_table.visualize_memory()

# Create GUI
root = tk.Tk()
root.title("Memory Segmentation GUI")
root.geometry("400x500")

seg_table = SegmentTable()

# Input for segments
tk.Label(root, text="Enter Segment (base,limit):").pack(pady=5)
entry_segment = tk.Entry(root, width=50)
entry_segment.pack(pady=5)
frame_segment_buttons = tk.Frame(root)
frame_segment_buttons.pack(pady=10)
tk.Button(frame_segment_buttons, text="Add Segment", command=add_segment).pack(side=tk.LEFT, padx=5)
tk.Button(frame_segment_buttons, text="Clear Fields", command=lambda: entry_segment.delete(0, tk.END)).pack(side=tk.LEFT, padx=5)

# Listbox to show added segments
listbox_segments = tk.Listbox(root, height=6, width=50)
listbox_segments.pack(pady=5)

# Visualize memory
frame_visual_buttons = tk.Frame(root)
frame_visual_buttons.pack(pady=10)
tk.Button(frame_visual_buttons, text="Visualize Memory", command=visualize).pack(side=tk.LEFT, padx=5)
tk.Button(frame_visual_buttons, text="Clear Fields", command=lambda: listbox_segments.delete(0, tk.END)).pack(side=tk.LEFT, padx=5)

# Input for logical address
tk.Label(root, text="Enter Logical Address (segment,offset):").pack(pady=5)
entry_logical = tk.Entry(root, width=50)
entry_logical.pack(pady=5)
frame_logical_buttons = tk.Frame(root)
frame_logical_buttons.pack(pady=10)
tk.Button(frame_logical_buttons, text="Translate Address", command=translate_address).pack(side=tk.LEFT, padx=5)
tk.Button(frame_logical_buttons, text="Clear Fields", command=lambda: entry_logical.delete(0, tk.END)).pack(side=tk.LEFT, padx=5)

lbl_result = tk.Label(root, text="Physical Address: ")
lbl_result.pack(pady=10)

# Run GUI
root.mainloop()
