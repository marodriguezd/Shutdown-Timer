import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk
import os
import threading
import time


class ShutdownApp:
    def __init__(self, root):
        """
        Initializes the Shutdown Timer application.

        :param root: The root window for the application.
        """
        self.root = root
        self.root.title("Shutdown Timer")
        self.root.geometry("400x250")  # Adjusted to provide space for improved design

        # Calculate the center position
        window_width = 400
        window_height = 250
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        center_x = int((screen_width - window_width) / 2)
        center_y = int((screen_height - window_height) / 2)

        # Position the window in the center of the screen
        self.root.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")

        # Interface improvement using a style and theme
        self.style = ttk.Style()
        self.root.set_theme("equilux")  # You can change "equilux" to another theme if desired

        # Custom style configuration for Labels
        self.style.configure("White.TLabel", foreground="white")

        # Main container
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.pack(expand=True, fill=tk.BOTH)

        # Title
        self.title_label = ttk.Label(self.main_frame, text="Shutdown Timer", style="White.TLabel", font=('Arial', 16),
                                     anchor="center")
        self.title_label.pack(pady=(0, 20))

        # Time input field
        self.time_var = tk.StringVar()
        self.time_entry = ttk.Entry(self.main_frame, textvariable=self.time_var, font=('Arial', 12), width=15)
        self.time_entry.pack()

        self.time_label = ttk.Label(self.main_frame, text="Enter the time in minutes", style="White.TLabel",
                                    font=('Arial', 10))
        self.time_label.pack(pady=(5, 20))

        # Buttons
        self.buttons_frame = ttk.Frame(self.main_frame)
        self.buttons_frame.pack()

        self.start_button = ttk.Button(self.buttons_frame, text="Start", command=self.start_shutdown_timer)
        self.start_button.pack(side=tk.LEFT, padx=10)

        self.cancel_button = ttk.Button(self.buttons_frame, text="Cancel", command=self.cancel_shutdown)
        self.cancel_button.pack(side=tk.LEFT, padx=10)

        # Status Label
        self.status_label = ttk.Label(self.main_frame, text="", style="White.TLabel", font=('Arial', 12))
        self.status_label.pack(pady=(20, 0))

        self.shutdown_timer = None

    def start_shutdown_timer(self):
        """
        Starts the shutdown timer with the specified time in minutes.
        """
        try:
            time_in_minutes = float(self.time_var.get())
            self.status_label.config(text=f"Shutdown scheduled in {time_in_minutes} minutes.")
            self.shutdown_timer = threading.Thread(target=self.initiate_shutdown, args=(time_in_minutes,))
            self.shutdown_timer.start()
        except ValueError:
            self.status_label.config(text="Please, enter a valid time.")

    def initiate_shutdown(self, time_in_minutes):
        """
        Schedules the system shutdown after the specified time in minutes.

        :param time_in_minutes: Time in minutes after which the system will shut down.
        """
        seconds = int(time_in_minutes * 60)
        shutdown_command = f"shutdown /s /t {seconds}"
        os.system(shutdown_command)
        self.status_label.config(text=f"Shutdown scheduled in {time_in_minutes} minutes.")

    def cancel_shutdown(self):
        """
        Cancels the scheduled shutdown if it has been set.
        """
        os.system("shutdown /a")
        self.status_label.config(text="Shutdown cancelled.")


if __name__ == "__main__":
    root = ThemedTk(theme="equilux")  # We're using ThemedTk to apply themes
    app = ShutdownApp(root)
    root.mainloop()
