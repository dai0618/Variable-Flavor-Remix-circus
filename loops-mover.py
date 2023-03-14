import time
import os
import shutil
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class ChangeHandler(FileSystemEventHandler):
    def on_modified(self, event):
        target_file_path = event.src_path
        root, ext = os.path.splitext(target_file_path)
        print(target_file_path)

        # if ext == '.asd':
        #     new_path = shutil.move(root, played_loops_dir)
        #     print('moved', root)


if __name__ == "__main__":
    loops_dir = './tmp/separated_loops'
    played_loops_dir = './tmp/played_loops'
    os.makedirs(played_loops_dir, exist_ok=True)

    observer = Observer()
    observer.schedule(ChangeHandler(), loops_dir, recursive=True)
    observer.start()
    # print('watching', loops_dir, '...')
    print('watching', loops_dir, '...')

    try:
        while True:
            time.sleep(1)
    finally:
        observer.stop()
        observer.join()
