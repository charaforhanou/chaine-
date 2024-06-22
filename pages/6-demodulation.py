import numpy as np
from scipy.signal import firwin, lfilter, butter, filtfilt
import streamlit as st
import matplotlib.pyplot as plt

# def nyquist_filter(signal, Ts, sampling_rate=1000):
#     num_samples_per_period = int(Ts * sampling_rate / 1000)
#     roll_off = 0.25
#     num_taps = 101
    
#     nyquist_filter = firwin(num_taps, cutoff=1.0 / num_samples_per_period, window=('kaiser', roll_off))
#     nyquist_signal = lfilter(nyquist_filter, 1.0, signal)
#     return nyquist_signal

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


def read_signal(filename):
    """Reads the modulated signal from a file."""
    with open(filename, 'r') as file:
        lines = file.readlines()
        signal_data = np.array([float(line.strip()) for line in lines if not line.startswith("#")])
    return signal_data


def main():
    filename = 'modulated_signal_ASK.txt'
    st.title("Modulation and Demodulation")
    modulated_signal = read_signal(filename)
    # User input
    sampling_rate = st.number_input("Sampling Rate (Hz)", min_value=1000, step=1000, value=10000)
    Ts = st.number_input("Signal Period (s)", min_value=1.0, step=1.0, value=1.0)
    binary_sequence_length = st.number_input("Binary Sequence Length", min_value=10, step=10, value=100)
    carrier_freq = st.number_input("Carrier Frequency (Hz)", min_value=100, step=10, value=250)

    binary_sequence = np.random.choice([0, 1], size=binary_sequence_length)
    # signal = nyquist_filter(binary_sequence, Ts, sampling_rate)
    # modulated_signal = modulate(signal, carrier_freq, sampling_rate)
    demodulated_signal = demodulate(modulated_signal, carrier_freq, sampling_rate)

    # Plot the signals
    t = np.arange(len(modulated_signal)) / sampling_rate

    fig, ax = plt.subplots(3, 1, figsize=(12, 8))
    ax[0].plot(t, modulated_signal, label='Nyquist Filtered Signal')
    ax[0].legend()
    ax[1].plot(t, modulated_signal, label='Modulated Signal')
    ax[1].legend()
    ax[2].plot(t, demodulated_signal, label='Demodulated Signal')
    ax[2].legend()

    st.pyplot(fig)

if __name__ == "__main__":
    main()
