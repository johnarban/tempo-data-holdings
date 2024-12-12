#!/bin/bash

# Function to commit and push files in chunks
commit_push_chunk() {
    local i=$1
    local chunk_size=$2
    # Get current branch
    current_branch=$(git rev-parse --abbrev-ref HEAD)
    
    # echo "Committing chunk $i of $total_chunks..."
    # echo "$@"
    # Add modified files to stage using $@
    # git add "$@"
    echo "$@" | tr ' ' '\n' | while read -r file; do
    # check the file exists
    if [ -f "$file" ]; then
        git add "$file"
        # echo "Adding $file to stage..."
    fi
    
done

    
    # # Commit changes
    git commit -m "Commit $i of $total_chunks"
    
    # # Push changes to remote
    git push origin "$current_branch"
}

# Main function
main() {
    # Set chunk size (adjust as needed)
    chunk_size=150
    
    echo "Processing commits in chunks..."
    
    # Count total number of modified files
    total_modified_files=$(git diff --name-only --diff-filter=M | wc -l)
    
    # Calculate total number of chunks
    total_chunks=$((total_modified_files / chunk_size + 1))
    
    for i in $(seq 1 $total_chunks); do
        echo "Processing chunk $i of $total_chunks"
        
        # Find modified files for this chunk
        modified_files=$(git diff --name-only --diff-filter=M | head -n $((i * chunk_size)) | tail -n $chunk_size)
        
        # Call commit_push_chunk function with specific files
        commit_push_chunk $i $chunk_size "$modified_files"
        
        echo "Press 'y' to continue to the next step, or 'n' to exit:"
        read -p "> " input
        
        case $input in
            y) i=$((i + 1));;
            n) echo "Exiting script."; exit 0;;
            *) echo "Invalid input. Please enter 'y' or 'n'.";;
        esac
    done
    
    echo "All chunks processed successfully!"
}

# Trap Ctrl+C and Cmd+C interrupts
trap 'echo "Interrupt received. Finishing current commit..."; git add "$@"; git commit -m "Interrupted commit"; git push origin "$current_branch"; exit 0' SIGINT

# Run main function
main
