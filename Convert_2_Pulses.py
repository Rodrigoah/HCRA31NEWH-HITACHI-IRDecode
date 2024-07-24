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
            if current_value == 1:
                durations.append(round(count/sampling_frequency_mhz))
            else:
                durations.append(-round(count/sampling_frequency_mhz))
            current_value = sample
            count = 1
   # durations.append((current_value, count))  # Append the last run
    durations = durations[1:]
    return durations

# Function to parse durations

def parse_durations(durations):
    parsed_durations = []
    
    #for duration in durations:
        #if abs(duration)<2000:
            #regular pulse
            
    
    return parsed_durations

# Function to find pulses and decode frames


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


def plot_signal(signal):
    """
    Plots a signal where each position in the vector represents the length in time.
    
    Parameters:
    signal (list of int): The input signal where each value represents the length in time.
                          Positive values indicate '1' and negative values indicate '0'.
    """
    # Initialize variables
    time = 0
    times = []
    values = []

    # Loop through the signal to create the time and value arrays
    for duration in signal:
        # Determine the value (1 or 0)
        value = 1 if duration > 0 else 0
        # Append the start time and value
        times.append(time)
        values.append(value)
        # Increment time by the absolute duration
        time += abs(duration)
        # Append the end time and value
        times.append(time)
        values.append(value)

    # Convert time from microseconds to seconds for plotting
    times = np.array(times) / 1e6

    # Plot the signal
    plt.figure(figsize=(10, 2))
    plt.step(times, values, where='post')
    plt.ylim(-0.5, 1.5)
    plt.xlabel('Time (s)')
    plt.ylabel('Signal')
    plt.title('Signal Plot')
    plt.grid(True)
    plt.show()
    
def plot_signal_24mhz(signal):
    """
    Plots a signal sampled at 24 MHz.
    
    Parameters:
    signal (list of int): The input signal sampled at 24 MHz, consisting of 0s and 1s.
    """
    # Calculate the time for each sample
    sample_period = 1 / 24e6  # 1/24 MHz = 41.67 nanoseconds
    times = np.arange(0, len(signal) * sample_period, sample_period)

    # Plot the signal
    plt.figure(figsize=(10, 2))
    plt.step(times, signal, where='post')
    plt.ylim(-0.5, 1.5)
    plt.xlabel('Time (s)')
    plt.ylabel('Signal')
    plt.title('Signal Plot at 24 MHz')
    plt.grid(True)
    plt.show()

# Example usage
def compute_pulse_statistics(durations):
    """
    Computes statistics for different types of pulse durations.
    
    Parameters:
    durations (list of int): The input durations of pulses, where:
                             - Negative values around 600 represent low pulses
                             - Positive values around 600 represent logic lows
                             - Positive values around 1700 represent highs
    
    Returns:
    dict: A dictionary with the average and standard deviation for each category.
    """
    low_pulses = [d for d in durations if d < 0 and abs(d) >= 500 and abs(d) <= 700]
    logic_lows = [d for d in durations if d > 0 and d >= 500 and d <= 700]
    logic_highs = [d for d in durations if d > 0 and d >= 1500 and d <= 1900]

    stats = {}
    
    if low_pulses:
        stats['low_pulses'] = {
            'average': np.mean(low_pulses),
            'std_dev': np.std(low_pulses),
            'max': np.max(low_pulses),
            'min': np.min(low_pulses)
        }
    else:
        stats['low_pulses'] = {
            'average': None,
            'std_dev': None
        }
        
    if logic_lows:
        stats['logic_lows'] = {
            'average': np.mean(logic_lows),
            'std_dev': np.std(logic_lows),
            'max': np.max(logic_lows),
            'min': np.min(logic_lows)
        }
    else:
        stats['logic_lows'] = {
            'average': None,
            'std_dev': None
        }
    
    if logic_highs:
        stats['logic_highs'] = {
            'average': np.mean(logic_highs),
            'std_dev': np.std(logic_highs),
            'max': np.max(logic_highs),
            'min': np.min(logic_highs)
            
        }
    else:
        stats['logic_highs'] = {
            'average': None,
            'std_dev': None
        }
    
    return stats


def Parse_Durations_2_BIN(durations):
    Low_duration = 600
    Logic_High_duration = 1600
    Logic_Low_duration = 600
    Decoded_BIN = []
    
    for position in range(len(durations) - 1):
        current_duration = durations[position]
        next_duration = durations[position + 1]
        
        if current_duration < 0:
            # If the current duration is low level
            if 1675 < next_duration < 1710:
                Decoded_BIN.append(1)
            elif 515 < next_duration <  610:
                Decoded_BIN.append(0)
            elif 7990 < next_duration <  8050:
                Decoded_BIN.append('Long pulse:'+ str(next_duration))
                
            
            else:
                Decoded_BIN.append("Error pulse + " + str(next_duration))
        #else:
            # If the current duration is high level
            #if current_duration > Logic_High_duration * 1.1:
                #Decoded_BIN.append(current_duration)
    
    return Decoded_BIN

def Parse_BIN_Words (Binary):
    
    words = []
    Word_lengths = [48,64,56]
    word_number=0
    Position=0
    print("good")
    for length in Word_lengths:
        words.append([None] * length)
    for Bit in Binary[1:]:
        print(Bit)
        if Bit == 0 or Bit == 1:
            words[Position][word_number]=Bit
            Position +=1
        else:
            word_number += 1
            Position=0
            
    
    return words


# Main function to execute the workflow
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

                        durations = parse_samples(samples)
                        plot_signal(durations)
                        #plot_signal_24mhz(samples)
                        stats = compute_pulse_statistics(durations)
                        Binary=Parse_Durations_2_BIN(durations)
                        Words=Parse_BIN_Words(Binary)
                        

                        # Write the filename and decoded signals in a new line
        
        print(f"Decoded signals have been written to {output_file_path}")

except FileNotFoundError as fnf_error:
        print(fnf_error)
except Exception as e:
        print(f"An error occurred: {e}")



