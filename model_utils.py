import matplotlib.pyplot as plt
import numpy as np
import librosa
from sklearn import metrics
from sklearn.model_selection import train_test_split

import random

# Code based on GuitarLSTM by Keith Bloemer:
# https://github.com/GuitarML/GuitarLSTM

# Plotting Functions

def plot_waveform(s, title):
    plt.figure(figsize=(14, 3))
    plt.plot(s)
    plt.title(title)
    plt.show()

# Simple function to plot three waveforms for comparing
def compare_waveforms(original, predicted, true_output, title, start, stop):
    plt.figure(figsize=(16,6))
    plt.plot(original[start:stop])
    plt.plot(predicted[start:stop])
    plt.plot(true_output[start:stop])
    plt.legend(['original', 'predicted', 'true output'])
    plt.title(title)
    plt.show()

# Viewing spectrograms set to showing hz with no mel or log scale, to inspect high frequencies.
def plot_spectrogram_hz(s,sr,title, style):
    D = librosa.stft(s)
    DdB = librosa.amplitude_to_db(abs(D))
    plt.figure(figsize=(14, 6))
    librosa.display.specshow(DdB[0:1800], sr=sr, x_axis='time', y_axis=style)
    plt.title(title)
    plt.show()

# Plots prediction results to compare with input
def plot_result(trainY, testY, train_predict, test_predict):
    actual = np.append(trainY, testY)
    predictions = np.append(train_predict, test_predict)
    rows = len(actual)
    plt.figure(figsize=(15, 6), dpi=80)
    plt.plot(range(rows), actual, alpha=0.3, color='blue')
    plt.plot(range(rows), predictions, alpha=0.3, color='green')
    plt.axvline(x=len(trainY), color='r')
    plt.legend(['Actual', 'Predictions'])
    plt.xlabel('Time in samples')
    plt.ylabel('')
    plt.title('Actual and Predicted Values. The Red Line Separates The Training And Test Examples')
    plt.show()

# Metrics Functions

def energy_normalized_mae(true, predicted):
    y_true = true / np.max(true)
    y_pred = predicted / np.max(predicted)
    return metrics.mean_absolute_error(y_true, y_pred)

def esr(true, predicted):
    return np.sum(np.square(np.abs(true-predicted))) / np.sum(np.square(np.abs(true)))

def normalized_esr(true, predicted):
    true = true / np.max(true)
    predicted = predicted/np.max(predicted)
    return np.sum(np.square(np.abs(true-predicted))) / np.sum(np.square(np.abs(true)))


# Data Segmentation Functions

# Change data to format expected by the model
# Non-sequential version
def create_dataset(input_file, output_file, size_training, size_test, frame, sr, test_ratio):
    signal = input_file
    wet = output_file
    
    # Creating the foundation of the dataset by splitting the whole audio into 5 seconds segments
    segment_size = sr * 5
    dry_segments = np.zeros((int(signal.size/segment_size), segment_size))
    wet_segments = np.zeros((int(signal.size/segment_size), segment_size))
    counter = 0

    for i in range(0, signal.size-segment_size-1, segment_size):          
        dry_segment = signal[i:i+segment_size]
        wet_segment = wet[i:i+segment_size]
        dry_segments[counter,:], wet_segments[counter,:] = dry_segment, wet_segment
        counter+= 1

    if test_ratio != 1.0:
        # Splitting the segments into the training and testing set
        dry_train, dry_test, wet_train, wet_test = train_test_split(dry_segments, wet_segments, test_size=test_ratio, random_state=5)
    else:
        dry_test = dry_segments
        wet_test = wet_segments

    # Creating the training set (randomly pulling frames and target value from all segments in train set)
    features_train = np.zeros((size_training, frame))
    targets_train = np.zeros((size_training))
    counter = 0

    for i in range(size_training):
        random_index = random.randint(0,dry_train.shape[0]-1)
        dry_slice = dry_train[random_index]
        wet_slice = wet_train[random_index]
        random_start = random.randint(0,segment_size-frame-2)
        features = dry_slice[random_start:random_start+frame]
        target = wet_slice[random_start+frame-1]

        features_train[counter,:], targets_train[counter] = features, target
        counter += 1

    # Creating the testing set (randomly puling frames and target value from segments in test set)
    features_test = np.zeros((size_test, frame))
    targets_test = np.zeros((size_test))
    counter = 0

    for i in range(size_test):
        random_index = random.randint(0,dry_test.shape[0]-1)
        dry_slice = dry_test[random_index]
        wet_slice = wet_test[random_index]
        random_start = random.randint(0,segment_size-frame-2)
        features = dry_slice[random_start:random_start+frame]
        target = wet_slice[random_start+frame-1]

        features_test[counter,:], targets_test[counter] = features, target
        counter += 1

    return dry_test, wet_test, features_train, features_test, targets_train, targets_test

