from moviepy.editor import VideoFileClip
import speech_recognition as sr
import os
import wave
import contextlib
import logging
from datetime import datetime
import time

# Set up logging here
def setup_logging():
    log_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "logs")
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = os.path.join(log_dir, f"transcript_{timestamp}.log")
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    return log_file

def get_audio_duration(audio_file):
    with contextlib.closing(wave.open(audio_file, 'r')) as f:
        frames = f.getnframes()
        rate = f.getframerate()
        duration = frames / float(rate)
        return duration

def transcribe_chunk(recognizer, audio, chunk_num, max_retries=3):
    for attempt in range(max_retries):
        try:
            # Adjust recognition parameters for better accuracy
            recognizer.dynamic_energy_threshold = True
            recognizer.energy_threshold = 4000  # Adjust this value based on your audio
            recognizer.pause_threshold = 0.8    # Reduce pause threshold
            
            text = recognizer.recognize_google(audio, language="en-US")
            if text.strip():  # Only return if we got actual text
                return text
            else:
                logging.warning(f"Empty transcription for chunk {chunk_num}, attempt {attempt + 1}")
        except sr.UnknownValueError:
            logging.warning(f"Could not understand audio in chunk {chunk_num}, attempt {attempt + 1}")
        except sr.RequestError as e:
            logging.error(f"Error in chunk {chunk_num}, attempt {attempt + 1}: {str(e)}")
            if attempt < max_retries - 1:
                time.sleep(2)  # Wait before retrying
                continue
            return None
        except Exception as e:
            logging.error(f"Unexpected error in chunk {chunk_num}, attempt {attempt + 1}: {str(e)}")
            if attempt < max_retries - 1:
                time.sleep(2)
                continue
            return None
    return None

def first(file_path):
    try:
        # Set up logging
        log_file = setup_logging()
        logging.info(f"Starting transcription for video: {file_path}")
        
        # Extract audio from video
        clip = VideoFileClip(file_path)
        audio_file = "theaudio.wav"
        clip.audio.write_audiofile(audio_file)
        logging.info(f"Audio extracted and saved as: {audio_file}")
        
        # Get the full path of the audio file
        AUDIO_FILE = os.path.join(os.path.dirname(os.path.realpath(__file__)), audio_file)
        
        # Initialize recognizer
        r = sr.Recognizer()
        
        # Calculate total duration
        total_duration = get_audio_duration(AUDIO_FILE)
        chunk_duration = 30  # Reduced chunk size to 30 seconds for better accuracy
        full_text = []
        
        logging.info(f"Total audio duration: {total_duration:.2f} seconds")
        logging.info(f"Processing in chunks of {chunk_duration} seconds")
        
        # Process audio in chunks
        with sr.AudioFile(AUDIO_FILE) as source:
            # Adjust for ambient noise at the start
            r.adjust_for_ambient_noise(source, duration=1)
            
            for i in range(0, int(total_duration), chunk_duration):
                chunk_start = i
                chunk_end = min(i + chunk_duration, int(total_duration))
                chunk_num = i // chunk_duration + 1
                logging.info(f"Processing chunk {chunk_num} ({chunk_start}-{chunk_end} seconds)")
                
                # Record the chunk
                audio = r.record(source, duration=chunk_duration)
                
                # Try to transcribe the chunk
                text = transcribe_chunk(r, audio, chunk_num)
                
                if text:
                    full_text.append(text)
                    logging.info(f"Chunk {chunk_num} transcription: {text}")
                else:
                    logging.warning(f"Failed to transcribe chunk {chunk_num} after all attempts")
                    full_text.append(f"[Chunk {chunk_num} transcription failed]")
                
                # Add a small delay between chunks to prevent API rate limiting
                time.sleep(1)
        
        # Combine all chunks
        final_text = " ".join(full_text)
        
        # Save to file
        input_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), "input.txt")
        with open(input_file, "w+", encoding='utf-8') as file:
            file.write(final_text)
            
        logging.info("Processing completed successfully")
        logging.info(f"Full transcript saved to: {input_file}")
        logging.info(f"Log file saved to: {log_file}")
        
        return final_text
        
    except Exception as e:
        logging.error(f"Error processing video: {str(e)}")
        return f"Error: {str(e)}"
