import librosa as lib
import numpy as np
import pandas as pd

import os, random

# Combines files from the dataset to create input expected for the LSTM.
#
# Input:
#   genre - String
#       Genre name, must be same from list in effectData.csv name.
#   effect_data_path - String
#       Path to effect data csv file.
#   file_data_path - String
#       Path to file data csv file.
#   mu_comp - Boolean - Default True
#       Specify whether to use mu's law compression.
#   srate - Integer - Default 22050
#       Specify srate to load files at.
#   duration - Integer - Default 120
#       Specify duration of output in seconds.
#   type - String - Default "scale"
#       Type of audio wanted. 
#           Options: scale, random, pentatonic
#   incl_poly - Boolean - Default True
#       Choose to include polyphonic sounds in output.
#
# Output:
#   clean_audio - np.array
#       Long clean audio to be used for training and testing input.
#   effect_audio - np.array
#       Long audio with applied effect to be used as training and 
#       testing output.
def create_data(genre, effect_data_path, file_data_path, mu_comp=True, srate=22050, duration=120, type="scale", incl_poly=False):
    mono_sample_path = os.path.join("dataset", "monophonic", "Samples")

    if incl_poly == True:
        print("Polymphonic not currently supported. Ignoring param.")
    
    effect_df = pd.read_csv(effect_data_path)
    file_df = pd.read_csv(file_data_path)

    effect_df = effect_df[( effect_df.genre == genre)].iloc[0]

    if (effect_df.empty):
        print("Genre could not be found, double check string format.")
        return [], []

    clean_path = os.path.join(mono_sample_path, "NoFX")
    effect_path = os.path.join(mono_sample_path, effect_df.fxType)

    # For both, use picking for play style and instrument 9 (the stratocaster)
    # Only grab files that match the genre given
    file_effect_df = file_df[
        ( file_df.playStyle == 3 ) &
        ( file_df.instrumentSetting == 9 ) &
        ( file_df.fxType == effect_df.fxTypeID ) &
        ( file_df.fxSetting == effect_df.fxSettingID )
    ]

    # Only select no effect
    file_clean_df = file_df[
        ( file_df.playStyle == 3 ) &
        ( file_df.instrumentSetting == 9 ) &
        ( file_df.fxType == 11 )
    ]

    if (type == "scale"):
        # Duration / 2 makes sure a scale of specified duration is guaranteed.
        # 2 is used because the dataset notes are all 2 second durations.
        start = random.randint(0, (len(file_clean_df) - (int) (duration / 2)))

        clean_audio = _create_scale(clean_path, file_clean_df, srate, duration, start)
        effect_audio = _create_scale(effect_path, file_effect_df, srate, duration, start)
    elif (type == "random"):
        clean_audio, effect_audio = _create_random(clean_path, effect_path, file_clean_df, file_effect_df, srate, duration)
    elif (type == "pentatonic"):
        clean_audio, effect_audio = _create_pentatonic(clean_path, effect_path, file_clean_df, file_effect_df, srate, duration)
    else:
        print("Type not found. Select from: scale, random, pentatonic.")
        clean_audio, effect_audio = []

    if (mu_comp == True):
        clean_audio = lib.mu_compress(clean_audio, mu=255)
        effect_audio = lib.mu_compress(effect_audio, mu=255)

    return clean_audio, effect_audio

# -----------------------------------------------------------------------
# Helper function below are designed to be used only in this module.

# Picks a random starting note, then puts notes in order up to a duration.
def _create_scale(audio_path, file_df, srate, duration, start):
    audio = []

    max_length = duration * srate

    for _, row in file_df[start:].iterrows():
        file = os.path.join(audio_path, row.fileID + ".wav")
        note, _ = lib.load(file, sr=srate)

        audio = np.hstack([audio, note])

        if (len(audio) >= max_length):
            return audio

    return audio

