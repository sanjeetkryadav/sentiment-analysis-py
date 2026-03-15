import os
import logging
import tkinter as tk
from tkinter import messagebox, ttk
from ver import first
from senti import second

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')


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
        result_window = tk.Toplevel(root)
        result_window.title("Analysis Results")
        result_window.geometry("800x610")

        # Window behavior
        result_window.attributes('-topmost', True)
        result_window.focus_force()

        # Create a frame with scrollbar
        main_frame = ttk.Frame(result_window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        canvas = tk.Canvas(main_frame)
        scrollbar = ttk.Scrollbar(
            main_frame, orient=tk.VERTICAL, command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Transcription section
        ttk.Label(scrollable_frame, text="Video Transcription:",
                  style="Heading.TLabel").pack(pady=10)
        transcription_text = tk.Text(
            scrollable_frame, wrap=tk.WORD, height=10, width=80)
        transcription_text.pack(padx=10, fill=tk.X)
        transcription_text.insert("1.0", transcription)
        transcription_text.config(state=tk.DISABLED)

        # Overall Sentiment section
        ttk.Label(scrollable_frame, text="Overall Sentiment:",
                  style="Heading.TLabel").pack(pady=10)
        ttk.Label(scrollable_frame,
                  text=f"{sentiment} (Compound Score: {score:.3f})").pack()

        # Detailed Sentiment Analysis section
        ttk.Label(scrollable_frame, text="Detailed Analysis:",
                  style="Heading.TLabel").pack(pady=10)
        explanation_text = tk.Text(
            scrollable_frame, wrap=tk.WORD, height=12, width=80)
        explanation_text.pack(padx=10, fill=tk.X)
        explanation_text.insert("1.0", explanation)
        explanation_text.config(state=tk.DISABLED)

        # Layout scrollbar and canvas
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Close button
        close_button = ttk.Button(
            result_window, text="Close", command=result_window.destroy)
        close_button.pack(pady=10)

        # Center the window
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

ttk.Label(main_container, text="Video Sentiment Analyzer",
          style="Heading.TLabel").pack(pady=10)
ttk.Label(main_container, text="Enter the path to your video file:").pack()

entry = ttk.Entry(main_container, font=("Helvetica", 12))
entry.pack(pady=15, padx=20, fill=tk.X)

ttk.Button(main_container, text="Process Video",
           command=process_video, style="Big.TButton").pack(pady=10)

# Status bar area
status_frame = ttk.Frame(main_container)
status_frame.pack(fill=tk.X, pady=10)

status_label = ttk.Label(status_frame, text="Ready",
                         style="Status.TLabel", anchor="center")
status_label.pack(expand=True, fill=tk.X)

if __name__ == "__main__":
    root.mainloop()
