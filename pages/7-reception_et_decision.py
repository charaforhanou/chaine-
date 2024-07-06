import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

def read_signal(filename):
    """Reads the signal from a file."""
    try:
        signal_data = np.loadtxt(filename)
        return signal_data
    except Exception as e:
        st.error(f"Error reading the file: {e}")
        return np.array([])

def detect_period(demodulated_signal, sampling_rate):
    """Detects the period of the NRZ signal from the demodulated signal."""
    peaks, _ = find_peaks(np.abs(demodulated_signal), height=np.max(np.abs(demodulated_signal)) * 0.5)
    if len(peaks) > 1:
        periods = np.diff(peaks) / sampling_rate
        average_period = np.mean(periods)
    else:
        average_period = None
    return average_period, peaks

def read_binary_sequence_and_period(filename):
    """Reads binary sequence and period from a file."""
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()[1:]  # Skip the first line (header)
            binary_sequence = []
            periods = []
            for line in lines:
                try:
                    value, period = line.split()
                    binary_sequence.append(int(value))
                    periods.append(float(period))
                except ValueError:
                    st.warning(f"Skipping line with invalid format: {line.strip()}")
    except Exception as e:
        st.error(f"An error occurred while reading the file: {e}")
        return [], 0

    if len(set(periods)) == 1:
        return binary_sequence, periods[0]  # Return the sequence and the consistent period
    else:
        st.error("The periods in the file are not consistent.")
        return [], 0

def extract_binary_sequence(demodulated_signal, period, sampling_rate):
    """Extracts the binary sequence from the demodulated signal based on the detected period."""
    binary_sequence = []
    step = int(period * sampling_rate)
    for i in range(0, len(demodulated_signal), step):
        segment = demodulated_signal[i:i+step]
        if len(segment) > 0:
            bit = 1 if np.mean(segment) > 0 else 0
            binary_sequence.append(bit)
    return binary_sequence

def nyquist_filter(binary_sequence, period, sampling_rate):
    """Generates a Nyquist filtered signal based on binary sequence."""
    t = np.arange(0, len(binary_sequence) * period, 1 / sampling_rate)
    nyquist_signal = np.zeros_like(t)

    for i, bit in enumerate(binary_sequence):
        if bit == 1:
            nyquist_signal[i * int(sampling_rate * period):(i + 1) * int(sampling_rate * period)] = 1
        else:
            nyquist_signal[i * int(sampling_rate * period):(i + 1) * int(sampling_rate * period)] = -1

    return nyquist_signal

def main():
    st.title("NRZ Signal Detection and Binary Sequence Extraction")

    filename = 'saved_demodulated_signal.txt'
    sampling_rate = st.number_input("Sampling Rate (Hz)", min_value=100, step=100, value=1000)

    demodulated_signal = read_signal(filename)
    
    if demodulated_signal.size == 0:
        st.write("Unable to read the demodulated signal.")
        return

    # Plot the demodulated signal
    t = np.arange(len(demodulated_signal)) / sampling_rate
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(t, demodulated_signal, label='Demodulated Signal')
    ax.set_title("Demodulated Signal")
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Amplitude")
    ax.legend()
    st.pyplot(fig)
    
    binary_sequence, period = read_binary_sequence_and_period("binary_sequence_and_period.txt")
    detected_period, peaks = detect_period(demodulated_signal, sampling_rate)

    if detected_period is not None:
        st.write(f"Detected Period: {detected_period:.4f} s")
    else:
        st.write("Unable to detect the period of the signal.")
        return

    # Apply Nyquist filter based on binary sequence
    nyquist_signal = nyquist_filter(binary_sequence, period, sampling_rate)
    
    # Generate time vector for Nyquist signal
    t_nyquist = np.arange(0, len(nyquist_signal)) / sampling_rate

    # Plot the NRZ signal
    nrz_signal = read_signal("nrz_signal.txt")
    t_nrz = np.arange(len(nrz_signal)) / sampling_rate
    # fig, ax = plt.subplots(figsize=(12, 6))
    # ax.plot(t_nrz, nrz_signal, label='NRZ Signal')
    # ax.set_title("NRZ Signal")
    # ax.set_xlabel("Time (s)")
    # ax.set_ylabel("Amplitude")
    # ax.legend()
    # st.pyplot(fig)

    # Plot the Nyquist filtered signal
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(t_nyquist, nyquist_signal, label='Nyquist Filtered Signal')
    ax.set_title("Nyquist Filtered Signal")
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Amplitude")
    ax.legend()
    st.pyplot(fig)

    # Display the binary sequence
    st.write(f"Binary Sequence: {binary_sequence}")

if __name__ == "__main__":
    main()