#!/bin/bash

# Directory where the original images are located
inputDir="."
# Directory where the resized images will be saved
outputDir="./resized_images"

# Create the output directory if it doesn't exist
mkdir -p "$outputDir"

# Count the total number of PNG files in the input directory
totalFiles=$(ls "$inputDir"/*.png | wc -l)

# Initialize variables for tracking progress
currentFile=0
percentageComplete=0

# Function to update the progress bar
updateProgressBar() {
  local percent=$1
  local cols=$(tput cols)
  local width=$((cols - 8))
  local filledWidth=$((width * percent / 100))
  local emptyWidth=$((width - filledWidth))

  printf '\r['
  printf '%*s' "$filledWidth" | tr ' ' '='
  printf '%*s' "$emptyWidth"
  printf '] %3d%%' "$percent"
}

# Iterate over each PNG file in the input directory
for img in "$inputDir"/*.png; do
  # Increment the current file counter
  ((currentFile++))

  # Calculate the percentage of completion
  percentageComplete=$(( ($currentFile * 100) / $totalFiles ))

  # Update the progress bar
  updateProgressBar $percentageComplete

  # Use convert to resize the image and save it in the output directory
  # Assuming a 2.5 times reduction in resolution, adjust the resize parameters accordingly
  convert "$img" -sample 40% -channel alpha -threshold 25% "$outputDir/${img##*/}"

  # Clear the progress bar after updating it
  printf "\033[2K\r"
  
done

echo -e "\nDone!"
