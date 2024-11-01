import tkinter as tk
from tkinter import ttk

class AntiDoroTimer:
    def __init__(self, root):
        self.root = root
        self.root.title("AntiDoro Timer")
        self.root.geometry("380x280")
        self.font = ("Helvetica", 13)
        self.style = ttk.Style(self.root)
        self.style.configure("TButton", font=self.font, padding=(5, 3), width=8)
        self.style.configure("TLabel", font=self.font)
        self.selected_button = None
        self.session_time = 0
        self.time_remaining = 0
        self.current_phase = ""
        self.running = False
        self.setup_initial_screen()

    def setup_initial_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.selected_button = None
        frame = tk.Frame(self.root)
        frame.place(relx=0.5, rely=0.4, anchor='center')
        self.session_label = tk.Label(frame, text="Select session time: 0 mins", font=self.font)
        self.session_label.grid(row=0, column=0, columnspan=3, padx=5, pady=(0, 10))
        self.three_hr_button = ttk.Button(frame, text="3h/50", command=lambda: self.set_session_time(50, self.three_hr_button))
        self.three_hr_button.grid(row=1, column=0, padx=3)
        self.two_hr_button = ttk.Button(frame, text="2h/40", command=lambda: self.set_session_time(40, self.two_hr_button))
        self.two_hr_button.grid(row=1, column=1, padx=3)
        self.one_hr_button = ttk.Button(frame, text="1h/30", command=lambda: self.set_session_time(30, self.one_hr_button))
        self.one_hr_button.grid(row=1, column=2, padx=3)
        self.start_button = ttk.Button(self.root, text="Start", command=self.begin_sequence)
        self.start_button.place(relx=0.5, rely=0.65, anchor='center')

    def set_session_time(self, initial_session_time, button):
        self.session_time = initial_session_time
        self.update_total_time_display()
        if self.selected_button:
            self.selected_button.state(["!pressed"])
        button.state(["pressed"])
        self.selected_button = button

    def update_total_time_display(self):
        if self.session_time == 50:
            total_time = sum([50, 40, 30, 20, 10]) + 4 * 10
        elif self.session_time == 40:
            total_time = sum([40, 30, 20, 10]) + 3 * 10
        elif self.session_time == 30:
            total_time = sum([30, 20, 10]) + 2 * 10
        else:
            total_time = 0
        self.session_label.config(text=f"Select session time: {total_time} mins")

    def begin_sequence(self):
        self.root.geometry("180x150")
        if self.session_time == 50:
            self.work_times = [50, 40, 30, 20, 10]
        elif self.session_time == 40:
            self.work_times = [40, 30, 20, 10]
        elif self.session_time == 30:
            self.work_times = [30, 20, 10]
        self.break_time = 10
        self.current_phase = "work"
        self.current_index = 0
        self.running = True
        self.start_phase()

    def start_phase(self):
        if not self.running:
            return
        if self.current_phase == "work":
            if self.current_index < len(self.work_times):
                self.time_remaining = self.work_times[self.current_index] * 60
                self.update_running_screen("Work")
            else:
                self.end_timer()
                return
        elif self.current_phase == "break":
            self.time_remaining = self.break_time * 60
            self.update_running_screen("Break")
        self.update_timer()

    def update_running_screen(self, phase_text):
        if not hasattr(self, 'phase_label') or not self.phase_label.winfo_exists():
            for widget in self.root.winfo_children():
                widget.destroy()
            self.phase_label = tk.Label(self.root, text=f"{phase_text}: {self.format_time(self.time_remaining)}", font=self.font)
            self.phase_label.place(relx=0.5, rely=0.4, anchor='center')
            self.stop_button = ttk.Button(self.root, text="Stop", command=self.stop_timer)
            self.stop_button.place(relx=0.5, rely=0.7, anchor='center')
        else:
            self.phase_label.config(text=f"{phase_text}: {self.format_time(self.time_remaining)}")

    def update_timer(self):
        if not self.running:
            return
        if self.time_remaining > 0:
            self.phase_label.config(text=f"{self.current_phase.capitalize()}: {self.format_time(self.time_remaining)}")
            self.time_remaining -= 1
            self.root.after(1000, self.update_timer)
        else:
            if self.current_phase == "work":
                self.current_phase = "break"
            else:
                self.current_phase = "work"
                self.current_index += 1
            self.start_phase()

    def format_time(self, seconds):
        minutes = seconds // 60
        seconds = seconds % 60
        return f"{minutes:02}:{seconds:02}"

    def stop_timer(self):
        self.running = False
        self.setup_initial_screen()
        self.root.geometry("380x280")

    def end_timer(self):
        self.running = False
        for widget in self.root.winfo_children():
            widget.destroy()
        self.end_label = tk.Label(self.root, text="Session Complete!", font=self.font)
        self.end_label.place(relx=0.5, rely=0.4, anchor='center')
        self.reset_button = ttk.Button(self.root, text="Reset", command=self.setup_initial_screen)
        self.reset_button.place(relx=0.5, rely=0.7, anchor='center')

root = tk.Tk()
app = AntiDoroTimer(root)
root.mainloop()
