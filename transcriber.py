import os
import time
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEvent, FileSystemEventHandler
import whisper

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

MODEL_PATH = "base"
AUDIO_FILE_EXT = ".m4a"
AUDIO_DIR = os.path.join(os.getcwd(), "audio")
TRANSCRIPT_DIR = os.path.join(os.getcwd(), "transcripts")

model = whisper.load_model(MODEL_PATH)

class AudioHandler(FileSystemEventHandler):
    def on_created(self, event: FileSystemEvent) -> None:
        if event.is_directory:
            return
        if event.src_path.endswith(AUDIO_FILE_EXT):
            try:
                self.transcribe_audio(event.src_path)
            except Exception as e:
                logging.error(f"Failed to transcribe {event.src_path}: {e}")

    def transcribe_audio(self, src_path: str) -> None:
        logging.info(f"Transcribing audio file: {src_path}")
        result = model.transcribe(src_path)

        os.makedirs(TRANSCRIPT_DIR, exist_ok=True)
        
        transcript_file = os.path.join(TRANSCRIPT_DIR, f"{os.path.basename(src_path)}.txt")
        with open(transcript_file, "w") as f:
            f.write(result["text"])
        
        logging.info(f"Transcript saved: {transcript_file}")

def main():
    observer = Observer()
    event_handler = AudioHandler()
    observer.schedule(event_handler, AUDIO_DIR, recursive=True)
    observer.start()
    
    logging.info(f"started monitoring dir: {AUDIO_DIR}")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        logging.info("observer stopped.")
    finally:
        observer.join()


if __name__ == "__main__":
    main()
