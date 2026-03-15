import os
import logging
import tkinter as tk
from tkinter import messagebox, ttk
from ver import first  
from senti import second


def process_video():
    try:
        video_path = entry.get().strip()
        if not video_path:
            messagebox.showerror("Error", "Please enter a video path")
            return

        if not os.path.exists(video_path):
            messagebox.showerror("Error", "Video file not found")
            return

        # Show processing message
        status_label.config(text="Processing video... Please wait.")
        root.update()

        # Process video and get transcription
        transcription = first(video_path)
        if transcription.startswith("Error"):
            messagebox.showerror("Error", transcription)
            status_label.config(text="Ready")
            return

        # Analyze sentiment
        sentiment, score, explanation = second()
        if sentiment.startswith("Error"):
            messagebox.showerror("Error", sentiment)
            status_label.config(text="Ready")
            return

        # Log sentiment analysis results
        logging.info("Sentiment Analysis Results:")
        logging.info(f"Overall Sentiment: {sentiment}")
        logging.info(f"Compound Score: {score:.3f}")

        # Show results window
        # --- Updated Results Window (Centered, No Scrollbar) ---
        result_window = tk.Toplevel(root)
        result_window.title("Analysis Results")
        result_window.geometry("800x700")

        # Window behavior
        result_window.attributes('-topmost', True)
        result_window.focus_force()

        # Main container that fills the window and centers content
        # Using a frame with padding to act as the central wrapper
        main_frame = ttk.Frame(result_window, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # 1. Transcription Section
        ttk.Label(main_frame, text="Video Transcription:",
                  style="Heading.TLabel").pack(pady=(10, 5), anchor="center")

        transcription_text = tk.Text(main_frame, wrap=tk.WORD, height=8, width=70,
                                     font=("Helvetica", 10))
        transcription_text.pack(pady=5, padx=10)
        transcription_text.insert("1.0", transcription)
        transcription_text.config(state=tk.DISABLED)

        # 2. Overall Sentiment Section
        ttk.Label(main_frame, text="Overall Sentiment:",
                  style="Heading.TLabel").pack(pady=(10, 5), anchor="center")

        sentiment_display = ttk.Label(main_frame,
                                      text=f"{sentiment}\n(Compound Score: {score:.3f})",
                                      font=("Helvetica", 11, "bold"), justify="center")
        sentiment_display.pack(pady=5, anchor="center")

        # 3. Detailed Sentiment Analysis section
        ttk.Label(main_frame, text="Detailed Analysis:",
                  style="Heading.TLabel").pack(pady=(20, 5), anchor="center")

        explanation_text = tk.Text(main_frame, wrap=tk.WORD, height=12, width=70,
                                   font=("Helvetica", 10), bg="#f9f9f9")
        explanation_text.pack(pady=5, padx=10)
        explanation_text.insert("1.0", explanation)
        explanation_text.config(state=tk.DISABLED)

        # 4. Close button
        close_button = ttk.Button(main_frame, text="Close",
                                  command=result_window.destroy, style="Big.TButton")
        close_button.pack(pady=10, anchor="center")

        # Center the window on the screen
        result_window.update_idletasks()
        width = result_window.winfo_width()
        height = result_window.winfo_height()
        x = (result_window.winfo_screenwidth() // 2) - (width // 2)
        y = (result_window.winfo_screenheight() // 2) - (height // 2)
        result_window.geometry(f'{width}x{height}+{x}+{y}')

        status_label.config(text="Ready")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")
        status_label.config(text="Ready")


# --- UI Initialization ---
root = tk.Tk()
root.title("Video Sentiment Analyzer")
root.geometry("700x300")

# Styles
style = ttk.Style()
style.configure("Heading.TLabel", font=("Helvetica", 14, "bold"))
style.configure("Status.TLabel", font=("Helvetica", 10), padding=5)
style.configure("Big.TButton", font=("Helvetica", 10, "bold"), padding=10)

# Main layout container
main_container = ttk.Frame(root, padding="20")
main_container.pack(fill=tk.BOTH, expand=True)

ttk.Label(main_container, text="Video Sentiment Analyzer",style="Heading.TLabel").pack(pady=10)
ttk.Label(main_container, text="Enter the path to your video file:").pack()

entry = ttk.Entry(main_container, font=("Helvetica", 12))
entry.pack(pady=15, padx=20, fill=tk.X)

ttk.Button(main_container, text="Process Video",command=process_video, style="Big.TButton").pack(pady=10)

# Status bar area
status_frame = ttk.Frame(main_container)
status_frame.pack(fill=tk.X, pady=10)

status_label = ttk.Label(status_frame, text="Ready",style="Status.TLabel", anchor="center")
status_label.pack(expand=True, fill=tk.X)

if __name__ == "__main__":
    root.mainloop()
