#!/bin/bash

# Check if a filename was provided
if [ $# -eq 0 ]; then
    echo "Usage: $0 <filename>"
    exit 1
fi

# Assign the first argument as the filename
filename="$1"

# Check if the file exists
if [ ! -f "$filename" ]; then
    echo "File $filename does not exist"
    exit 1
fi

# Format the JSON file in place
cat "$filename" | json_pp > temp.json && mv temp.json "$filename"
