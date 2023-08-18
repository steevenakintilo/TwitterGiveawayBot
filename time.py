import time
import subprocess

def measure_execution_time(program_path):
    start_time = time.time()
    subprocess.call(['python', program_path])
    end_time = time.time()

    execution_time = end_time - start_time
    return execution_time

# Provide the path to your Python program that you want to measure
program_path = 'main.py'

execution_time = measure_execution_time(program_path)
print(f"The program executed in {execution_time:.2f} seconds.")