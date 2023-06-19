import tkinter as tk
from tkinter import messagebox


class DiskScheduler:
    def __init__(self, sequence):
        self.sequence = sequence

    def fcfs(self, initial_position):
        current_position = initial_position
        total_seek_time = 0

        for track in self.sequence:
            seek_time = abs(track - current_position)
            total_seek_time += seek_time
            current_position = track

        return total_seek_time

    def sstf(self, initial_position):
        current_position = initial_position
        total_seek_time = 0
        sequence = self.sequence.copy()

        while sequence:
            nearest_track = min(
                sequence, key=lambda track: abs(track - current_position))
            seek_time = abs(nearest_track - current_position)
            total_seek_time += seek_time
            current_position = nearest_track
            sequence.remove(nearest_track)

        return total_seek_time


    def scan(self, initial_position, direction):
        current_position = initial_position
        total_seek_time = 0
        sequence = self.sequence.copy()

        sequence.append(initial_position)
        sequence.sort()

        if direction == "left":
            index = sequence.index(initial_position)
            left_sequence = sequence[:index]
            right_sequence = sequence[index + 1:]
        else:
            index = sequence.index(initial_position)
            left_sequence = sequence[:index + 1]
            right_sequence = sequence[index:]

        left_sequence.reverse()

        total_seek_time += abs(left_sequence[0] - current_position)
        total_seek_time += abs(right_sequence[-1] - left_sequence[0])

        return total_seek_time


def handle_submit():
    sequence_input = sequence_entry.get()
    initial_position = int(initial_position_entry.get())
    direction = direction_var.get()

    try:
        sequence = list(map(int, sequence_input.split(",")))
        scheduler = DiskScheduler(sequence)

        fcfs_seek_time = scheduler.fcfs(initial_position)
        sstf_seek_time = scheduler.sstf(initial_position)
        scan_seek_time = scheduler.scan(initial_position, direction)

        fcfs_result_label.config(text=f"FCFS: {fcfs_seek_time}")
        sstf_result_label.config(text=f"SSTF: {sstf_seek_time}")
        scan_result_label.config(text=f"SCAN: {scan_seek_time}")

    except ValueError:
        messagebox.showerror(
            "Invalid Input", "Please enter a valid sequence of track numbers (comma-separated).")


# Create GUI
window = tk.Tk()
window.title("Disk Scheduling Simulator")

# Sequence input frame
sequence_frame = tk.LabelFrame(window, text="Sequence")
sequence_frame.pack(padx=10, pady=10)

sequence_label = tk.Label(
    sequence_frame, text="Track Sequence (comma-separated):")
sequence_label.grid(row=0, column=0)
sequence_entry = tk.Entry(sequence_frame)
sequence_entry.grid(row=0, column=1)

# Initial position input frame
initial_position_frame = tk.LabelFrame(window, text="Initial Position")
initial_position_frame.pack(padx=10, pady=10)

initial_position_label = tk.Label(
    initial_position_frame, text="Initial Position:")
initial_position_label.grid(row=0, column=0)
initial_position_entry = tk.Entry(initial_position_frame)
initial_position_entry.grid(row=0, column=1)

# Direction input frame
direction_frame = tk.LabelFrame(window, text="Direction")
direction_frame.pack(padx=10, pady=10)

direction_var = tk.StringVar(value="left")

left_radio = tk.Radiobutton(
    direction_frame, text="Left", variable=direction_var, value="left")
left_radio.grid(row=0, column=0)

right_radio = tk.Radiobutton(
    direction_frame, text="Right", variable=direction_var, value="right")
right_radio.grid(row=0, column=1)

# Submit button
submit_button = tk.Button(window, text="Calculate", command=handle_submit)
submit_button.pack(pady=10)

# Result labels
result_frame = tk.LabelFrame(window, text="Results")
result_frame.pack(padx=10, pady=10)

fcfs_result_label = tk.Label(result_frame, text="FCFS: ")
fcfs_result_label.grid(row=0, column=0)

sstf_result_label = tk.Label(result_frame, text="SSTF: ")
sstf_result_label.grid(row=1, column=0)

scan_result_label = tk.Label(result_frame, text="SCAN: ")
scan_result_label.grid(row=2, column=0)

window.mainloop()
