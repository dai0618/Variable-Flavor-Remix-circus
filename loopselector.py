import os
import pydub

import torch
import torchaudio
import openunmix
from openunmix import predict
from openunmix import data


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

def create_separated_loops(track_title):
    # root directory
    loops_root_dir = './tmp/loops'
    separated_loops_root_dir = "./tmp/separated_loops"
    wav_preview_dir = './tmp/wav_preview'

    # separated_loopsと同じ階層にパスを作製
    separated_loops_root_stem = "./tmp/separated_loops_stem"
    # each track
    loops_dir = f"{loops_root_dir}/{track_title}"
    os.makedirs(loops_dir, exist_ok=True)
    loops_paths = os.listdir(loops_dir)

    for i, file_path in enumerate(loops_paths):
        # run openunmixer
        sound = pydub.AudioSegment.from_mp3(f"{loops_dir}/{file_path}")
        wav_path = f"{wav_preview_dir}/{track_title}.wav"
        sound.export(wav_path, format="wav")

        print(f"running openunmixer on {file_path}")
        wav_abs_filepath = os.path.abspath(wav_path)

        separate_to_stems(wav_abs_filepath, separated_loops_root_stem)