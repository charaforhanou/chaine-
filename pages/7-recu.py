import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
from scipy.signal import firwin, lfilter, butter, filtfilt
from scipy.fftpack import fft, fftfreq
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
        average_period = np.mean(periods)
        
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
def detect_carrier_frequency(signal, sampling_rate):
    # Compute the FFT of the signal
    N = len(signal)
    fft_signal = fft(signal)
    fft_magnitude = np.abs(fft_signal)
    
    # Compute the frequency bins
    frequencies = fftfreq(N, d=1/sampling_rate)
    
    # Find the peak frequency
    peak_index = np.argmax(fft_magnitude[:N // 2])  # Only consider positive frequencies
    peak_frequency = frequencies[peak_index]
    
    return peak_frequency
def main():
    filename = 'modulated_signal_ASK.txt'
    modulated_signal = read_signal(filename)
    
    # User input
    sampling_rate=1000

    
    # Detect the carrier frequency from the modulated signal
    detected_carrier_freq = detect_carrier_frequency(modulated_signal, sampling_rate)
    st.write(f"Detected Carrier Frequency: {detected_carrier_freq} Hz")
    
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
    period
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
#1101011101
        # Display the detected period and binary sequence
        st.write(f"Detected Period: {period:.4f} s")
        st.write(f"Binary Sequence: {binary_sequence}")
    else:
        st.write("Unable to detect the period of the signal.")

if __name__ == "__main__":
    main()
