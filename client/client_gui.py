import tkinter as tk
from tkinter import filedialog
import subprocess

selected_file = ""


def browse_file():

    global selected_file

    file_path = filedialog.askopenfilename(
        filetypes=[
            (
                "Video Files",
                "*.mp4 *.avi *.mov *.mkv"
            )
        ]
    )

    if file_path:

        selected_file = file_path

        file_label.config(
            text=file_path
        )


def upload_video():

    global selected_file

    if selected_file == "":

        status_label.config(
            text="Please select a file"
        )

        return

    subprocess.Popen(
        [
            "python",
            "client/upload_client.py",
            selected_file
        ]
    )

    status_label.config(
        text="Upload Started"
    )


def download_video():

    subprocess.Popen(
        [
            "python",
            "client/download_client.py"
        ]
    )

    status_label.config(
        text="Download Started"
    )


window = tk.Tk()

window.title(
    "Secure Cloud Client"
)

window.geometry(
    "600x300"
)

title_label = tk.Label(
    window,
    text="Secure Cloud Client",
    font=("Arial", 14, "bold")
)

title_label.pack(
    pady=10
)

file_label = tk.Label(
    window,
    text="No file selected",
    wraplength=500
)

file_label.pack(
    pady=10
)

browse_button = tk.Button(
    window,
    text="Browse",
    width=20,
    command=browse_file
)

browse_button.pack(
    pady=5
)

upload_button = tk.Button(
    window,
    text="Upload",
    width=20,
    command=upload_video
)

upload_button.pack(
    pady=5
)

download_button = tk.Button(
    window,
    text="Download",
    width=20,
    command=download_video
)

download_button.pack(
    pady=5
)

status_label = tk.Label(
    window,
    text="Ready"
)

status_label.pack(
    pady=10
)

window.mainloop()