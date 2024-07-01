import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import welch, firwin, lfilter

def getsignal_ts():
    filename = "binary_sequence_and_period.txt"
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

def filtre_NRZ(signal, Ts, sampling_rate=1000):
    num_samples_per_period = int(Ts * sampling_rate / 1000)
    nrz_signal = np.repeat(signal, num_samples_per_period)
    return nrz_signal

def filtre_nyquist(signal, Ts, sampling_rate=1000):
    num_samples_per_period = int(Ts * sampling_rate / 1000)
    roll_off = 0.25
    num_taps = 101
    nyquist_filter = firwin(num_taps, cutoff=1.0 / num_samples_per_period, window=('kaiser', roll_off), scale=True)
    nyquist_signal = lfilter(nyquist_filter, 1.0, signal)

    # Normalize the Nyquist signal to ensure it fits within the expected amplitude range
    nyquist_signal /= np.max(np.abs(nyquist_signal))

    return nyquist_signal

def calculate_dsp(signal, sampling_rate=1000):
    freqs, psd = welch(signal, fs=sampling_rate, nperseg=1024)
    return freqs, psd

def filtre_blanch(signal, Ts, sampling_rate=1000):
    num_samples_per_period = int(Ts * sampling_rate / 1000)
    whitened_signal = np.zeros(len(signal) * num_samples_per_period)
    for i, bit in enumerate(signal):
        if bit == 1:
            whitened_signal[i * num_samples_per_period:(i + 1) * num_samples_per_period] = 1
        else:
            whitened_signal[i * num_samples_per_period:(i + 1) * num_samples_per_period] = -1
    return whitened_signal

def plot_signals(signal, Ts, sampling_rate=1000):
    nrz_signal = filtre_NRZ(signal, Ts, sampling_rate)
    white = filtre_blanch(signal, Ts, sampling_rate)
    nyquist_signal = filtre_nyquist(white, Ts, sampling_rate)

    freqs, psd = calculate_dsp(nyquist_signal, sampling_rate)

    total_duration_ms = len(white) * (1000 / sampling_rate)
    t = np.linspace(0, total_duration_ms / 1000, len(white))

    # Plot the whitening filter
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(white, label='Whitened Signal', color='blue')
    ax.set_xlabel('Samples')
    ax.set_ylabel('Amplitude')
    ax.set_title('Whitening Filter')
    ax.legend()
    st.pyplot(fig)

    # Plot the Nyquist filter
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(nyquist_signal, label='Nyquist Signal', color='green')
    ax.set_xlabel('Samples')
    ax.set_ylabel('Amplitude')
    ax.set_title('Nyquist Filter')
    ax.legend()
    st.pyplot(fig)

    # Plot the DSP of the Nyquist signal
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(freqs, psd, label='Nyquist DSP', color='orange')
    ax.set_xlabel('Frequency (Hz)')
    ax.set_ylabel('Power Spectral Density (dB/Hz)')
    ax.set_title('Nyquist Signal DSP')
    ax.legend()
    st.pyplot(fig)

    # Save Nyquist signal to a file
    filename = "nyquist_signal.txt"
    np.savetxt(filename, nyquist_signal, fmt='%f', header="Nyquist Signal")

st.title("Signal Filters and DSP")

signal, Ts = getsignal_ts()

if not signal or not Ts:
    signal = st.text_input("Enter Binary Sequence (comma-separated)", value="1,0,1,1,0")
    Ts = st.number_input("Period of the Square Wave (ms)", min_value=1, value=100, step=1)
    signal = [int(bit) for bit in signal.split(',')]

# Plot the signals and DSP
plot_signals(signal, Ts)
