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

def filtre_blanch(signal, Ts, sampling_rate=1000):
    num_samples_per_period = int(Ts * sampling_rate / 1000)
    whitened_signal = np.zeros(len(signal) * num_samples_per_period)
    for i, bit in enumerate(signal):
        if bit == 1:
            whitened_signal[i * num_samples_per_period] = 1
    return whitened_signal

def filtre_NRZ(signal, Ts, sampling_rate=1000):
    num_samples_per_period = int(Ts * sampling_rate / 1000)
    nrz_signal = np.zeros(len(signal) * num_samples_per_period)
    for i, bit in enumerate(signal):
        value = 1 if bit == 1 else -1
        nrz_signal[i * num_samples_per_period:(i + 1) * num_samples_per_period] = value
    return nrz_signal

def filtre_nyquist(signal, Ts, sampling_rate=1000):
    # Example Nyquist filter (Raised Cosine Filter)
    num_samples_per_period = int(Ts * sampling_rate / 1000)
    roll_off = 0.25
    num_taps = 101
    nyquist_filter = firwin(num_taps, cutoff=1.0 / num_samples_per_period, window=('kaiser', roll_off))
    nyquist_signal = lfilter(nyquist_filter, 1.0, signal)
    return nyquist_signal

def calculate_dsp(signal, sampling_rate=1000):
    freqs, psd = welch(signal, fs=sampling_rate, nperseg=1024)
    return freqs, psd

def plot_signals(signal, Ts, sampling_rate=1000):
    whitened_signal = filtre_blanch(signal, Ts, sampling_rate)
    nrz_signal = filtre_NRZ(signal, Ts, sampling_rate)
    nyquist_signal = filtre_nyquist(nrz_signal, Ts, sampling_rate)
    freqs, psd = calculate_dsp(whitened_signal, sampling_rate)
    
    total_duration_ms = len(nyquist_signal) * (1000 / sampling_rate)
    t = np.linspace(0, total_duration_ms / 1000, len(nyquist_signal))

    fig, axs = plt.subplots(3, 1, figsize=(10, 12))

    axs[0].plot(t[:len(whitened_signal)], whitened_signal, label='Whitened Signal', color='red')
    axs[0].set_xlabel('Time (s)')
    axs[0].set_ylabel('Amplitude')
    axs[0].set_title('Whitened Signal')
    axs[0].legend()

    axs[1].plot(t[:len(nrz_signal)], nrz_signal, label='NRZ Signal', color='blue')
    axs[1].set_xlabel('Time (s)')
    axs[1].set_ylabel('Amplitude')
    axs[1].set_title('NRZ Signal')
    axs[1].legend()

    axs[2].plot(t, nyquist_signal, label='Nyquist Signal', color='green')
    axs[2].set_xlabel('Time (s)')
    axs[2].set_ylabel('Amplitude')
    axs[2].set_title('Nyquist Signal')
    axs[2].legend()

    fig.tight_layout()
    st.pyplot(fig)

    # Save Nyquist signal to a file
    filename = "nyquist_signal.txt"
    np.savetxt(filename, nyquist_signal, fmt='%f', header="Nyquist Signal")
    st.markdown(f"Download Nyquist signal: [Nyquist Signal]({filename})")

st.title("Signal Filters and DSP")

signal, Ts = getsignal_ts()

if not signal or not Ts:
    signal = st.text_input("Enter Binary Sequence (comma-separated)", value="1,0,1,1,0")
    Ts = st.number_input("Period of the Square Wave (ms)", min_value=1, value=100, step=1)
    signal = [int(bit) for bit in signal.split(',')]

# Plot the signals and DSP
plot_signals(signal, Ts)



# with nyquist on NRZ 