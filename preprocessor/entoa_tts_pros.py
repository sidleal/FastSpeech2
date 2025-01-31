import os

import librosa
import numpy as np
from scipy.io import wavfile
from tqdm import tqdm

from text import _clean_text


def prepare_align(config):
    in_dir = config["path"]["corpus_path"]
    out_dir = config["path"]["raw_path"]
    sampling_rate = config["preprocessing"]["audio"]["sampling_rate"]
    max_wav_value = config["preprocessing"]["audio"]["max_wav_value"]
    with open(os.path.join(in_dir, "entoa-tts-pros-all.csv"), encoding="utf-8") as f:
        for line in tqdm(f):
            if 'path' in line:
                continue
            parts = line.strip().split(",")
            base_name = parts[0].split("/")[-1][:-4]

            text = parts[5]
            speaker = parts[2]
            
            wav_path = in_dir + "/"+ parts[0]
            print(wav_path, speaker, text)

            if os.path.exists(wav_path):
                os.makedirs(os.path.join(out_dir, speaker), exist_ok=True)
                wav, _ = librosa.load(wav_path, sampling_rate)
                wav = wav / max(abs(wav)) * max_wav_value
                wavfile.write(
                    os.path.join(out_dir, speaker, "{}.wav".format(base_name)),
                    sampling_rate,
                    wav.astype(np.int16),
                )
                with open(
                    os.path.join(out_dir, speaker, "{}.lab".format(base_name)),
                    "w",
                ) as f1:
                    f1.write(text)