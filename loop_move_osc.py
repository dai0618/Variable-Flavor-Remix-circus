import os
from pythonosc import dispatcher
from pythonosc import osc_server
import glob
import shutil


def move_loop(file_name):
    separated_loops_dir = './tmp/separated_loops_stem'
    played_loops_dir = './tmp/played_loops'
    os.makedirs(played_loops_dir, exist_ok=True)

    target_loop = glob.glob(
        f"{separated_loops_dir}/*/{file_name}.*",
        recursive=True
    )
    try:
        os.remove(f"{played_loops_dir}/{file_name}.wav")
    except:
        print("can't remove!!")

    
    if target_loop:
        target_loop_path = target_loop[0]
        shutil.move(target_loop_path, played_loops_dir)
        print('moved', file_name)

    # print(target_loop)