# Chooses a random file each time till the duration of audio is achieved.
def _create_random(clean_path, effect_path, file_clean_df, file_effect_df, srate, duration):
    clean_audio = []
    effect_audio = []

    max_length = duration * srate

    while len(clean_audio) < max_length:
        index = random.randint(0, len(file_clean_df) - 1)

        clean_file = os.path.join(clean_path, file_clean_df.iloc[index].fileID + ".wav")
        effect_file = os.path.join(effect_path, file_effect_df.iloc[index].fileID + ".wav")

        clean, _ = lib.load(clean_file, sr=srate)
        effect, _ = lib.load(effect_file, sr=srate)

        # Create random duration
        note_length = (int) (len(clean) / random.randint(1, 4))

        # Remove leading and trailing silence in a predictable manner
        clean, indexes = lib.effects.trim(clean)
        effect = effect[indexes[0]:indexes[1]]

        clean_note = process_note(clean, note_length, srate)
        effect_note = process_note(effect, note_length, srate)

        clean_audio = np.hstack([clean_audio, clean_note])
        effect_audio = np.hstack([effect_audio, effect_note])

    return clean_audio, effect_audio

# Creates a solo-like tune based on a pentatonic scale.
# Chooses a random starting value on the low E string from the files, then maps out 
# the appropriate pentatonic scale.
# From that scale it chooses random notes to create the audio up to the duration.
def _create_pentatonic(clean_path, effect_path, file_clean_df, file_effect_df, srate, duration):

    # 9 because dataset goes up to fret 12 on each string and we want whole scale
    start_fret = random.randint(0, 9)

    file_clean_df = file_clean_df[
        ((file_clean_df.string) == 1 & (file_clean_df.fret == start_fret)) |
        ((file_clean_df.string == 1) & (file_clean_df.fret == start_fret + 3)) |
        ((file_clean_df.string == 2) & (file_clean_df.fret == start_fret)) |
        ((file_clean_df.string == 2) & (file_clean_df.fret == start_fret + 2)) |
        ((file_clean_df.string == 3) & (file_clean_df.fret == start_fret)) |
        ((file_clean_df.string == 3) & (file_clean_df.fret == start_fret + 2)) |
        ((file_clean_df.string == 4) & (file_clean_df.fret == start_fret)) |
        ((file_clean_df.string == 4) & (file_clean_df.fret == start_fret + 2)) |
        ((file_clean_df.string == 5) & (file_clean_df.fret == start_fret)) |
        ((file_clean_df.string == 5) & (file_clean_df.fret == start_fret + 3)) |
        ((file_clean_df.string == 6) & (file_clean_df.fret == start_fret)) |
        ((file_clean_df.string == 6) & (file_clean_df.fret == start_fret + 3))
    ]

    file_effect_df = file_effect_df[
        ((file_effect_df.string == 1) & (file_effect_df.fret == start_fret)) |
        ((file_effect_df.string == 1) & (file_effect_df.fret == start_fret + 3)) |
        ((file_effect_df.string == 2) & (file_effect_df.fret == start_fret)) |
        ((file_effect_df.string == 2) & (file_effect_df.fret == start_fret + 2)) |
        ((file_effect_df.string == 3) & (file_effect_df.fret == start_fret)) |
        ((file_effect_df.string == 3) & (file_effect_df.fret == start_fret + 2)) |
        ((file_effect_df.string == 4) & (file_effect_df.fret == start_fret)) |
        ((file_effect_df.string == 4) & (file_effect_df.fret == start_fret + 2)) |
        ((file_effect_df.string == 5) & (file_effect_df.fret == start_fret)) |
        ((file_effect_df.string == 5) & (file_effect_df.fret == start_fret + 3)) |
        ((file_effect_df.string == 6) & (file_effect_df.fret == start_fret)) |
        ((file_effect_df.string == 6) & (file_effect_df.fret == start_fret + 3))
    ]

    return _create_random(clean_path, effect_path, file_clean_df, file_effect_df, srate, duration)

# Cleans up notes and changes their duration.
def process_note(note, note_length, srate):
    fade_length = (int) (srate * 0.1)
    fade_curve = np.linspace(1.0, 0.0, fade_length)

    note = note[:note_length]
    fade_start = len(note) - fade_length

    # Add quick fade to make note change less abrupt
    note[fade_start:] = note[fade_start:] * fade_curve

    return note