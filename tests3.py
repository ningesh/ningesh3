# -*- coding: utf-8 -*-
"""
Created on Tue Aug 16 20:16:55 2022

@author: INBOTICS
"""
import s3fs
import zipfile
import tempfile
import numpy as np
from tensorflow import keras
from pathlib import Path
import logging
import os

AWS_ACCESS_KEY="AKIAWESODN7K3SHSRMO6"
AWS_SECRET_KEY="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"
BUCKET_NAME="testbucketningesh"


def get_s3fs():
  return s3fs.S3FileSystem(key=AWS_ACCESS_KEY, secret=AWS_SECRET_KEY)

def zipdir(path, ziph):
  # Zipfile hook to zip up model folders
  length = len(path) # Doing this to get rid of parent folders
  for root, dirs, files in os.walk(path):
    folder = root[length:] # We don't need parent folders! Why in the world does zipfile zip the whole tree??
    for file in files:
      ziph.write(os.path.join(root, file), os.path.join(folder, file))

def s3_get_keras_model(model_name: str) -> keras.Model:
  with tempfile.TemporaryDirectory() as tempdir:
    s3fs = get_s3fs()
    # Fetch and save the zip file to the temporary directory
    s3fs.get(f"{BUCKET_NAME}/{model_name}.h5py", f"{tempdir}/{model_name}.h5py")
    # Extract the model zip file within the temporary directory
    # with zipfile.ZipFile(f"{tempdir}/{model_name}.zip") as zip_ref:
    #     zip_ref.extractall(f"{tempdir}/{model_name}")
    # Load the keras model from the temporary directory
    return keras.models.load_model(f"{tempdir}/{model_name}")


loaded_model = s3_get_keras_model("model")