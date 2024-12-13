import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext

def fifo_page_replacement(reference_string, num_frames):
    frames = []
    page_faults = 0
    result = "Step | Frames | Page Fault\n"

    for step, page in enumerate(reference_string, start=1):
        if page not in frames:
            page_faults += 1
            if len(frames) < num_frames:
                frames.append(page)
            else:
                frames.pop(0)
                frames.append(page)
            fault = "Yes"
        else:
            fault = "No"

        result += f"{step:4} | {frames} | {fault}\n"

    result += f"\nTotal Page Faults: {page_faults}\n"
    return result

def lru_page_replacement(reference_string, num_frames):
    frames = []
    usage_history = {}
    page_faults = 0
    current_time = 0
    result = "Step | Frames | Page Fault\n"

    for step, page in enumerate(reference_string, start=1):
        current_time += 1
        if page not in frames:
            page_faults += 1
            if len(frames) < num_frames:
                frames.append(page)
            else:
                lru_page = min(frames, key=lambda p: usage_history.get(p, float('inf')))
                frames.remove(lru_page)
                frames.append(page)
            usage_history[page] = current_time
            fault = "Yes"
        else:
            usage_history[page] = current_time
            fault = "No"

        result += f"{step:4} | {frames} | {fault}\n"

    result += f"\nTotal Page Faults: {page_faults}\n"
    return result

def optimal_page_replacement(reference_string, num_frames):
    frames = []
    page_faults = 0
    result = "Step | Frames | Page Fault\n"

    for step, page in enumerate(reference_string, start=1):
        if page not in frames:
            page_faults += 1
            if len(frames) < num_frames:
                frames.append(page)
            else:
                future_uses = {f: (reference_string[step:].index(f) if f in reference_string[step:] else float('inf')) for f in frames}
                page_to_replace = max(future_uses, key=future_uses.get)
                frames.remove(page_to_replace)
                frames.append(page)
            fault = "Yes"
        else:
            fault = "No"

        result += f"{step:4} | {frames} | {fault}\n"

    result += f"\nTotal Page Faults: {page_faults}\n"
    return result

def run_simulation():
    reference_string = ref_string_entry.get()
    num_frames = num_frames_entry.get()

    try:
        reference_list = list(map(int, reference_string.split()))
        frames = int(num_frames)
    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid inputs for reference string and number of frames.")
        return

    algorithm = algorithm_choice.get()
    if algorithm == "FIFO":
        result = fifo_page_replacement(reference_list, frames)
    elif algorithm == "LRU":
        result = lru_page_replacement(reference_list, frames)
    elif algorithm == "Optimal":
        result = optimal_page_replacement(reference_list, frames)
    else:
        messagebox.showerror("Algorithm Error", "Please select a valid algorithm.")
        return

    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, result)

# Create main window
root = tk.Tk()
root.title("Virtual Memory Simulator")

# Input Frame
input_frame = ttk.LabelFrame(root, text="Input Parameters")
input_frame.pack(padx=10, pady=10, fill="x")

# Reference String
ttk.Label(input_frame, text="Reference String:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
ref_string_entry = ttk.Entry(input_frame, width=40)
ref_string_entry.grid(row=0, column=1, padx=5, pady=5)

# Number of Frames
ttk.Label(input_frame, text="Number of Frames:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
num_frames_entry = ttk.Entry(input_frame, width=20)
num_frames_entry.grid(row=1, column=1, padx=5, pady=5)

# Algorithm Choice
ttk.Label(input_frame, text="Algorithm:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
algorithm_choice = ttk.Combobox(input_frame, values=["FIFO", "LRU", "Optimal"], state="readonly")
algorithm_choice.grid(row=2, column=1, padx=5, pady=5)
algorithm_choice.set("FIFO")

# Run Button
run_button = ttk.Button(input_frame, text="Run Simulation", command=run_simulation)
run_button.grid(row=3, column=0, columnspan=2, pady=10)

# Result Frame
result_frame = ttk.LabelFrame(root, text="Results")
result_frame.pack(padx=10, pady=10, fill="both", expand=True)

result_text = scrolledtext.ScrolledText(result_frame, wrap=tk.WORD, height=15)
result_text.pack(fill="both", expand=True, padx=5, pady=5)

# Run the application
root.mainloop()
