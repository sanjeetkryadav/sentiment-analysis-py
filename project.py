from tkinter import *
from tkinter import messagebox
from tkinter.ttk import *
from ver import first
from senti import second
import os
import logging

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
            
        # Analyze sentiment -
        sentiment, score, explanation = second()
        if sentiment.startswith("Error"):
            messagebox.showerror("Error", sentiment)
            status_label.config(text="Ready")
            return
            
        # Log sentiment analysis results
        logging.info("\nSentiment Analysis Results:")
        logging.info(f"Overall Sentiment: {sentiment}")
        logging.info(f"Compound Score: {score:.3f}")
        logging.info(f"Detailed Analysis:\n{explanation}")
            
        # Show results
        result_window = Toplevel(root)
        result_window.title("Analysis Results")
        result_window.geometry("800x610")
        
        # Make window stay on top but allow minimizing
        result_window.attributes('-topmost', True)
        result_window.focus_force()
        
        # Create a frame with scrollbar
        main_frame = Frame(result_window)
        main_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)
        
        canvas = Canvas(main_frame)
        scrollbar = Scrollbar(main_frame, orient=VERTICAL, command=canvas.yview)
        scrollable_frame = Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Transcription
        Label(scrollable_frame, text="Video Transcription:", style="Heading.TLabel").pack(pady=10)
        transcription_text = Text(scrollable_frame, wrap=WORD, height=10, width=80)
        transcription_text.pack(padx=10, fill=X)
        transcription_text.insert("1.0", transcription)
        transcription_text.config(state=DISABLED)
        
        # Overall Sentiment
        Label(scrollable_frame, text="Overall Sentiment:", style="Heading.TLabel").pack(pady=10)
        Label(scrollable_frame, text=f"{sentiment} (Compound Score: {score:.3f})").pack()
        
        # Detailed Sentiment Analysis
        Label(scrollable_frame, text="Detailed Analysis:", style="Heading.TLabel").pack(pady=10)
        explanation_text = Text(scrollable_frame, wrap=WORD, height=12, width=80)
        explanation_text.pack(padx=10, fill=X)
        explanation_text.insert("1.0", explanation)
        explanation_text.config(state=DISABLED)
        
        # Pack scrollbar and canvas
        scrollbar.pack(side=RIGHT, fill=Y)
        canvas.pack(side=LEFT, fill=BOTH, expand=True)
        
        # Add close button
        close_button = Button(result_window, text="Close", command=result_window.destroy)
        close_button.pack(pady=10)
        
        # Center the window on screen
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

# Create main window
root = Tk()
root.title("Video Sentiment Analyzer Window")
root.geometry("700x300")  

# Style
style = Style()
style.configure("Heading.TLabel", font=("Helvetica", 14, "bold"))
style.configure("Status.TLabel", font=("Helvetica", 10), padding=5, anchor="center")
style.configure("Big.TButton", font=("Helvetica", 10, "bold"), padding=10)

# Main content
frame = Frame(root, padding="20")
frame.pack(fill=BOTH, expand=True)

Label(frame, text="Video Sentiment Analyzer", style="Heading.TLabel").pack(pady=10)
Label(frame, text="Enter the path to your video file:").pack()

entry = Text(frame, width=60, height=1, font=("Helvetica", 12))
entry.pack(pady=15, padx=20, fill=X)

Button(frame, text="Process Video", command=process_video, style="Big.TButton").pack(pady=10)

# Create a container frame for the status label
status_frame = Frame(frame)
status_frame.pack(fill=X, pady=10)

status_label = Label(status_frame, text="Ready", style="Status.TLabel", anchor="center")
status_label.pack(expand=True, fill=X)

root.mainloop()
