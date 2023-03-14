import os
import loopextractor
import glob

from spleeter import separator
from spleeter.separator import Separator

def create_loop(audio_path, track_title):
    print(f"recieved {track_title}")

    #root directory
    loops_root_dir = './loops_ver2'
    separated_loops_root_dir = "./separated_loops"

    separated_stems_root_dir = "./separated_stems"

    #making directory
    loops_dir = f"{loops_root_dir}/{track_title}"
    loops_stems_dir = "{}/{}".format(separated_loops_root_dir, track_title)

    os.makedirs(loops_dir, exist_ok=True)
    os.makedirs(separated_stems_root_dir, exist_ok=True)

    #run spleeter
    print("running spleeter")
    separator = Separator('spleeter:4stems')
    separator.separate_to_file(audio_path, separated_stems_root_dir)

    loops_paths = glob.glob(f"{separated_stems_root_dir}/{track_title}/*")
    for i, file_path in enumerate(loops_paths):
        #run loop extractor
        loopextractor.run_algorithm(
            file_path,
            output_savename= f"{loops_dir}/{track_title}_{i}",
            beats_num= 4
        )

    print('Done creating loop')

    return(loops_stems_dir)

if __name__ == "__main__":
    # Run algorithm on test song:
    create_loop('/Users/ryohasegawa/Documents/coding/spotify_api/visitor-reflective-remix/reciever/preview_tracks/mBvZtxh6z5EMrW91fVHj.mp3', "mBvZtxh6z5EMrW91fVHj")
