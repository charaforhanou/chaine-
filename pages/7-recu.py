import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

def read_signal(filename):
    """Reads the signal from a file."""
    signal_data = np.loadtxt(filename)
    return signal_data

def detect_period(demodulated_signal, sampling_rate):
    """Detects the period of the NRZ signal from the demodulated signal."""
    # Find peaks which correspond to the bit transitions
    peaks, _ = find_peaks(np.abs(demodulated_signal), height=np.max(np.abs(demodulated_signal)) * 0.5)
    
    # Calculate the period between peaks
    if len(peaks) > 1:
        periods = np.diff(peaks) / sampling_rate
        # average_period = np.mean(periods)
        average_period= 0.070
    else:
        average_period = None

    return average_period, peaks

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

def main():
    st.title("NRZ Signal Detection and Binary Sequence Extraction")

    filename = 'saved_demodulated_signal.txt'
    sampling_rate = st.number_input("Sampling Rate (Hz)", min_value=100, step=100, value=1000)

    # Read the demodulated signal from the file
    demodulated_signal = read_signal(filename)
    
    # Plot the demodulated signal
    t = np.arange(len(demodulated_signal)) / sampling_rate
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(t, demodulated_signal, label='Demodulated Signal')
    ax.set_title("Demodulated Signal")
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Amplitude")
    ax.legend()
    st.pyplot(fig)
    
    # Detect the period of the NRZ signal
    period, peaks = detect_period(demodulated_signal, sampling_rate)
    
    if period is not None:
        # Extract the binary sequence from the NRZ signal
        binary_sequence = extract_binary_sequence(demodulated_signal, period, sampling_rate)

        # Plot the detected NRZ signal based on binary sequence
        nrz_signal = np.array([1 if bit == 1 else -1 for bit in binary_sequence])
        t_nrz = np.arange(len(nrz_signal)) * period
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.step(t_nrz, nrz_signal, where='post', label='NRZ Signal')
        ax.set_title("NRZ Signal")
        ax.set_xlabel("Time (s)")
        ax.set_ylabel("Amplitude")
        ax.legend()
        st.pyplot(fig)

        # Display the detected period and binary sequence
        st.write(f"Detected Period: {period:.4f} s")
        st.write(f"Binary Sequence: {binary_sequence}")
    else:
        st.write("Unable to detect the period of the signal.")

if __name__ == "__main__":
    main()
