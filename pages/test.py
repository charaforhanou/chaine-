import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

st.set_option('deprecation.showPyplotGlobalUse', False)

def plot_signal(signal, title="Signal"):
    sampling_rate = 1000  # Assuming a sampling rate of 1000 Hz
    total_duration_ms = len(signal) * (1000 / sampling_rate)
    t = np.linspace(0, total_duration_ms / 1000, len(signal))

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.plot(t, signal, label=title)
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Amplitude')
    ax.set_title(title)
    ax.legend()
    ax.grid(True)

    st.pyplot(fig)

def demodulate_ask_with_both_transitions(modulated_signal, threshold=0.1):
    # Demodulate using cosine squared demodulation
    demodulated_signal = np.square(modulated_signal)

    # Find both positive and negative transitions
    positive_transitions, _ = find_peaks(demodulated_signal, height=threshold)
    negative_transitions, _ = find_peaks(-demodulated_signal, height=threshold)

    # Initialize demodulated binary signal
    demodulated_binary_signal = np.zeros_like(demodulated_signal)

    # Mark positive transitions as '1' and negative transitions as '-1'
    demodulated_binary_signal[positive_transitions] = 1
    demodulated_binary_signal[negative_transitions] = -1

    return demodulated_binary_signal

def estimate_period(demodulated_binary_signal, sampling_rate=1000):
    # Find indices of transitions
    transitions_indices = np.where(np.abs(np.diff(demodulated_binary_signal)) > 0)[0]

    # Calculate time differences between consecutive transitions
    time_diffs = np.diff(transitions_indices) / sampling_rate

    # Take the average time difference as the estimated period
    estimated_period = np.mean(time_diffs)
    
    return estimated_period

def main():
    st.title("Demodulate ASK Modulated Signal")

    # File name for the modulated signal
    filename = "modulated_signal_ASK.txt"

    try:
        modulated_signal = np.loadtxt(filename)
        st.subheader("Original Modulated Signal")
        plot_signal(modulated_signal, title="Original Modulated Signal")

        # Demodulate the ASK modulated signal
        demodulated_signal = demodulate_ask_with_both_transitions(modulated_signal)
        st.subheader("Demodulated Binary Signal")
        plot_signal(demodulated_signal, title="Demodulated Binary Signal")

        # Estimate the period
        estimated_period = estimate_period(demodulated_signal)
        st.subheader("Estimated Period")
        st.write("Estimated Period:", 1000*estimated_period, "ms")
    except Exception as e:
        st.error(f"An error occurred while reading the file: {e}")

if __name__ == "__main__":
    main()
