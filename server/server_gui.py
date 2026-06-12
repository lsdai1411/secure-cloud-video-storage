import tkinter as tk
import subprocess

from tkinter import StringVar


server_process = None


def start_server():

    global server_process

    if server_process is None:

        server_process = subprocess.Popen(
            ["python", "server/cloud_server.py"]
        )

        status_label.config(
            text="Server Running"
        )

def stop_server():

    global server_process

    if server_process is not None:

        server_process.terminate()

        server_process = None

        status_label.config(
            text="Server Stopped"
        )

def update_network_mode():

    with open(
        "server/network_mode.txt",
        "w"
    ) as f:

        f.write(
            network_mode.get()
        )


def refresh_logs():

    try:

        with open(
            "logs/system.log",
            "r",
            encoding="utf-8"
        ) as f:

            logs = f.readlines()

        log_box.delete(
            "1.0",
            tk.END
        )

        for line in logs[-10:]:

            log_box.insert(
                tk.END,
                line
            )

    except Exception as e:

        print(
            "LOG ERROR:",
            e
        )

    window.after(
        2000,
        refresh_logs
    )


window = tk.Tk()

window.title(
    "Secure Cloud Server"
)

window.geometry(
    "600x450"
)

title_label = tk.Label(
    window,
    text="Secure Cloud Server",
    font=("Arial", 14, "bold")
)

title_label.pack(
    pady=10
)

start_button = tk.Button(
    window,
    text="Start Server",
    width=20,
    height=2,
    command=start_server
)

start_button.pack(
    pady=10
)

stop_button = tk.Button(
    window,
    text="Stop Server",
    width=20,
    height=2,
    command=stop_server
)

stop_button.pack(
    pady=5
)

status_label = tk.Label(
    window,
    text="Server Stopped"
)

status_label.pack(
    pady=10
)

network_title = tk.Label(
    window,
    text="Network Mode"
)

network_title.pack(
    pady=(10, 0)
)

network_mode = StringVar()

network_mode.set(
    "NORMAL"
)

normal_radio = tk.Radiobutton(
    window,
    text="NORMAL",
    variable=network_mode,
    value="NORMAL",
    command=update_network_mode
)

normal_radio.pack()

packet_radio = tk.Radiobutton(
    window,
    text="PACKET LOSS",
    variable=network_mode,
    value="PACKET_LOSS",
    command=update_network_mode
)

packet_radio.pack()

log_title = tk.Label(
    window,
    text="Recent Activity"
)

log_title.pack()

log_box = tk.Text(
    window,
    height=10,
    width=70
)

log_box.pack(
    pady=5
)

update_network_mode()

refresh_logs()

window.mainloop()