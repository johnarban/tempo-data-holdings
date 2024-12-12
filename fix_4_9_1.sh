#!/bin/bash

# Find all files with the pattern "*4_9_1*"
find . -name "*4_9_1*" | while read -r file; do
  # Generate the new file name by replacing '_4_9_1.png' with '.png'
  new_file=$(echo "$file" | sed 's/_4_9_1\.png$/.png/')
  
  # Rename the file
  mv "$file" "$new_file"
# echo "$file" to "$new_file"
done