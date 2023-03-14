import os
import numpy as np
import madmom
import librosa
import soundfile as sf


def extract_loops(audio_file, num_beats=16, output_savename="extracted_loop"):
    assert os.path.exists(audio_file)

    # Load mono audio:
    signal_mono, fs = librosa.load(audio_file, sr=44100, mono=True)
    # Use madmom to estimate the downbeat times:
    downbeat_times = get_downbeats(signal_mono, num_beats)
    # print(downbeat_times)
    # Convert times to frames so we segment signal:
    downbeat_samples = librosa.time_to_samples(downbeat_times, sr=fs)
    # print(downbeat_samples)

    # extract mulitple loops
    # looppaths = []
    # for i, (start, end) in enumerate(zip(downbeat_samples[:-1], downbeat_samples[1:])):
    #     filepath = "{0}_{1}.wav".format(output_savename, i)
    #     sf.write(filepath, signal_mono[start:end], fs)
    #     looppaths.append(filepath)
    # return looppaths

    # extracting only 1 loop
    start = downbeat_samples[:-2][0]
    end = downbeat_samples[2:][0]
    file_path = f"{output_savename}.wav"
    sf.write(file_path, signal_mono[start:end], fs)
    return file_path


def get_downbeats(signal, num_beats=4):
    act = madmom.features.downbeats.RNNDownBeatProcessor()(signal)
    proc = madmom.features.downbeats.DBNDownBeatTrackingProcessor(
        beats_per_bar=[num_beats],
        min_bpm=80.0,
        max_bpm=170,
        fps=100,
        threshold=0.50,
        correct=False
    )
    processor_output = proc(act)
    # print(processor_output)
    downbeat_times = processor_output[processor_output[:, 1]==1, 0]
    return downbeat_times


if __name__ == "__main__":
    extract_loops("tie-me-30.mp3", num_beats=16)
