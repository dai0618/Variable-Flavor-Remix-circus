import os
import pydub

import torch
import torchaudio
import openunmix
from openunmix import predict
from openunmix import data

import loopextractor2


def separate_to_stems(input_file, output_dir):
    separator = openunmix.umxl()

    audio, rate = data.load_audio(input_file)
    estimates = predict.separate(audio, rate)

    file_name = os.path.splitext(os.path.basename(input_file))[0]

    os.makedirs(output_dir, exist_ok=True)
    for target, estimate in estimates.items():
        target_path = f"{output_dir}/{target}/{target}_{file_name}.wav"
        torchaudio.save(
            target_path,
            torch.squeeze(estimate).to("cpu"),
            sample_rate=separator.sample_rate,
        )


def create_loop(audio_path, track_title, key):
    # warnings.filterwarnings('ignore')

    # root directory
    loops_root_dir = './tmp/loops'
    separated_loops_root_dir = "./tmp/separated_loops"
    wav_preview_dir = './tmp/wav_preview'

    # separated_loopsと同じ階層にパスを作製
    separated_loops_root_stem = "./tmp/separated_loops_stem"

    # each track
    loops_dir = f"{loops_root_dir}/{track_title}"
    os.makedirs(loops_dir, exist_ok=True)

    # loops_key_dir = f"{separated_loops_root_dir}/{str(key)}"
    # os.makedirs(loops_key_dir, exist_ok=True)

    # separated_loopsと同じ階層にフォルダを作製
    parts = ['bass', 'drums', 'other', 'vocals']
    os.makedirs(separated_loops_root_stem, exist_ok=True)
    # loops_key_dir_stem = f"{separated_loops_root_stem}/{str(key)}"
    # os.makedirs(loops_key_dir_stem, exist_ok=True)
    for part in parts:
        loops_key_dir_stem_part = f"{separated_loops_root_stem}/{part}"
        os.makedirs(loops_key_dir_stem_part, exist_ok=True)

    output_path = f"tmp/loops/{track_title}/{track_title}.wav"

    # loop extraction
    loopextractor2.extract_loops(
        audio_path,
        num_beats=8,
        output_savename=f"{loops_dir}/{track_title}",
    )

    loops_paths = os.listdir(loops_dir)
    # for i, file_path in enumerate(loops_paths):
    #     # run openunmixer
    #     sound = pydub.AudioSegment.from_mp3(f"{loops_dir}/{file_path}")
    #     wav_path = f"{wav_preview_dir}/{track_title}.wav"
    #     sound.export(wav_path, format="wav")

    #     print(f"running openunmixer on {file_path}")
    #     wav_abs_filepath = os.path.abspath(wav_path)

    #     separate_to_stems(wav_abs_filepath, separated_loops_root_stem)

    print('Created loop')

    return track_title

    # 現在のloopのパス
    # loops_path = f"{separated_loops_root_dir}/{key}/{track_title}"
    # # stemごとにフォルダに移動
    # for part in parts:
    #     part_file = part + '_' + track_title
    #     shutil.move(f"{loops_path}/{part_file}", f"{loops_key_dir_stem}/{i}")


if __name__ == "__main__":
    # Run algorithm on test song:
    create_loop('./tmp/tie-me-30.mp3', 'tie-me-down', 0)
