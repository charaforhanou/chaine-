import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

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

signal, Ts = getsignal_ts()

def filtre_blanch(signal, Ts, sampling_rate=1000):
    """
    Apply the whitening filter to the input signal.

    Parameters:
    signal (list): Input signal
    Ts (float): Period of the square wave (in milliseconds)
    sampling_rate (int): Sampling rate in Hz (samples per second)

    Returns:
    numpy.ndarray: Whitened signal
    """
    num_samples_per_period = int(Ts * sampling_rate / 1000)
    whitened_signal = np.zeros(len(signal) * num_samples_per_period)
    for i, bit in enumerate(signal):
        if bit == 1:
            whitened_signal[i * num_samples_per_period] = 1
    return whitened_signal

def plot_whitened_signal(signal, Ts, sampling_rate=1000):
    """
    Plot the whitened signal.

    Parameters:
    signal (list): Input signal
    Ts (float): Period of the square wave (in milliseconds)
    sampling_rate (int): Sampling rate in Hz (samples per second)
    """
    # Apply the whitening filter
    whitened_signal = filtre_blanch(signal, Ts, sampling_rate)

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
    st.pyplot(fig)

# Streamlit app
st.title("Whitened Signal")

# If signal and Ts are not obtained from the file, provide input fields for them
if not signal or not Ts:
    signal = st.text_input("Enter Binary Sequence (comma-separated)", value="1,0,1,1,0")
    Ts = st.number_input("Period of the Square Wave (ms)", min_value=1, value=100, step=1)
    signal = [int(bit) for bit in signal.split(',')]

# Plot the whitened signal
plot_whitened_signal(signal, Ts)
