import numpy as np
from scipy.signal import firwin, lfilter, butter, filtfilt
from scipy.fftpack import fft, fftfreq
import streamlit as st
import matplotlib.pyplot as plt

def modulate(signal, carrier_freq, sampling_rate):
    t = np.arange(len(signal)) / sampling_rate
    carrier = np.cos(2 * np.pi * carrier_freq * t)
    modulated_signal = signal * carrier
    return modulated_signal

def demodulate(modulated_signal, carrier_freq, sampling_rate):
    t = np.arange(len(modulated_signal)) / sampling_rate
    carrier = np.cos(2 * np.pi * carrier_freq * t)
    demodulated_signal = modulated_signal * carrier
    
    # Apply low-pass filter to recover the baseband signal
    nyquist_rate = sampling_rate / 2
    cutoff_freq = carrier_freq / nyquist_rate
    b, a = butter(5, cutoff_freq)
    recovered_signal = filtfilt(b, a, demodulated_signal)
    return recovered_signal

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

def read_signal(filename):
    """Reads the modulated signal from a file."""
    with open(filename, 'r') as file:
        lines = file.readlines()
        signal_data = np.array([float(line.strip()) for line in lines if not line.startswith("#")])
    return signal_data

def main():
    st.title("Modulation and Demodulation")
    filename = 'modulated_signal_ASK.txt'
    modulated_signal = read_signal(filename)
    
    # User input
    sampling_rate = st.number_input("Sampling Rate (Hz)", min_value=100, step=100, value=1000)
    Ts = st.number_input("Signal Period (ms)", min_value=1.0, step=1.0, value=20.0)
    
    # Detect the carrier frequency from the modulated signal
    detected_carrier_freq = detect_carrier_frequency(modulated_signal, sampling_rate)
    st.write(f"Detected Carrier Frequency: {detected_carrier_freq} Hz")
    
    # Demodulate the signal using the detected carrier frequency
    demodulated_signal = demodulate(modulated_signal, detected_carrier_freq, sampling_rate)

    # Plot the signals
    t = np.arange(len(modulated_signal)) / sampling_rate

    fig, ax = plt.subplots(2, 1, figsize=(12, 8))
  
    ax[0].plot(t, modulated_signal, label='Modulated Signal')
    ax[0].legend()
    ax[0].set_title("Modulated Signal")
    ax[0].set_xlabel("Time (s)")
    ax[0].set_ylabel("Amplitude")

    ax[1].plot(t, demodulated_signal, label='Demodulated Signal')
    ax[1].legend()
    ax[1].set_title("Demodulated Signal")
    ax[1].set_xlabel("Time (s)")
    ax[1].set_ylabel("Amplitude")

    st.pyplot(fig)

if __name__ == "__main__":
    main()
