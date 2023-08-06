import numpy as np
import os
import pandas as pd
import librosa


def extract_feature_for_audio(y, sr):
    mfcc = np.mean(librosa.feature.mfcc(y=y, sr=sr, n_mfcc=40).T, axis=0)
    mel = np.mean(librosa.feature.melspectrogram(y=y, sr=sr).T, axis=0)
    stft = np.abs(librosa.stft(y))
    chroma = np.mean(librosa.feature.chroma_stft(S=stft, y=y, sr=sr).T, axis=0)
    contrast = np.mean(librosa.feature.spectral_contrast(S=stft, y=y, sr=sr).T, axis=0)
    tonnetz = np.mean(librosa.feature.tonnetz(y=librosa.effects.harmonic(y), sr=sr).T, axis=0)
    return mfcc, chroma, mel, contrast, tonnetz  # shape: (40,), (12,), (128,), (7,), (6,)


def generate_feature_file(path):
    columns = ['feature_column'] * 193 + ['label']
    audio_df = pd.DataFrame(columns=columns)

    label = 0
    label_name_dict = {}

    for sub_directory in os.listdir(path):

        audio_directory = ""

        if path[-1] == '/':
            audio_directory = path + sub_directory
        else:
            audio_directory = path + '/' + sub_directory

        label_name_dict[label] = sub_directory

        for files in os.listdir(audio_directory):
            audio, sr = librosa.load(path)
            mfcc, chroma, mel, contrast, tonnetz = extract_feature_for_audio(audio, sr)
            features = np.hstack([mfcc, chroma, mel, contrast, tonnetz, label])
            fill = np.empty((0, 194))
            features = np.vstack([fill, features])
            row_df = pd.DataFrame(features, columns=columns)
            audio_df = audio_df.append(row_df, ignore_index=True)

        label += 1

    return audio_df, label_name_dict
