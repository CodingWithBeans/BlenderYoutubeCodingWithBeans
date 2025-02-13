import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import cv2
import numpy as np
from PIL import Image
import time
import os
import BackEnd 

# Global variables to store selected file and frames list
selected_video_path = None
ascii_frames = []

def select_file(preview_widget, fileTypeMp4):
    """Function to determine if the file type is a video or image."""
    if fileTypeMp4.get():  # Use .get() to check BooleanVar value
        select_Mp4(preview_widget)
    else:
        select_image(preview_widget)

def select_Mp4(preview_widget):
    """Function to select a Mp4 file."""
    global selected_video_path, ascii_frames
    check_frame_empty(preview_widget, ascii_frames)
    selected_video_path = filedialog.askopenfilename(filetypes=[("Video Files", "*.mp4;*.avi;*.mov")])
    if selected_video_path:
        messagebox.showinfo("Video Selected", f"Selected file: {selected_video_path}")
        preview_widget.delete("1.0", tk.END)  # Clear preview widget
        preview_widget.insert(tk.END, "Video selected. Ready to generate ASCII art!")
    else:
        messagebox.showwarning("No File Selected", "Please select a video file.")

def select_image(preview_widget):
    """Function to select an image file."""
    global selected_file_path
    selected_file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.gif")])
    if selected_file_path:
        messagebox.showinfo("Image Selected", f"Selected file: {selected_file_path}")
        preview_widget.delete("1.0", tk.END)  # Clear preview widget
        preview_widget.insert(tk.END, "Image selected. Ready to generate ASCII art!")
    else:
        messagebox.showwarning("No File Selected", "Please select an image file.")

def generate_ascii_for_video(preview_widget, block_size, line_detection, progress_bar):
    """Function to generate ASCII art for each frame in the video."""
    global selected_video_path, ascii_frames

    if selected_video_path:
        try:
            # Open the video file
            video_capture = cv2.VideoCapture(selected_video_path)
            if not video_capture.isOpened():
                raise RuntimeError(f"Failed to open video file: {selected_video_path}")

            # Clear the frames list
            ascii_frames = []
            
            # Get the total number of frames in the video
            total_frames = int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT))
            progress_bar['maximum'] = total_frames  # Set the maximum value of progress bar
            progress_bar['value'] = 0  # Start with the value at 0

            while video_capture.isOpened():
                ret, frame = video_capture.read()
                if not ret:
                    break  # End of video

                # Convert frame to ASCII art
                frame_ascii = process_frame_to_ascii(frame, block_size, line_detection)
                ascii_frames.append(frame_ascii)

                # Update the progress bar
                progress_bar['value'] += 1
                progress_bar.update()  # Update progress bar

            # Display the first frame in the preview widget
            preview_widget.delete("1.0", tk.END)  # Clear previous content
            preview_widget.insert(tk.END, ascii_frames[0])

            # Close the video capture
            video_capture.release()

        except Exception as e:
            messagebox.showerror("Error", f"Failed to process video: {e}")
            print("Error", f"Failed to process video: {e}")
    else:
        messagebox.showwarning("No File Selected", "Please select a video file first.")
        print("No File Selected", "Please select a video file first.")

def process_frame_to_ascii(frame, block_size, line_detection):
    """Convert a video frame to ASCII art."""
    if line_detection:
        frame = BackEnd.edge_detection(frame)  # Apply edge detection if required

    # Convert the frame to grayscale if it's not already
    if len(frame.shape) == 3:  # Check if frame has 3 channels (BGR/RGB)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Calculate new dimensions based on the block size
    height, width = frame.shape
    new_width = width // (block_size * 3)
    new_height = height // (block_size * 6)

    # Resize the frame
    resized_frame = cv2.resize(frame, (new_width, new_height))

    # Generate ASCII art from the frame
    ascii_art = ""
    for y in range(new_height):
        for x in range(new_width):
            brightness = resized_frame[y, x]
            char_index = int((brightness / 255) * (len(BackEnd.ascii_characters_by_density) - 1))
            ascii_art += BackEnd.ascii_characters_by_density[char_index]
        ascii_art += "\n"

    return ascii_art

def generate_art(preview_widget, block_size, line_detection):
    """Function to generate ASCII art."""
    global selected_file_path
    if selected_file_path:
        try:
            # Generate ASCII art using backend
            ascii_art = BackEnd.get_ascii_art(selected_file_path, block_size, line_detection)

            # Display ASCII art in the preview widget
            preview_widget.delete("1.0", tk.END)  # Clear previous content
            preview_widget.insert(tk.END, ascii_art)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to process file: {e}")
    else:
        messagebox.showwarning("No File Selected", "Please select an image file first.")

