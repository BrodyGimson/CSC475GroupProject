import numpy as np
import librosa as lib
import pandas as pd

import os

# Combines files from the dataset to create input expected for the LSTM.
# Input:
#   effect - String
#       Effect name, must be same as folders in dataset.
#   metadata_path - String
#       Path to metadata csv file.
#   incl_poly - Boolean - Not supported yet
#       Choose to include polyphonic sounds in output.
# Output:
#   clean_audio - np.array
#       Long clean audio to be used for training and testing input.
#   effect_audio - np.array
#       Long audio with applied effect to be used as training and 
#       testing output.
def create_data(effect, metadata_path, incl_poly=False):
    mono_sample_path = os.path.join("dataset", "monophonic", "Samples")
    pass