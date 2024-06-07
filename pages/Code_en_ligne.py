import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import welch

def apply_RZ(binary_sequence, Ts):
    rz_sequence = []
    for bit in binary_sequence:
        if bit == 1:
            rz_sequence.extend([1] * (Ts // 2) + [0] * (Ts // 2))
        else:
            rz_sequence.extend([0] * Ts)
    return rz_sequence

def apply_NRZ(binary_sequence, Ts):
    nrz = [0]
    for bit in binary_sequence:
            nrz.extend([1, -1] if bit == 0 else [-1, 1])
    return nrz

def apply_Miller(binary_sequence, Ts):
    miller_sequence = []
    current_level = 1
    for bit in binary_sequence:
        if bit == 1:
            current_level = -current_level
            miller_sequence.extend([current_level] * (Ts // 2))
            current_level = -current_level
            miller_sequence.extend([current_level] * (Ts // 2))
        else:
            miller_sequence.extend([current_level] * Ts)
    return miller_sequence

def apply_Manchester(binary_sequence, Ts):
    manchester_sequence = []
    for bit in binary_sequence:
        manchester_sequence.extend([1, -1] if bit == 1 else [-1, 1])
    return np.repeat(manchester_sequence, Ts // 2)

def apply_HDBN(binary_sequence, Ts, order):
    hdbn_sequence = []
    zero_count = 0
    previous_pulse = -1

    for bit in binary_sequence:
        if bit == 0:
            zero_count += 1
            if zero_count == order:
                hdbn_sequence.extend([0] * (Ts - 1) + [1])
                zero_count = 0
            else:
                hdbn_sequence.extend([0] * Ts)
        else:
            if zero_count >= order:
                zero_count = 0
            previous_pulse = -previous_pulse
            hdbn_sequence.extend([previous_pulse] * Ts)
    return hdbn_sequence

# def plot_signal(signal, title, period_ms):
#     t = np.linspace(0, len(signal) * period_ms / len(signal), len(signal))
#     plt.figure(figsize=(10, 4))
#     plt.plot(t, signal)
#     plt.title(title)
#     plt.xlabel('Time (ms)')
#     plt.ylabel('Amplitude')
#     plt.xlim(0, 1000)  # Set x-axis limit from 0 to 1000 ms
#     plt.grid(True)
#     st.pyplot()

def plot_signal(signal, title, period_ms):
    t = np.linspace(0, len(signal) * period_ms / len(signal), len(signal) + 1)  # Add one extra point for step plot
    plt.figure(figsize=(10, 4))
    plt.step(t, np.hstack((signal, signal[-1])), where='post')  # Use step plot
    plt.title(title)
    plt.xlabel('Time (ms)')
    plt.ylabel('Amplitude')
    plt.xlim(0, 1000)  # Set x-axis limit from 0 to 1000 ms
    plt.grid(True)
    st.pyplot()



def plot_dsp(signal, fs):
    freqs, psd = welch(signal, fs, nperseg=1024)
    plt.figure(figsize=(10, 4))
    plt.semilogy(freqs, psd)
    plt.title('Power Spectral Density')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Power/Frequency (dB/Hz)')
    plt.grid(True)
    st.pyplot()

st.title("Binary Transmission with Filters")

filter_type = st.selectbox("Select filter type:", ["RZ", "NRZ", "Miller", "Manchester", "HDBN"])

if filter_type == "HDBN":
    hdbn_order = st.number_input("HDBN Filter Order", min_value=1, step=1, value=3)
else:
    hdbn_order = 3

filename = "binary_sequence_and_period.txt"
try:
    with open(filename, 'r') as file:
        lines = file.readlines()[1:]  # Skip the first line (header)
        binary_sequence = []
        for line in lines:
            try:
                binary_sequence.append(int(line.split()[0]))
            except ValueError:
                st.warning(f"Skipping non-numeric value: {line.split()[0]}")
        period_ms = float(lines[0].split()[1])
except Exception as e:
    st.error("An error occurred while reading the file: {}".format(e))
    binary_sequence = [1, 0, 1, 1, 0]
    period_ms = 100

fs = 1000  # Sampling rate in Hz
Ts = int(fs * period_ms / 1000)  # Period in samples

if filter_type == "RZ":
    filtered_sequence = apply_RZ(binary_sequence, Ts)
elif filter_type == "NRZ":
    filtered_sequence = apply_NRZ(binary_sequence, Ts)
elif filter_type == "Miller":
    filtered_sequence = apply_Miller(binary_sequence, Ts)
elif filter_type == "Manchester":
    filtered_sequence = apply_Manchester(binary_sequence, Ts)
elif filter_type == "HDBN":
    filtered_sequence = apply_HDBN(binary_sequence, Ts, hdbn_order)

# Assemble the binary sequence into a single string
binary_sequence_str = ''.join(map(str, binary_sequence))

# Display the original binary sequence
st.write("Original Binary Sequence:", binary_sequence_str)

# Plot original binary sequence
plot_signal(binary_sequence, 'Original Binary Sequence', 1000)

# Plot filtered sequence
plot_signal(filtered_sequence, f'Filtered Sequence ({filter_type})', 1000)