def update_select_button_text(button, fileTypeMp4):
    """Update the button text based on the fileTypeMp4 value."""
    button.config(
        text="Select Video" if fileTypeMp4.get() else "Select Image"
    )

def update_generate_button_text(button, fileTypeMp4):
    """Update the button text based on the fileTypeMp4 value."""
    button.config(
        text="Generate Video" if fileTypeMp4.get() else "Generate Image"
    )

def play_video(preview_widget):
    """Function to play the generated ASCII art as a video."""
    global ascii_frames

    if not ascii_frames:
        messagebox.showwarning("No Frames", "No frames to display. Please generate ASCII art first.")
        return

    try:
        # Play each frame with a delay to simulate video
        for frame in ascii_frames:
            preview_widget.delete("1.0", tk.END)  # Clear previous content
            preview_widget.insert(tk.END, frame)
            preview_widget.update()  # Update the widget
            time.sleep(0.03)  # 10 frames per second (adjust as needed)

    except Exception as e:
        messagebox.showerror("Error", f"Failed to play video: {e}")

def save_video(ascii_frames):
    """Function to save ascii video"""
    ascii_art = ascii_frames
    if len(ascii_frames) == 0:
        messagebox.showinfo("Save", "Ascii_frames is empty")
        return
    
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])

    if not file_path:
        messagebox.showinfo("")


def save_art(preview_widget):
    """Function to save the generated ASCII art to a file."""
    # Get the content of the preview widget
    ascii_art = preview_widget.get("1.0", tk.END).strip()
    
    if ascii_art:  # Ensure there is ASCII art to save
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
        if file_path:
            try:
                # Save ASCII art to the file
                BackEnd.save_ascii_art(ascii_art, file_path)
                messagebox.showinfo("Save", "ASCII Art saved successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save ASCII art: {e}")
        else:
            messagebox.showwarning("Save Cancelled", "Save operation was cancelled.")
    else:
        messagebox.showwarning("No Art to Save", "There is no ASCII art to save. Please generate art first.")

def check_frame_empty(preview_widget, ascii_frames):
    if len(ascii_frames) == 0:
        pass
    else:
        ascii_frames = []

    preview_widget.delete("1.0", tk.END)

