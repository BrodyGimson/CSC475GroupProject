import librosa as lib
import numpy as np
import pandas as pd

import os, random

# TODO: Update dataset creation to incorporate metadata and tags.

# Combines files from the dataset to create input expected for the LSTM.
#
# Input:
#   effect - String
#       Effect name, must be same as folders in dataset.
#   metadata_path - String
#       Path to metadata csv file.
#   mu_comp - Boolean - Default True
#       Specify whether to use mu's law compression.
#   srate - Integer - Default 22050
#       Specified srate to load files at.
#   duration - Integer - Default 120
#       Specified duration of output in seconds.
#   type - String - Default "scale"
#       Type of audio wanted. Options: scale, random (not implemented), pentatonic (not implemented)
#   incl_poly - Boolean - Default True
#       Choose to include polyphonic sounds in output.
#
# Output:
#   clean_audio - np.array
#       Long clean audio to be used for training and testing input.
#   effect_audio - np.array
#       Long audio with applied effect to be used as training and 
#       testing output.
def create_data(effect, metadata_path, mu_comp=True, srate=22050, duration=120, type="scale", incl_poly=False):
    mono_sample_path = os.path.join("dataset", "monophonic", "Samples")

    if incl_poly == True:
        print("Polymphonic not currently supported. Ignoring param.")
    
    clean_path = os.path.join(mono_sample_path, "NoFX")
    effect_path = os.path.join(mono_sample_path, effect)

    if (not os.path.isdir(effect_path)):
        print("Effect could not be found, double check string format.")
        return [], []

    if (type == "scale"):
        clean_audio = _create_scale(clean_path, metadata_path, srate, duration)
        effect_audio = _create_scale(effect_path, metadata_path, srate, duration)
    elif (type == "random"):
        clean_audio, effect_audio = _create_random(clean_path, effect_path, metadata_path, srate, duration)
    elif (type == "pentatonic"):
        clean_audio, effect_audio = _create_pentatonic(clean_path, effect_path, metadata_path, srate, duration)
    else:
        print("Type not found. Select from: scale, random, pentatonic.")
        clean_audio, effect_audio = []

    if (mu_comp == True):
        clean_audio = lib.mu_compress(clean_audio, mu=255)
        effect_audio = lib.mu_compress(effect_audio, mu=255)

    return clean_audio, effect_audio

# -----------------------------------------------------------------------
# Helper function below are designed to be used only in this module.

# Simply puts notes in order, up to the duration, into one audio stream.
def _create_scale(audio_path, metadata_path, srate, duration):
    audio = []

    max_length = duration * srate

    # Sort files as listdir puts them in random order dependent on OS.
    file_paths = sorted(os.listdir(audio_path))

    # TODO: Update logic to incorporate tagging and fix below.
    # i counter and modulo 3 are temporary measures.
    for i, file_path in enumerate(file_paths):

        # Account for the three effect strengths.
        if (i % 3 == 0 or "NoFX" in audio_path):
            file = os.path.join(audio_path, file_path)
            note, _ = lib.load(file, sr=srate)

            audio = np.hstack([audio, note])

        if (len(audio) >= max_length):
            return audio

    return audio

# Simply chooses a random file each time till the duration of audio is achieved.
def _create_random(clean_path, effect_path, metadata_path, srate, duration):
    audio = []

    max_length = duration * srate

    print("Random type not implemented yet.")
    return []

# Creates a solo-like tune based on the pentatonic scale.
# Chooses a random starting value on the low E string from the files, then maps out 
# the appropriate pentatonic scale.
# From the scale it chooses random notes to create the audio up to the duration.
def _create_pentatonic(clean_path, effect_path, metadata_path, srate, duration):
    audio = []

    max_length = duration * srate

    print("Pentatonic type not implemented yet.")
    return []