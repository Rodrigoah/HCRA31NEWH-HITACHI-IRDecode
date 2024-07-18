import csv
import numpy as np
import os

# Define the sampling frequency
sampling_frequency_mhz = 24
sampling_frequency_hz = sampling_frequency_mhz * 1e6

# Timing criteria in seconds
low_duration = 570e-6  # 570 microseconds
high_duration_0 = 600e-6  # 600 microseconds for logic 0
high_duration_1 = 1686e-6  # 1686 microseconds for logic 1
pulse_4505us = 4505e-6  # 4505 microseconds
pulse_8007us = 8007e-6  # 8007 microseconds

# Convert durations to sample counts
low_samples = int(low_duration * sampling_frequency_hz)
high_samples_0 = int(high_duration_0 * sampling_frequency_hz)
high_samples_1 = int(high_duration_1 * sampling_frequency_hz)
pulse_4505_samples = int(pulse_4505us * sampling_frequency_hz)
pulse_8007_samples = int(pulse_8007us * sampling_frequency_hz)

# Frame lengths
first_frame_bits = 48
second_frame_bits = 64
third_frame_bits = 56

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

# Function to decode a frame
def decode_frame(durations, bit_count):
    binary_values = []
    i = 0
    while len(binary_values) < bit_count and i < len(durations) - 1:
        if durations[i][0] == 0 and low_samples * 0.9 <= durations[i][1] <= low_samples * 1.1:
            if high_samples_0 * 0.9 <= durations[i+1][1] <= high_samples_0 * 1.1:
                binary_values.append(0)
                i += 2
            elif high_samples_1 * 0.9 <= durations[i+1][1] <= high_samples_1 * 1.1:
                binary_values.append(1)
                i += 2
            else:
                i += 1
        else:
            i += 1
    return binary_values, i

# Function to find pulses and decode frames
def find_pulses_and_decode(durations):
    decoded_signals = []
    i = 0
    while i < len(durations):
        # Detect the first pulse of 4505us
        if durations[i][0] == 1 and pulse_4505_samples * 0.9 <= durations[i][1] <= pulse_4505_samples * 1.1:
            # Decode the first frame of 48 bits
            frame, index = decode_frame(durations[i+1:], first_frame_bits)
            decoded_signals.append(frame)
            i += index + 1
        # Detect the second pulse of 8007us
        elif durations[i][0] == 1 and pulse_8007_samples * 0.9 <= durations[i][1] <= pulse_8007_samples * 1.1:
            # Decode the second frame of 64 bits
            frame, index = decode_frame(durations[i+1:], second_frame_bits)
            decoded_signals.append(frame)
            i += index + 1
        # Detect the third pulse of 8007us
        elif durations[i][0] == 1 and pulse_8007_samples * 0.9 <= durations[i][1] <= pulse_8007_samples * 1.1:
            # Decode the third frame of 56 bits
            frame, index = decode_frame(durations[i+1:], third_frame_bits)
            decoded_signals.append(frame)
            i += index + 1
        else:
            i += 1
    return decoded_signals

# Function to calculate statistics
def calculate_statistics(durations):
    low_durations = [duration[1] for duration in durations if duration[0] == 0]
    high_durations = [duration[1] for duration in durations if duration[0] == 1]
    
    avg_low = np.mean(low_durations) * 1e6 / sampling_frequency_hz
    std_low = np.std(low_durations) * 1e6 / sampling_frequency_hz
    
    short_high_durations = [duration for duration in high_durations if high_samples_0 * 0.9 <= duration <= high_samples_0 * 1.1]
    long_high_durations = [duration for duration in high_durations if high_samples_1 * 0.9 <= duration <= high_samples_1 * 1.1]
    
    avg_short_high = np.mean(short_high_durations) * 1e6 / sampling_frequency_hz if short_high_durations else 0
    avg_long_high = np.mean(long_high_durations) * 1e6 / sampling_frequency_hz if long_high_durations else 0
    
    return avg_low, std_low, avg_short_high, avg_long_high

# Function to prompt for folder selection
def select_folder():
    import tkinter as tk
    from tkinter import filedialog

    root = tk.Tk()
    root.withdraw()  # Hide the root window
    folder_path = filedialog.askdirectory(title="Select Folder")
    
    if not folder_path:
        raise FileNotFoundError("No folder selected.")
    
    return folder_path

# Main function to execute the workflow
def main():
    try:
        # Prompt user to select a folder
        folder_path = select_folder()

        # Prepare the output file path
        output_file_path = os.path.join(folder_path, "decoded_signals.txt")

        with open(output_file_path, 'w') as output_file:
            # Iterate over all files in the folder and subfolders
            for root, _, files in os.walk(folder_path):
                for file_name in files:
                    if file_name.endswith('.csv'):
                        file_path = os.path.join(root, file_name)

                        # Read samples from the CSV file
                        samples = read_csv(file_path)

                        # Parse samples to get durations of 1s and 0s
                        durations = parse_samples(samples)

                        # Find pulses and decode frames
                        decoded_signals = find_pulses_and_decode(durations)

                        # Write the filename and decoded signals in a new line
                        output_file.write(f"{file_name} - ")
                        for i, binary_values in enumerate(decoded_signals):
                            binary_str = ''.join(map(str, binary_values))
                            if i > 0:
                                output_file.write('\t')
                            output_file.write(binary_str)
                        output_file.write('\n')
        
        print(f"Decoded signals have been written to {output_file_path}")

    except FileNotFoundError as fnf_error:
        print(fnf_error)
    except Exception as e:
        print(f"An error occurred: {e}")
        # Calculate and print statistics
        avg_low, std_low, avg_short_high, avg_long_high = calculate_statistics(durations)
        print(f"Average low pulse duration: {avg_low:.2f} microseconds")
        print(f"Standard deviation of low pulse durations: {std_low:.2f} microseconds")
        print(f"Average high short pulse duration: {avg_short_high:.2f} microseconds")
        print(f"Average high long pulse duration: {avg_long_high:.2f} microseconds")

if __name__ == "__main__":
    main()
