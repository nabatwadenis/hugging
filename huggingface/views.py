import base64
import io
import logging
import os
import random

import librosa
import numpy as np
import pydub
from datasets import load_dataset, Audio
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
# from huggingface_hub.commands.user import login
from huggingface_hub import HfApi, login
from pydub import AudioSegment
from tqdm import tqdm

from boto3.s3.transfer import S3Transfer
import boto3

client = boto3.client('s3', aws_access_key_id='AKIASKPDZEFWLZ2K6JIL',
                      aws_secret_access_key='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')

minimum = 6000
maximum = 6010
train_range = 'train[' + str(0) + ':' + str(maximum) + ']'


def load_audio_datasets():
    dataset = load_dataset("DrLugha/kimeru_yt_2022_v0.1.0", split=train_range, use_auth_token=True)
    return dataset


def read_dataset_and_upload(self):
    dataset = load_audio_datasets()

    audio_blobs = []
    for i in tqdm(range(minimum, maximum)):
        audio_array = np.asarray(dataset[i]["audio"]["array"])
        channels = 2 if (audio_array.ndim == 2 and audio_array.shape[1] == 2) else 1

        print(audio_array)

        # Convert audio array to 16-bit integer format
        y = np.int16(audio_array * 2 ** 15)

        clip = pydub.AudioSegment(y.tobytes(),
                                  frame_rate=dataset[i]["audio"]["sampling_rate"],
                                  sample_width=2,
                                  channels=channels)

        audio_blob = clip.export(format='wav').read()
        audio_blobs.append({
            "index": i,
            "filename": str(i) + ".wav"
        })

        upload_s3(audio_blob, i)

    return JsonResponse(audio_blobs, safe=False)


def upload_s3(file_blob, index):
    try:
        client.put_object(Body=file_blob,
                          Bucket='zeraki-translations',
                          Key='audio_files/kimeru_yt_2022_v0.1.0/' + str(index) + ".wav")
    except Exception as e:
        logging.exception("Error uploading file to S3. Index: %s. Exception: %s", index, str(e))
        raise e
