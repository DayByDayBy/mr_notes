import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEvent, FileSystemEventHandler
import whisper

model_path = "base"
audio_file_ext = ".m4a"

class AudioHandler(FileSystemEventHandler):
    def on_created(self, event: FileSystemEvent) -> None:
        if event.is_directory():
            return None
    
        if event.src_path.endswith(audio_file_ext):
            result = whisper.load_model(
                model_path
                ).transcribe(
                    event.src_path)
            transcript_dir = os.path.join(os.getcwd(), "transcripts")
            if not os.path.exists(transcript_dir):
                os.makedirs(transcript_dir)
            transcript_file = f"{os.path.basename(event.src_path)}.txt"
            with open(os.path.join(transcript_dir, transcript_file), "w") as f:
                f.write(result["text"])
            
            print(f"transcript saved - {event.src_path}")

observer = Observer()
observer.schedule(AudioHandler(), os.getcwd() + "/audio", recursive = True)
observer.start()

try:

    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()
    observer.join()