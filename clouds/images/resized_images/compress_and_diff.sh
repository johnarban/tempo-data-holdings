#!/usr/bin/env bash

set -euo pipefail

# Directory where the original images are located
inputDir="."

# Directory where the compressed images will be saved
compressedDir="./compressed_images"

# Directory where the difference images will be saved
diffDir="./diff_images"

# Create the directories if they don't exist
# mkdir -p "$compressedDir"
# mkdir -p "$diffDir"

# Count the total number of PNG files in the input directory
totalFiles=$(ls "$inputDir"/*.png | wc -l)

# Initialize variables for tracking progress
count=0

# takes two strings which are filenames, then print out the file sizes in kB with no decimal, and the compression ratio two 2 decimal places
function print_file_size_and_compression_ratio() {
    local originalSize=$(stat -f%z "$1" )
    local compressedSize=$(stat -f%z "$2")
    # in kb
    originalSize=$(echo "scale=2; $originalSize/1024" | bc)
    compressedSize=$(echo "scale=2; $compressedSize/1024" | bc)
    ratio=$(echo "scale=2; $originalSize/$compressedSize" | bc)
    originalSize=$(echo "scale=0; $originalSize" | bc)
    compressedSize=$(echo "scale=0; $compressedSize" | bc)
    
    
    
    echo "  Original size: $originalSize kb to compressed size: $compressedSize kb"
    echo "  Ratio: $ratio"
}

# Loop through all the *.png files in the input directory
for file in "$inputDir"/*.png; do

    echo "Compressing $file"
    # Compress the image https://imagemagick.org/script/command-line-options.php#quality 
    # -quality 15 is (1) zlib compression level 1 with (5) adaptive filter)
    # convert "$file" -quality 15 "$compressedDir/${file##*/}"
    # convert "$file" -define png:compression-filter=5 -define png:compression-level=1 -define png:compression-strategy=3 "$compressedDir/${file##*/}"
    convert "$file" -define png:compression-filter=5 -define png:compression-level=1 -define png:compression-strategy=3 "$file"
    
    # Calculate the difference between the original and compressed images using imagemagick compare  # dev/null to suppress output
    # compare -verbose -metric AE "$file" "$compressedDir/${file##*/}" "$diffDir/${file##*/}" 2>/dev/null
    

    # Print out the file sizes and compression ratio
    # print_file_size_and_compression_ratio "$file" "$compressedDir/${file##*/}"
    
    
    # break after 10 files
    # count=$((count+1))
    # if [ $count -eq 2 ]; then
    #     break
    # fi

done