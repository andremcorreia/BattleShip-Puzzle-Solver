#!/bin/bash

# Loop through instance files
for instance_file in instance*.txt; do
    # Get the instance number from the file name
    instance_number="${instance_file%%.*}"
    instance_number="${instance_number#instance}"

    # Run the command and redirect input from instance file
    IFS= read -r -d '' output < <(py bimaru.py < "$instance_file")

    # Remove Windows return characters
    output=$(echo "$output" | tr -d '\r')
    expected_output=$(echo "$expected_output" | tr -d '\r')


    # Compare the output with the respective .out file
    expected_output_file="instance${instance_number}.out"
    expected_output=$(cat "$expected_output_file")

    if [[ "$output" != "$expected_output" ]]; then
        # Output and expected output differ, create a .diff file
        diff_file="instance${instance_number}.diff"
        echo "Output differs for $instance_file. Creating $diff_file..."
        echo "--- Output ---" > "$diff_file"
        echo "$output" >> "$diff_file"
        echo "--- Expected Output ---" >> "$diff_file"
        echo "$expected_output" >> "$diff_file"
    else
        # Output and expected output are the same, ensure no .diff file exists
        diff_file="instance${instance_number}.diff"
        if [ -e "$diff_file" ]; then
            echo "Output matches for $instance_file. Removing $diff_file..."
            rm "$diff_file"
        fi
    fi
done
