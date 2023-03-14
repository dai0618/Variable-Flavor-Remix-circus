import os
from pythonosc import dispatcher
from pythonosc import osc_server
import glob
import shutil


def move_loop(file_name):
    target_loop = glob.glob(
        f"{separated_loops_dir}/*/*/{file_name}.*",
        recursive=True
    )

    if target_loop:
        target_loop_path = target_loop[0]
        shutil.move(target_loop_path, played_loops_dir)
        print('moved', file_name)

    # print(target_loop)


def osc_received(unused_addr, args, *values):
    file_name = args
    print('received', file_name)
    move_loop(file_name)


if __name__ == "__main__":
    separated_loops_dir = './tmp/separated_loops'
    played_loops_dir = './tmp/played_loops'
    os.makedirs(played_loops_dir, exist_ok=True)

    # osc server
    dispatcher = dispatcher.Dispatcher()
    dispatcher.map("/file_name", osc_received)

    server = osc_server.ThreadingOSCUDPServer(
        ('localhost', 8888),
        dispatcher
    )

    print(f"serving on {server.server_address}")

    server.serve_forever()
