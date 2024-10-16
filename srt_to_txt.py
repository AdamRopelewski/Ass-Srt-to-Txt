import os
import re
import tkinter as tk
from tkinterdnd2 import TkinterDnD, DND_FILES
from tkinter import messagebox
import subprocess


def srt_to_txt(srt_file):
    # Read the content of the SRT file
    with open(srt_file, "r", encoding="utf-8") as f:
        content = f.read()

    # Remove timecodes and sequence numbers
    text = re.sub(
        r"\d+\n\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}\n", "", content
    )
    text = re.sub(r"\n\d+\n", "\n", text)

    # Remove font tags and any other HTML-like tags (e.g., <font>, <i>, etc.)
    text = re.sub(r"<.*?>", "", text)

    # Remove empty lines (including multiple newlines in a row)
    # Replaces multiple new lines with a single one and trims leading/trailing new lines
    text = re.sub(r"\n+", "\n", text).strip()

    # Define the output .txt file path
    txt_file = os.path.splitext(srt_file)[0] + ".txt"

    # Write the cleaned text to the .txt file
    with open(txt_file, "w", encoding="utf-8") as f:
        f.write(text)

    return txt_file


def ass_to_srt(ass_file):
    srt_file = os.path.splitext(ass_file)[0] + ".srt"
    command = ["ffmpeg", "-i", ass_file, "-c:s", "srt", srt_file]
    try:
        subprocess.run(command, check=True)
        return srt_file
    except subprocess.CalledProcessError as e:
        print(f"Error converting ASS to SRT: {e}")
        return None


def on_drop(event):
    # Get the file path from the drag-and-drop event
    file = event.data.strip("{}")  # tkinterdnd2 may wrap path in {}
    if file.endswith(".ass"):
        file = ass_to_srt(file)

    if not file.endswith(".srt"):
        messagebox.showerror("Invalid file", "Please drop an SRT file.")
        return

    try:
        # Convert SRT to TXT
        txt_file = srt_to_txt(file)
        messagebox.showinfo("Success", f"TXT file saved at: {txt_file}")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")


# Initialize TkinterDnD window
root = TkinterDnD.Tk()
root.title("SRT or ASS to TXT Converter")
root.geometry("280x150")
root.resizable(False, False)  # Prevent resizing the window


# Label to instruct the user
label = tk.Label(
    root,
    text="Drag and drop your .srt or .ass file here",
    width=40,
    height=10,
    bg="black",
    fg="white",
)
label.pack(padx=0, pady=0)

# Enable drag-and-drop functionality
label.drop_target_register(DND_FILES)
label.dnd_bind("<<Drop>>", on_drop)

# Run the GUI application
root.mainloop()
