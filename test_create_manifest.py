#! /usr/bin/env python
directories = ['early_release', 'released','clouds']



import json
import os
import numpy as np
from glob import glob
from typing import Dict, List
from typing import Dict, List, Union
from datetime import datetime, timezone, timedelta
from consolidate_time_files import consolidate_timestamps


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

class DirectoryInfo(TypedDict):
    image_directory: str
    resized_image_directory: str
    timestamps: List[int]

DirectoryStructure = Mapping[str, DirectoryInfo]
# {image_directory: str, resized_image_directory: str, timestamps: List[int]}
manifest: DirectoryStructure = {}

# Load existing manifest
manifest_path = 'manifest.json'
if os.path.exists(manifest_path):
    with open(manifest_path, 'r') as f:
        old_manifest: DirectoryStructure = json.load(f)
else:
    old_manifest: DirectoryStructure = {}
    
# use git to check if this is a sparse checkout
import subprocess
is_sparse = subprocess.run(['git', 'config', 'core.sparseCheckout'], capture_output=True)
is_sparse = 'true' in is_sparse.stdout.decode().lower()

# Update manifest with new directories
for directory in directories:
    print(directory)
    # if directory not in manifest:
    manifest[directory] = cast(DirectoryInfo, {})
    manifest[directory]['image_directory'] = os.path.join(directory, 'images')
    manifest[directory]['resized_image_directory'] = os.path.join(directory,'images', 'resized_images')
    timestamp_files =  glob(os.path.join(directory, 'images', 'times*.npy'))
    timestamps = consolidate_timestamps(directory)
    manifest[directory]['timestamps'] = timestamps
    # manifest[directory]['image_filenames'] = list(map(os.path.basename,glob(os.path.join(directory, 'images', 'tempo*.png'))))
    if not is_sparse:
        image_filenames = list(map(os.path.basename,glob(os.path.join(directory, 'images', 'tempo*.png'))))
        if len(image_filenames) == 0:
            print(f"No images found for {directory}")
        else:
            # Check if all timestamps have corresponding images
            test_ts = set([time_to_fname(t) for t in timestamps])
            test_fn = set(image_filenames)
            if test_ts != test_fn:
                print(f"Missing images for {directory}:\n {test_ts - test_fn}")
                print(f"Extra images for {directory}:\n {test_ts - test_fn}")
            else:
                print("\t All images present")
                print("\t Number of images: ", len(image_filenames))
        
    # sort the timestamps and filenames by timestamp
    manifest[directory]['timestamps'] = sorted(set(manifest[directory]['timestamps']))

# Print new dates added in Eastern Time
eastern = timezone(timedelta(hours=-5))  # Eastern Time Zone
for directory, info in manifest.items():
    print(f"Directory: {directory}")
    old_timestamps = set(old_manifest.get(directory, {}).get('timestamps', []))
    new_timestamps = set(info['timestamps'])
    added_timestamps = new_timestamps - old_timestamps
    for timestamp in added_timestamps:
        dt = datetime.fromtimestamp(timestamp / 1000, eastern)
        print(f"New date added: {dt.strftime('%Y-%m-%d %H:%M:%S %Z')}")


