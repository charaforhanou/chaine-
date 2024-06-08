import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import welch, firwin, lfilter

st.set_option('deprecation.showPyplotGlobalUse', False)

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

# def filtre_NRZ(signal, Ts, sampling_rate=1000):
#     num_samples_per_period = int(Ts * sampling_rate / 1000)
#     nrz_signal = np.zeros(len(signal) * num_samples_per_period)
#     for i, bit in enumerate(signal):
#         nrz_signal[i * num_samples_per_period:(i + 1) * num_samples_per_period] = 1 if bit == 1 else -1
#     return nrz_signal


def filtre_nyquist(signal, Ts, sampling_rate=1000):
    # Example Nyquist filter (Raised Cosine Filter)
    from scipy.signal import firwin, lfilter
    num_samples_per_period = int(Ts * sampling_rate / 1000)
    roll_off = 0.25
    num_taps = 101
    nyquist_filter = firwin(num_taps, cutoff=1.0 / num_samples_per_period, window=('kaiser', roll_off))
    nyquist_signal = lfilter(nyquist_filter, 1.0, np.repeat(signal, num_samples_per_period))
    return nyquist_signal


def calculate_dsp(signal, sampling_rate=1000):
    freqs, psd = welch(signal, fs=sampling_rate, nperseg=1024)
    return freqs, psd

def apply_NRZ(binary_sequence, Ts):
    nrz = [0]
    for bit in binary_sequence:
            nrz.extend([1, -1] if bit == 0 else [-1, 1])
    return nrz

def plot_signals(signal, Ts, sampling_rate=1000):
    whitened_signal = filtre_blanch(signal, Ts, sampling_rate)
    rz_signal = apply_NRZ(signal, Ts)
    nyquist_signal = filtre_nyquist(signal, Ts, sampling_rate)
    freqs, psd = calculate_dsp(whitened_signal, sampling_rate)

    # Calculate the total duration of the signal
    total_duration_ms = len(whitened_signal) * (1000 / sampling_rate)

    # Create the time axis with the same period as the binary sequence
    t = np.linspace(0, total_duration_ms / 1000, len(whitened_signal))

    # Create the figure and axis
    fig, ax = plt.subplots(figsize=(8, 6))

    # Plot the whitened signal
    ax.plot(t, whitened_signal, label='Whitened Signal', color='red')
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Amplitude')
    ax.set_title('Whitened Signal')
    ax.legend()

    # Display the plot in Streamlit
    fig, axs = plt.subplots(4, 1, figsize=(10, 12))

    axs[0].plot(t, whitened_signal, label='Whitened Signal', color='red')
    axs[0].set_xlabel('Time (s)')
    axs[0].set_ylabel('Amplitude')
    axs[0].set_title('Whitened Signal')
    axs[0].legend()

    axs[1].plot(t[:len(rz_signal)], rz_signal, label='NRZ Signal', color='blue')
    axs[1].set_xlabel('Time (s)')
    axs[1].set_ylabel('Amplitude')
    axs[1].set_title('          NRZ Signal')
    axs[1].legend()

    axs[2].plot(t[:len(nyquist_signal)], nyquist_signal, label='Nyquist Signal', color='green')
    axs[2].set_xlabel('Time (s)')
    axs[2].set_ylabel('Amplitude')
    axs[2].set_title('Nyquist Signal')
    axs[2].legend()

    axs[3].semilogy(freqs, psd, label='Power Spectral Density', color='purple')
    axs[3].set_xlabel('Frequency (Hz)')
    axs[3].set_ylabel('Power/Frequency (dB/Hz)')
    axs[3].set_title('Power Spectral Density')
    axs[3].legend()

    fig.tight_layout()
    st.pyplot(fig)


st.title("Signal Filters and DSP")

signal, Ts = getsignal_ts()

if not signal or not Ts:
    signal = st.text_input("Enter Binary Sequence (comma-separated)", value="1,0,1,1,0")
    Ts = st.number_input("Period of the Square Wave (ms)", min_value=1, value=100, step=1)
    signal = [int(bit) for bit in signal.split(',')]

# Plot the signals and DSP
plot_signals(signal, Ts)