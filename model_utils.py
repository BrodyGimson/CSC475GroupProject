import matplotlib.pyplot as plt
import numpy as np
import librosa
from sklearn import metrics

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