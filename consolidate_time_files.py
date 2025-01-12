#! /usr/bin/env python
directories = ['early_release', 'released','clouds']

# Each directory contains an image directory with contains
# *.npy file containing the timestamps in an array
# and .png images 
# a resized_images directory with resized images

# Create a manifest that is a json object with the following structure
# {
#   "[directory_name]": {
#     "image_directory": "[directory_name]/images",
#     "resized_image_directory": "[directory_name]/resized_images",
#     "timestamps": [timestamp1, timestamp2, ...],
#     "image_filenames": [filename1, filename2, ...]
#   },
#   ....
# }

import json
import os
import numpy as np
from glob import glob
from typing import Dict, List
from typing import Dict, List, Union
from datetime import datetime, timezone, timedelta


def time_to_fname(time: int, suffix = '') -> str:
    dt = datetime.fromtimestamp(time/1000, timezone.utc)
    format = '%Y-%m-%dT%Hh%Mm'
    time_str = dt.strftime(format)
    return f'tempo_{time_str}{suffix}.png'


def fname_to_time(fname: str) -> int:
    time_str = fname.replace('tempo_', '').replace('.png', '')
    dt = datetime.strptime(time_str, '%Y-%m-%dT%Hh%Mm')
    return int(dt.timestamp() * 1000)

from typing import Mapping, TypedDict, Union, List, cast

def strip_newlines(s: str) -> str:
    return s.replace('\n', '')

class DirectoryInfo(TypedDict):
    image_directory: str
    resized_image_directory: str
    timestamps: List[int]

DirectoryStructure = Mapping[str, DirectoryInfo]
manifest: DirectoryStructure = {}

# Load existing manifest
manifest_path = 'manifest.json'


# Update manifest with new directories
def consolidate_timestamps(directory) -> List[int]:
    timestamp_files =  glob(os.path.join(directory, 'images', 'times*.npy'))
    timestamps: List[int] = []
    for timestamp_file in timestamp_files:
        if timestamp_file != 'timestamps.npy':
            try:
                with open(timestamp_file, 'r') as f:
                    ts = f.read()[1:-1].split(',')
                    timestamps.extend(int(t) for t in ts)
            except UnicodeDecodeError:
                print(f'Error reading {timestamp_file}')
                print('Trying npy binary file')
                with open(timestamp_file, 'rb') as f:
                    ts = np.load(f)
                    timestamps.extend(ts)
            except Exception as e:
                print(f'Error reading {timestamp_file}')
                print(e)

    unique_timestamps = sorted(set(timestamps))
    # write this to a file
    with open(f'{directory}/images/timestamps.npy', 'w') as f:
        f.write('[\n')
        for t in unique_timestamps[:-1]:
            f.write(f'{t},\n') 
        f.write(f'{unique_timestamps[-1]}\n')
        f.write(']')
    print(f'Wrote {len(unique_timestamps)} timestamps to {directory}/images/timestamps.npy')
    return timestamps

# for directory in directories:
#     consolidate_timestamps(directory)

def read_timestamps_file(directory: str) -> List[int]:
    with open(f'{directory}/images/timestamps.npy', 'r') as f:
        ts = list(map(int, strip_newlines(f.read())[1:-1].split(',')))
    return ts
   