import os
import time
import pypandoc
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


# Now run your Pandoc commands or other operations that require pdflatex

class Watcher:
    DIRECTORY_TO_WATCH = "G:/My Drive/IARS 2024"

    def __init__(self):
        self.observer = Observer() # create observer

    def run(self):
        self.list_files_initial()
        event_handler = Handler() # create event handler
        self.observer.schedule(event_handler, self.DIRECTORY_TO_WATCH, recursive=True) # schedule the event handler
        self.observer.start() # start the observer
        try:
            while True:
                time.sleep(5) 
        except:
            self.observer.stop()
            print("Observer Stopped") 

        self.observer.join()

    def list_files_initial(self):
        print("Listing all files in directory at startup:")
        for filename in os.listdir(self.DIRECTORY_TO_WATCH):
            path = os.path.join(self.DIRECTORY_TO_WATCH, filename)
            if os.path.isfile(path):
                last_modified_time = os.path.getmtime(path)
                readable_time = time.ctime(last_modified_time)
                print(f"{filename}, Last Modified Time: {readable_time}")

class Handler(FileSystemEventHandler):

    @staticmethod
    def on_any_event(event):
        if event.is_directory:
            return None

        elif event.event_type == 'created' or event.event_type == 'modified':
            # Take any action here when a file is modified or created.
            if event.src_path.endswith(".docx"):
                output_filename = event.src_path.replace(".docx", ".pdf")
                pypandoc.convert_file(event.src_path, 'pdf', outputfile=output_filename)
                print(f"Converted {event.src_path} to PDF")

if __name__ == '__main__':
    w = Watcher()
    w.run()


    DIRECTORY_TO_WATCH = "G:/My Drive/IARS 2024"
