import pandas as pd
import tkinter as tk
from tkinter import filedialog
import matplotlib.pyplot as plt

def open_file_dialog():
    # Create a Tkinter root window
    root = tk.Tk()
    root.withdraw()  # Hide the root window

    # Open the file dialog
    file_path = filedialog.askopenfilename(
        filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
    )
    
    if file_path:
        # Read the CSV file into a pandas dataframe
        data = pd.read_csv(file_path)
        return data
    else:
        print("No file selected.")
        return None

def decode_logic_values(data, sample_rate):
    logic_values = data['logic'].tolist()  # Convert the logic column to a list
    
    bit_values = []
    bit_durations = []
    current_value = logic_values[0]
    count = 0
    ignore_pulse_duration_us = 4500  # Duration of the pulse to ignore in microseconds

    # Define pulse durations in microseconds
    low_pulse_duration_us = 600
    high_pulse_duration_us = 1687

    # Convert pulse durations to sample counts
    low_pulse_samples = int(low_pulse_duration_us * sample_rate / 1e6)
    high_pulse_samples = int(high_pulse_duration_us * sample_rate / 1e6)

    bit_start_indices = []  # List to store the start indices of bits
    current_index = 0  # Current index in the logic values list
    ignore_samples = int(ignore_pulse_duration_us * sample_rate / 1e6)  # Convert ignore duration to samples

    # Skip the initial ignore pulse
    while current_index < len(logic_values) and ignore_samples > 0:
        current_index += 1
        ignore_samples -= 1

    for value in logic_values[current_index:]:
        if value == current_value:
            count += 1
        else:
            if current_value == 0:  # Assuming 0 represents a low pulse
                if low_pulse_samples * 0.9 <= count <= low_pulse_samples * 1.1:
                    bit_values.append(0)
                    bit_durations.append(count / sample_rate * 1e6)  # Convert to microseconds
                    bit_start_indices.append(current_index - count)
            elif current_value == 1:  # Assuming 1 represents a high pulse
                if high_pulse_samples * 0.9 <= count <= high_pulse_samples * 1.1:
                    bit_values.append(1)
                    bit_durations.append(count / sample_rate * 1e6)  # Convert to microseconds
                    bit_start_indices.append(current_index - count)
            current_value = value
            count = 1
        
        current_index += 1

    # Check the last pulse
    if current_value == 0 and low_pulse_samples * 0.9 <= count <= low_pulse_samples * 1.1:
        bit_values.append(0)
        bit_durations.append(count / sample_rate * 1e6)
        bit_start_indices.append(current_index - count)
    elif current_value == 1 and high_pulse_samples * 0.9 <= count <= high_pulse_samples * 1.1:
        bit_values.append(1)
        bit_durations.append(count / sample_rate * 1e6)
        bit_start_indices.append(current_index - count)

    return bit_values, bit_durations, bit_start_indices

def convert_to_hex(bit_values):
    # Convert bit values to hexadecimal string
    hex_string = ""
    for i in range(0, len(bit_values), 4):
        # Take 4 bits at a time and convert to hexadecimal
        bits = bit_values[i:i+4]
        hex_digit = hex(int("".join(map(str, bits)), 2))[2:]  # Convert binary to hex
        hex_string += hex_digit.upper()  # Append to hex string
    
    return hex_string

def plot_signal_with_bits(data, bit_start_indices, bit_values, bit_durations):
    logic_values = data['logic'].tolist()
    
    plt.figure(figsize=(12, 6))
    plt.plot(logic_values, label='Logic Signal')

    # Plot each bit with its duration and add duration annotations
    for i, bit_start in enumerate(bit_start_indices):
        color = 'g' if bit_values[i] == 1 else 'b'  # Green for high (1), blue for low (0)
        plt.axvline(x=bit_start, color=color, linestyle='-', label='Bit Start' if i == 0 else "")
        plt.text(bit_start, 1.1, f'{bit_durations[i]:.1f} µs', color=color, fontsize=10, ha='center', va='bottom')  # Add duration annotation
        
        if bit_values[i] == 1:  # Only annotate for high pulses
            plt.text(bit_start + bit_durations[i] / 2, 0.5, f'{bit_durations[i]:.1f} µs', color='k', fontsize=8, ha='center', va='center')  # Add duration annotation in the center of high pulse

        plt.text(bit_start, -0.1, f'{bit_values[i]}', color=color, fontsize=10, ha='center', va='top')  # Mark bit value

    plt.xlabel('Sample Index')
    plt.ylabel('Logic Level')
    plt.title('Logic Signal with Bit Markings and Durations')
    plt.ylim(-0.5, 1.5)  # Set y-axis limits to make space for annotations
    plt.legend()
    plt.grid(True)
    plt.show()

# Open the file dialog and read the CSV file
data = open_file_dialog()

if data is not None:
    # Define the sample rate (in Hz)
    sample_rate = 24e6  # 24 MHz
    
    # Decode the logic values and get bit values, durations, and start indices
    bit_values, bit_durations, bit_start_indices = decode_logic_values(data, sample_rate)
    
    # Print the bit values and durations
    print("Bit Values:", bit_values)
    print("Bit Durations (in µs):", bit_durations)
    
    # Convert bit values to hexadecimal
    hex_string = convert_to_hex(bit_values)
    print("Hexadecimal Representation:", hex_string)
    
    # Plot the signal with vertical bars where the bits start and add duration annotations
    plot_signal_with_bits(data, bit_start_indices, bit_values, bit_durations)
else:
    print("Failed to load data.")