def create_main():
    """Function to create the main window."""
    main_window = tk.Tk()
    main_window.title("Settings for your generation!")
    main_window.geometry("800x600")
    main_window.configure(bg="#f0f0f0")

    # Variables
    block_size_var = tk.IntVar(value=9)
    line_detection = tk.BooleanVar()
    fileTypeMp4 = tk.BooleanVar()
    current_font_size = tk.IntVar(value=12)  # Initial font size

    # Top frame for settings
    settings_frame = tk.Frame(main_window)
    settings_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

    # Button to select a video
    select_file_button = tk.Button(
        settings_frame,
        text="Select Image",
        font=("Rockabilly", 10),
        command=lambda: select_file(preview_widget, fileTypeMp4),
        width=20,
        height=2
    )

    fileTypeMp4.trace_add("write", lambda *args: update_select_button_text(select_file_button, fileTypeMp4))

    select_file_button.grid(row=0, column=0, padx=5, pady=5)
    
    def handle_generate(preview_widget, fileTypeMp4, block_size_var, line_detection, progress_bar):
        """Execute the appropriate generate function based on fileTypeMp4 value."""
        if fileTypeMp4.get():
            generate_ascii_for_video(
                preview_widget,
                block_size_var.get(),
                line_detection.get(),
                progress_bar
            )
        else:
            generate_art(
                preview_widget,
                block_size_var.get(),
                line_detection.get()
            )

    # Button to generate ASCII art
    generate_art_button = tk.Button(
        settings_frame,
        text="Generate ASCII",
        font=("Rockabilly", 10),
        command=lambda: handle_generate(
            preview_widget,
            fileTypeMp4,
            block_size_var,
            line_detection,
            progress_bar
        ),
        width=20,
        height=2
    )

    # Update button text dynamically based on fileTypeMp4
    fileTypeMp4.trace_add("write", lambda *args: update_generate_button_text(generate_art_button, fileTypeMp4))

    generate_art_button.grid(row=0, column=1, padx=5, pady=5)



    # Block size scale
    block_size_scale = tk.Scale(
        settings_frame,
        from_=1,
        to_=20,
        orient=tk.HORIZONTAL,
        variable=block_size_var,
        label="Block Size (Pixels per Character)"
    )
    block_size_scale.grid(row=0, column=3, padx=5, pady=5)

    # Line detection checkbox
    LineDetection_box = tk.Checkbutton(
        settings_frame,
        text='Line Detection (Edge Detection)',
        variable=line_detection,
        onvalue=True,
        offvalue=False,
    )
    LineDetection_box.grid(row=0, column=5, columnspan=2, pady=5)

        # Line detection checkbox
    mp4jpeg_box = tk.Checkbutton(
        settings_frame,
        text='Video?',
        variable=fileTypeMp4,
        onvalue=True,
        offvalue=False,
    )
    mp4jpeg_box.grid(row=0, column=7, columnspan=2, pady=5)
    
    # Frame for preview widget
    preview_frame = tk.Frame(main_window)
    preview_frame.pack(side=tk.BOTTOM, expand=True, fill=tk.BOTH, padx=10, pady=10)

    # Preview widget for displaying ASCII art frames
    preview_widget = tk.Text(
        preview_frame,
        wrap=tk.WORD,
        font=("Courier", current_font_size.get()),
        bg="#ffffff",
        fg="#000000"
    )
    preview_widget.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

    # Scrollbar for preview widget
    scrollbar = tk.Scrollbar(preview_frame, command=preview_widget.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    preview_widget.config(yscrollcommand=scrollbar.set)

    # Function to handle zoom (mouse wheel with Shift) or scrolling
    def mouse_wheel(event):
        """Zoom the ASCII art in and out with Shift, or scroll normally."""
        if event.state & 0x1:  # Shift key held
            # Zoom in or out
            delta = 1 if event.delta > 0 else -1
            new_size = current_font_size.get() + delta
            if 1 <= new_size <= 30:
                current_font_size.set(new_size)
                preview_widget.config(font=("Courier", current_font_size.get()))
        else:
            # Scroll vertically
            preview_widget.yview_scroll(-1 * (event.delta // 120), "units")

    # Function to handle key-based zoom
    def key_zoom(event):
        """Zoom in or out using - and = keys."""
        delta = 1 if event.char == '=' else -1 if event.char == '-' else 0
        if delta:
            new_size = current_font_size.get() + delta
            if 1 <= new_size <= 30:
                current_font_size.set(new_size)
                preview_widget.config(font=("Courier", current_font_size.get()))

    # Bind mouse wheel to the preview widget
    preview_widget.bind("<MouseWheel>", mouse_wheel)

    # Bind keyboard keys for zooming
    preview_widget.bind("<KeyPress-=>", key_zoom)  # Increase font size
    preview_widget.bind("<KeyPress-minus>", key_zoom)  # Decrease font size

    # Create a frame to hold the buttons
    button_frame = tk.Frame(main_window)
    button_frame.pack(pady=10)
    

    def update_play_button(parent_frame, preview_widget, fileTypeMp4):
        """Show or hide the Play button based on fileTypeMp4 value."""
        for widget in parent_frame.winfo_children():
            if getattr(widget, "is_play_button", False):
                widget.destroy()  # Remove existing play button if it exists

        if fileTypeMp4.get():
            # Create the Play button for videos
            play_button = tk.Button(
                parent_frame,
                text="Play ASCII Art Video",
                font=("Rockabilly", 10),
                command=lambda: play_video(preview_widget),
                width=20,
                height=2
            )
            play_button.is_play_button = True  # Tag to identify this button later
            play_button.pack(side="left", padx=5)

    fileTypeMp4.trace_add("write", lambda *args: update_play_button(button_frame, preview_widget, fileTypeMp4))

    update_play_button(button_frame, preview_widget, fileTypeMp4)


    # Save ASCII art button
    save_button = tk.Button(
        button_frame,
        text="Save ASCII Art",
        font=("Rockabilly", 10),
        command=lambda: save_art(preview_widget),
        width=20,
        height=2
    )
    save_button.pack(side="left", padx=5)

        # Progress bar for video processing
    progress_bar = ttk.Progressbar(
        button_frame,
        orient=tk.HORIZONTAL,
        length=200,
        mode="determinate"
    )
    progress_bar.pack(side="right", padx=5)


    return main_window

# Create and display the main window
main_window = create_main()
main_window.mainloop()
