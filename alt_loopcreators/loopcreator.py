import os
import loopextractor
import glob

from spleeter import separator
from spleeter.separator import Separator

def create_loop(audio_path, track_title):
    print('loopcreator_ver1')
    print(f"recieved {track_title}")

    #root directory
    loops_root_dir = './loops'
    separated_loops_root_dir = "./separated_loops"

    #making directory
    loops_dir = f"{loops_root_dir}/{track_title}"
    loops_stems_dir = "{}/{}".format(separated_loops_root_dir, track_title)

    os.makedirs(loops_dir, exist_ok=True)
    os.makedirs(loops_stems_dir, exist_ok=True)

    loopextractor.run_algorithm(
        audio_path,
        output_savename= f"{loops_dir}/{track_title}",
        beats_num= 16
    )

    #run spleeter
    print("running spleeter")
    separator = Separator('spleeter:4stems')

    loops_paths = glob.glob(f"{loops_dir}/*")
    for file_path in loops_paths:
        #chord detection

        #spleeter
        print(file_path)
        separator.separate_to_file(file_path, loops_stems_dir)

    print('Done creating loop')

    return(loops_stems_dir)


if __name__ == "__main__":
    # Run algorithm on test song:
    create_loop('/Users/ryohasegawa/Documents/coding/spotify_api/visitor-reflective-remix/reciever/preview_tracks/mBvZtxh6z5EMrW91fVHj.mp3', "mBvZtxh6z5EMrW91fVHj")