# Change data to format expected by the model
# Sequential version
def create_sequential_dataset(input_file, output_file, size_training, size_test, frame, sr): 
    signal = input_file
    wet = output_file
    
    # Creating the foundation of the dataset by splitting the whole audio into 5 seconds segments
    segment_size = sr * 5
    dry_segments = np.zeros((int(signal.size/segment_size), segment_size))
    wet_segments = np.zeros((int(signal.size/segment_size), segment_size))
    counter = 0

    for i in range(0, signal.size-segment_size-1, segment_size):
                
        dry_segment = signal[i:i+segment_size]
        
        wet_segment = wet[i:i+segment_size]

        dry_segments[counter,:], wet_segments[counter,:] = dry_segment, wet_segment
        counter+= 1

    # Splitting the segments into the training and testing set
    dry_train, dry_test, wet_train, wet_test = train_test_split(dry_segments, wet_segments, test_size=0.2, random_state=5)

    # Creating the training set (pulling frames in sequence from training and testing segments)
    train_frames_pr_segment = int(size_training / dry_train.shape[0])
    test_frames_pr_segment = int(size_test / dry_test.shape[0])

    features_train = np.zeros((size_training, frame))
    targets_train = np.zeros((size_training))
    counter = 0

    for i in range(0,dry_train.shape[0]):
        dry_segment = dry_train[i]
        wet_segment = wet_train[i]
        random_start = random.randint(0,dry_segment.size-train_frames_pr_segment-frame-1)

        for x in range(0+frame, train_frames_pr_segment+frame-2):
            start_point = x + random_start      
            features = dry_segment[start_point:start_point+frame]
            target = wet_segment[start_point+frame-1]
            
            features_train[counter,:], targets_train[counter] = features, target
            counter+= 1

    # Creating the testing set (sequentiually pulling frames and target value from segments in test set)
    features_test = np.zeros((size_test, frame))
    targets_test = np.zeros((size_test))
    counter = 0
    
    for i in range(0,dry_test.shape[0]):
        dry_segment = dry_test[i]
        wet_segment = wet_test[i]
        random_start = random.randint(0,dry_segment.size-test_frames_pr_segment-frame-1)
        
        for x in range(0+frame, test_frames_pr_segment+frame-1):
            start_point = x + random_start      
            features = dry_segment[start_point:start_point+frame]
            target = wet_segment[start_point+frame-1]
            
            features_test[counter,:], targets_test[counter] = features, target
            counter+= 1 
            
    return dry_test, wet_test, features_train, features_test, targets_train, targets_test

# Function used later in the notebook
# Function to prepare audio for the model to predict, as the model expects 
# the input of sequentially ordered frames
def prepare_audio_seq(dry_test, index, frame):    
    audio = dry_test[index]
    counter = 0
    audio = np.pad(audio, (frame-1,0))
    audio = audio[0:audio.size-frame+1]
    results = np.zeros((audio.size, frame))

    for i in range(0+frame,audio.size-frame-1):
            segment = audio[i-frame:i]
            results[counter,:] = segment
            counter+= 1
    
    return results