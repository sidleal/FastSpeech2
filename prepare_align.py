import argparse

import yaml

from preprocessor import ljspeech, aishell3, libritts, nurc_min, mupev, cmltts, entoa_tts_pros, mupev2


def main(config):
    if "LJSpeech" in config["dataset"]:
        ljspeech.prepare_align(config)
    if "AISHELL3" in config["dataset"]:
        aishell3.prepare_align(config)
    if "LibriTTS" in config["dataset"]:
        libritts.prepare_align(config)
    if "nurc_min" in config["dataset"]:
        nurc_min.prepare_align(config)
    if "mupev" in config["dataset"]:
        mupev.prepare_align(config)
    if "cmltts" in config["dataset"]:
        cmltts.prepare_align(config)
    if "entoa_tts_pros" in config["dataset"]:
        entoa_tts_pros.prepare_align(config)
    if "mupev2" in config["dataset"]:
        mupev2.prepare_align(config)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("config", type=str, help="path to preprocess.yaml")
    args = parser.parse_args()

    config = yaml.load(open(args.config, "r"), Loader=yaml.FullLoader)
    main(config)
