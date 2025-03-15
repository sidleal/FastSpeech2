import argparse

import yaml

from preprocessor import ljspeech, aishell3, libritts, nurc_min, mupev, cmltts, entoa_tts_pros, mupev2, cmltts_333, cmltts_entoa_pros, cmltts_entoa_auto


def main(config):
    if "LJSpeech" in config["dataset"]:
        ljspeech.prepare_align(config)
    elif "AISHELL3" in config["dataset"]:
        aishell3.prepare_align(config)
    elif "LibriTTS" in config["dataset"]:
        libritts.prepare_align(config)
    elif "nurc_min" in config["dataset"]:
        nurc_min.prepare_align(config)
    elif "mupev" in config["dataset"]:
        mupev.prepare_align(config)
    elif "cmltts_333" in config["dataset"]:
        cmltts_333.prepare_align(config)
    elif "cmltts_entoa_pros" in config["dataset"]:
        cmltts_entoa_pros.prepare_align(config)
    elif "cmltts_entoa_auto" in config["dataset"]:
        cmltts_entoa_auto.prepare_align(config)
    elif "cmltts" in config["dataset"]:
        cmltts.prepare_align(config)
    elif "entoa_tts_pros" in config["dataset"]:
        entoa_tts_pros.prepare_align(config)
    elif "mupev2" in config["dataset"]:
        mupev2.prepare_align(config)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("config", type=str, help="path to preprocess.yaml")
    args = parser.parse_args()

    config = yaml.load(open(args.config, "r"), Loader=yaml.FullLoader)
    main(config)
