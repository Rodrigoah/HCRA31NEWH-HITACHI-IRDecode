input_file = 'G:\My Drive\Proyectos\HITACHI HCRA31NEWH\GIT\HCRA31NEWH-HITACHI-IRDecode\RAW Captures\FFO_COOL_30_AUTO\OFF_COOL_30_AUTO.csv'
import csv
import numpy as np

# Define the sampling frequency
sampling_frequency_mhz = 24
sampling_frequency_hz = sampling_frequency_mhz * 1e6

# Timing criteria in seconds
low_duration = 570e-6  # 570 microseconds
high_duration_0 = 600e-6  # 600 microseconds for logic 0
high_duration_1 = 1686e-6  # 1686 microseconds for logic 1
long_pulse_duration = 8e-3  # 8 milliseconds

# Convert durations to sample counts
low_samples = int(low_duration * sampling_frequency_hz)
high_samples_0 = int(high_duration_0 * sampling_frequency_hz)
high_samples_1 = int(high_duration_1 * sampling_frequency_hz)
long_pulse_samples = int(long_pulse_duration * sampling_frequency_hz)

# Function to read CSV file and ignore the first line
def read_csv(file_path):
    samples = []
    with open(file_path, mode='r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # Skip the first line
        for row in csv_reader:
            samples.append(int(row[0]))
    return samples

# Function to parse samples and note durations of 1s and 0s
def parse_samples(samples):
    durations = []
    current_value = samples[0]
    count = 0
    for sample in samples:
        if sample == current_value:
            count += 1
        else:
            durations.append((current_value, count))
            current_value = sample
            count = 1
    durations.append((current_value, count))  # Append the last run
    return durations

# Function to convert durations to binary values
def durations_to_binary(durations):
    binary_values = []
    current_binary_string = []
    
    i = 0
    while i < len(durations) - 1:
        if durations[i][0] == 0 and low_samples * 0.9 <= durations[i][1] <= low_samples * 1.1:
            if high_samples_0 * 0.9 <= durations[i+1][1] <= high_samples_0 * 1.1:
                current_binary_string.append(0)
                i += 2
            elif high_samples_1 * 0.9 <= durations[i+1][1] <= high_samples_1 * 1.1:
                current_binary_string.append(1)
                i += 2
            else:
                i += 1
        elif durations[i][0] == 1 and durations[i][1] > long_pulse_samples:
            if current_binary_string:
                binary_values.append(current_binary_string)
                current_binary_string = []
            i += 1
        else:
            i += 1
    
    if current_binary_string:
        binary_values.append(current_binary_string)
    
    return binary_values

# Function to convert binary strings to hexadecimal
def binary_to_hex(binary_string):
    hex_string = hex(int(binary_string, 2))[2:].upper()
    return hex_string

# File path for the new CSV file
new_input_file = 'G:\My Drive\Proyectos\HITACHI HCRA31NEWH\GIT\HCRA31NEWH-HITACHI-IRDecode\RAW Captures\ON_DRY_27_AUTO\ON_DRY_27_AUTO.csv'

# Read samples from the new input CSV
new_samples = read_csv(new_input_file)

# Parse samples to get durations of 1s and 0s
new_durations = parse_samples(new_samples)

# Convert durations to binary values
new_binary_values = durations_to_binary(new_durations)

# Print the binary values and their corresponding hex values
for i, binary_string in enumerate(new_binary_values):
    binary_str = ''.join(map(str, binary_string))
    hex_str = binary_to_hex(binary_str)
    print(f"Binary decoded signal {i + 1}: {binary_str}")
    print(f"Hex decoded signal {i + 1}: {hex_str}")
