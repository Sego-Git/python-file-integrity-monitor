
import os
import time
import threading

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from integrity import check_integrity
from logger import log_event


class IntegrityEventHandler(FileSystemEventHandler):

    def __init__(self, folder_path, baseline):
        self.folder_path = folder_path
        self.baseline = baseline
        self.timer = None
        self.lock = threading.Lock()

    def on_any_event(self, event):

        # Ignore directory events.
        if event.is_directory:
            return

        # Process only relevant file events.
        if event.event_type not in {
            "created",
            "modified",
            "deleted",
            "moved"
        }:
            return

        print()
        print("REAL-TIME FILE EVENT DETECTED")
        print("Event type:", event.event_type)
        print("File:", event.src_path)
        
        log_event(
            "INFO",
            f"REALTIME_EVENT_{event.event_type.upper()}",
            event.src_path
        )

        # Reset the timer whenever another event arrives.
        with self.lock:

            if self.timer is not None:
                self.timer.cancel()

            self.timer = threading.Timer(
                1.0,
                self.run_integrity_check
            )

            self.timer.daemon = True
            self.timer.start()

    def run_integrity_check(self):

        print()
        print("Checking file integrity...")

        check_integrity(
            self.folder_path,
            self.baseline
        )

    def cancel_pending_timer(self):

        with self.lock:

            if self.timer is not None:
                self.timer.cancel()
                self.timer = None


def start_watching(folder_path, baseline):

    absolute_folder_path = os.path.abspath(folder_path)

    if not os.path.isdir(absolute_folder_path):
        print("ERROR: The specified folder does not exist.")
        print("Folder:", folder_path)
        return

    event_handler = IntegrityEventHandler(
        folder_path,
        baseline
    )

    observer = Observer()

    observer.schedule(
        event_handler,
        absolute_folder_path,
        recursive=True
    )

    observer.start()

    print("Real-time monitoring started.")
    print("Folder:", absolute_folder_path)
    print("Press CTRL+C to stop monitoring.")

    try:
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print("\nStopping real-time monitoring...")

    finally:
        observer.stop()
        observer.join()
        event_handler.cancel_pending_timer()

    print("Monitoring stopped.")