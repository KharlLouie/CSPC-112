import threading
import time
import tkinter as tk
from tkinter import ttk

# Buffer settings
BUFFER_SIZE = 5
buffer = []
mutex = threading.Semaphore(1)  # Ensures mutual exclusion
empty_slots = threading.Semaphore(BUFFER_SIZE)  # Controls producer
full_slots = threading.Semaphore(0)  # Controls consumer

consumer_sleep = 2.5 #rest time for consumer
producer_sleep = 1 #rest time for producer

# GUI Setup
class ProducerConsumerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Producer-Consumer Simulation")


        # Table Setup
        self.tree = ttk.Treeview(root, columns=("Step", "Producer Action", "Consumer Action", "Buffer Contents", "Empty", "Full"), show="headings")
        self.tree.heading("Step", text="Step")
        self.tree.heading("Producer Action", text="Producer Action")
        self.tree.heading("Consumer Action", text="Consumer Action")
        self.tree.heading("Buffer Contents", text="Buffer Contents")
        self.tree.heading("Empty", text="Empty")
        self.tree.heading("Full", text="Full")
        self.tree.pack()

        # Status Labels
        self.status_label = tk.Label(root, text="Status: Waiting", font=("Arial", 12))
        self.status_label.pack()

        # Step Counter
        self.step = 0

    def update_table(self, producer_action, consumer_action):
        self.step += 1
        buffer_state = list(buffer)  # Convert buffer to a list for display
        self.tree.insert("", "end", values=(self.step, producer_action, consumer_action, str(buffer), BUFFER_SIZE - len(buffer), len(buffer)))
        self.status_label.config(text=f"Buffer: {buffer_state}")
        self.root.update_idletasks()

# Producer function
def producer(gui):
    for i in range(1, 11):
        time.sleep(int(producer_sleep) if i == 1 else 1)  # Delay before starting

        empty_slots.acquire()  # Wait if buffer is full
        mutex.acquire()  # Lock buffer

        buffer.append(i)  # Produce item
        gui.update_table(f"Produced {i}", "")

        mutex.release()  # Unlock buffer
        full_slots.release()  # Signal that a new item is available

# Consumer function
def consumer(gui):
    for i in range(1, 11):
        time.sleep(int(consumer_sleep))  # Delay between consumptions

        full_slots.acquire()  # Wait if buffer is empty
        mutex.acquire()  # Lock buffer

        item = buffer.pop(0)  # Consume item
        gui.update_table("", f"Consumed {item}")

        mutex.release()  # Unlock buffer
        empty_slots.release()  # Signal that an empty slot is available


# Main function to start threads
def main():
    root = tk.Tk()
    gui = ProducerConsumerGUI(root)

    producer_thread = threading.Thread(target=producer, args=(gui,))
    consumer_thread = threading.Thread(target=consumer, args=(gui,))

    producer_thread.start()
    consumer_thread.start()

    root.mainloop()

    producer_thread.join()
    consumer_thread.join()

if __name__ == "__main__":
    main()