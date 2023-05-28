import os
import filecmp
import subprocess
import numpy
import re
import time

tests_folder = r"testsDiscord"
results_folder = r"outputs"
bimaru_script = r"bimaru.py"
errors_in_tests = []

def group_chars(string):
    string = string.replace('\n', '')  # Remove newline characters
    char_list = [string[i * 10 : i * 10 + 10] for i in range(0, 10)]  # Split into 10-character chunks
    matriz = []
    for f in char_list:
        matriz.append([val for val in f])
    return matriz

def check_result_is_good(test_file_path, thing):
    with open(test_file_path, "r") as k:
        lines = k.readlines()

    if len(thing.replace("\n", "")) < 100:
        return False

    matriz = group_chars(thing)
    # Extract the data from each line
    row_data = list(map(int, lines[0].split("\t")[1:]))
    column_data = list(map(int, lines[1].split("\t")[1:]))
    hints = []
    for line in lines[3:]:
        hint_data = line.split("\t")[1:]
        hints.append((int(hint_data[0]), int(hint_data[1]), hint_data[2].strip()))

    for y in range(10):
        nr = 0
        for r_value in matriz[y]:
            if r_value not in (".", "W"):
                nr += 1
        if nr != row_data[y]:
            return False

        nc = 0
        for z in range(10):
            if matriz[z][y] not in (".", "W"):
                nc += 1
        if nc != column_data[y]:
            return False

        for hint in hints:
            if hint[2] != matriz[hint[0]][hint[1]]:
                return False
        return True

# Create the results folder if it doesn't exist
if not os.path.exists(results_folder):
    os.makedirs(results_folder)

# Iterate over files in the tests folder
for file_name in os.listdir(tests_folder):
    if file_name.endswith(".txt"):
        test_file_path = os.path.join(tests_folder, file_name)
        output_file_path = os.path.join(results_folder, file_name.replace(".txt", ".out"))
        # Execute the bimaru.py script with the test file as input
        start_time = time.time()
        result = subprocess.run(["python", bimaru_script], input=open(test_file_path, 'rb').read(),
                       stdout=open(output_file_path, "w", newline=""))
        end_time = time.time()
        if result.returncode != 0:
            errors_in_tests.append(file_name)
        print(f"{file_name}: Executed in {end_time - start_time} seconds")

print("\n\n\nList of Inputs")

# Compare the output files in the results and tests folders
for file_name in os.listdir(tests_folder):
    if file_name.endswith(".txt"):
        test_file_path = os.path.join(tests_folder, file_name)
        output_file_path = os.path.join(results_folder, file_name.replace(".txt", ".out"))
        test_result_file_path = test_file_path.replace(".txt", ".out")

        # Check if it had an error during the process
        if file_name in errors_in_tests:
            print(f"{file_name}: Something went wrong during the process")
        # Compare the output file with the corresponding file in the tests folder
        else:
            with open(output_file_path, "r") as output_file, open(test_result_file_path, "r") as test_file:
                output_content = output_file.read()
                test_content = test_file.read()

            if re.split(r'(\s+)', test_content) == re.split(r'(\s+)', output_content):
                print(f"{file_name}: Output matches")
            else:
                if check_result_is_good(test_file_path, output_content):
                    print(f"{file_name}: Output does not match but respects the rules")
                else:
                    print(f"{file_name}: Output does not match")


    """elif filecmp.cmp(output_file_path, test_result_file_path):
            print(f"{file_name}: Output matches")
        else:
            print(f"{file_name}: Output does not match")"""
