import csv
import numpy as np
import os
import matplotlib.pyplot as plt

# Define the sampling frequency
sampling_frequency_mhz = 24
sampling_frequency_hz = sampling_frequency_mhz * 1e6

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
            if (count / sampling_frequency_mhz)>100:
                if current_value == 1:
                    durations.append(round(count / sampling_frequency_mhz))
                else:
                    durations.append(-round(count / sampling_frequency_mhz))
                current_value = sample
                count = 1
    durations = durations[1:]
    return durations

# Function to compute pulse statistics
def compute_pulse_statistics(durations):
    low_pulses = [d for d in durations if d < 0 and 500 <= abs(d) <= 700]
    logic_lows = [d for d in durations if d > 0 and 490 <= d <= 700]
    logic_highs = [d for d in durations if d > 0 and 1500 <= d <= 1900]

    stats = {
        'low_pulses': {'average': None, 'std_dev': None, 'max': None, 'min': None},
        'logic_lows': {'average': None, 'std_dev': None, 'max': None, 'min': None},
        'logic_highs': {'average': None, 'std_dev': None, 'max': None, 'min': None}
    }

    if low_pulses:
        stats['low_pulses'] = {
            'average': np.mean(low_pulses),
            'std_dev': np.std(low_pulses),
            'max': np.max(low_pulses),
            'min': np.min(low_pulses)
        }

    if logic_lows:
        stats['logic_lows'] = {
            'average': np.mean(logic_lows),
            'std_dev': np.std(logic_lows),
            'max': np.max(logic_lows),
            'min': np.min(logic_lows)
        }

    if logic_highs:
        stats['logic_highs'] = {
            'average': np.mean(logic_highs),
            'std_dev': np.std(logic_highs),
            'max': np.max(logic_highs),
            'min': np.min(logic_highs)
        }

    return stats

# Function to decode durations to binary values
def parse_durations_to_bin(durations, stats):
    decoded_bin = []
    for position in range(len(durations) - 1):
        current_duration = durations[position]
        next_duration = durations[position + 1]

        if current_duration < 0:
            if stats['logic_highs']['min'] <= next_duration <= stats['logic_highs']['max']:
                decoded_bin.append(1)
            elif stats['logic_lows']['min'] <= next_duration <= stats['logic_lows']['max']:
                decoded_bin.append(0)
            elif 7990 < next_duration < 8050:
                decoded_bin.append('Long pulse:' + str(next_duration))
            elif -2<next_duration<2:
                print(next_duration)
            else:
                decoded_bin.append("Error pulse2+ " + str(next_duration))
    return decoded_bin

def binary_to_reversed_hex(binary_list):
    """
    Converts a list of binary numbers to reversed hex bytes.
    
    Parameters:
    binary_list (list): A list of binary numbers (0 and 1).
    
    Returns:
    list: A list of reversed hex byte strings.
    """
    # Ensure the binary list is a multiple of 8
    if len(binary_list) % 8 != 0:
        raise ValueError("The length of the binary list must be a multiple of 8.")

    # Group the binary list into bytes (chunks of 8)
    bytes_list = [binary_list[i:i+8] for i in range(0, len(binary_list), 8)]

    reversed_hex_bytes = []

    for byte in bytes_list:
        # Reverse the byte
        reversed_byte = byte[::-1]
        # Convert the reversed byte to a string
        reversed_byte_str = ''.join(map(str, reversed_byte))
        # Convert the binary string to an integer
        reversed_byte_int = int(reversed_byte_str, 2)
        # Convert the integer to a hexadecimal string
        reversed_hex = format(reversed_byte_int, '02x')
        reversed_hex_bytes.append(reversed_hex)

    return reversed_hex_bytes

# Function to parse binary values to words
def parse_bin_to_words(binary):
    words = []
    word_lengths = [48, 64, 56]
    word_number = 0
    position = 0

    for length in word_lengths:
        words.append([None] * length)

    for bit in binary[1:]:
        if bit == 0 or bit == 1:
            words[word_number][position] = bit
            position += 1
        else:
            word_number += 1
            position = 0

    return words

# Function to write words to a text file
def write_words_to_file(file_name, words, file_path):
    def format_word(word):
        # Join the bits into a string
        word_str = ''.join(str(bit) for bit in word if bit is not None)
        # Add a space every 8 bits
        spaced_word_str = ' '.join(word_str[i:i+8] for i in range(0, len(word_str), 8))
        return spaced_word_str
    
    with open(file_path, 'a') as file:  # Open in append mode to add to the existing content
        file.write(file_name + ' - ' + '\t')
        for word in words:
            formatted_word = format_word(word)
            file.write(formatted_word + '\t')
        file.write('\n')

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

# Function to plot the signal
def plot_signal(signal):
    time = 0
    times = []
    values = []

    for duration in signal:
        value = 1 if duration > 0 else 0
        times.append(time)
        values.append(value)
        time += abs(duration)
        times.append(time)
        values.append(value)

    times = np.array(times) / 1e6

    plt.figure(figsize=(10, 2))
    plt.step(times, values, where='post')
    plt.ylim(-0.5, 1.5)
    plt.xlabel('Time (s)')
    plt.ylabel('Signal')
    plt.title('Signal Plot')
    plt.grid(True)
    plt.show()

def write_hex_to_file(file_name, reversed_hex, hex_file_path):
    with open(hex_file_path, 'a') as hex_file:
        hex_file.write(f"{file_name}: \t{reversed_hex}\n")

# Main function to execute the workflow
try:
    # Prompt user to select a folder
    folder_path = select_folder()

    # Prepare the output file path
    output_file_path = os.path.join(folder_path, "decoded_signals.txt")
    hex_file_path = os.path.join(folder_path, "hex_decoded_signals.txt")

    
    
    with open(output_file_path, 'w') as output_file:
        # Iterate over all files in the folder and subfolders
        for root, _, files in os.walk(folder_path):
            for file_name in files:
                if file_name.endswith('.csv'):
                    file_path = os.path.join(root, file_name)

                    # Read samples from the CSV file
                    samples = read_csv(file_path)

                    # Parse samples to durations
                    durations = parse_samples(samples)
                    plot_signal(durations)

                    # Compute pulse statistics
                    stats = compute_pulse_statistics(durations)

                    # Decode durations to binary values
                    binary = parse_durations_to_bin(durations, stats)
                    print("a")
                    # Parse binary values to words
                    words = parse_bin_to_words(binary)
                    print("b")
                    word=words[:][0]
                    word.extend(words[:][1])
                    word.extend(words[:][2])
                    # Write results to output file
                    reversed_hex = binary_to_reversed_hex(word)
                    print(file_name)
                    print(":")
                    print(reversed_hex)
                    write_words_to_file(file_name, words, output_file_path)
                    write_hex_to_file(file_name, reversed_hex, hex_file_path)

    print(f"Decoded signals have been written to {output_file_path}")

except FileNotFoundError as fnf_error:
    print(fnf_error)
except Exception as e:
    print(f"An error occurred: {e}")
    print(file_name)
