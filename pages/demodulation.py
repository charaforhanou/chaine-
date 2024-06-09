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

def demodulate_ask(modulated_signal, threshold=0.1):
    # Demodulate using envelope detection
    demodulated_signal = np.abs(modulated_signal)
    
    # Binarize the signal based on the threshold
    demodulated_binary_signal = np.where(demodulated_signal > threshold, 1, 0)
    
    return demodulated_binary_signal

def estimate_period(demodulated_binary_signal, sampling_rate=1000):
    # Find indices of transitions
    transitions_indices = np.where(np.diff(demodulated_binary_signal) != 0)[0]
    
    # Calculate time differences between consecutive transitions
    if len(transitions_indices) > 1:
        time_diffs = np.diff(transitions_indices) / sampling_rate
        # Take the average time difference as the estimated period
        estimated_period = np.mean(time_diffs)
    else:
        estimated_period = np.nan  # Not enough transitions to estimate period
    
    return estimated_period

def main():
    st.title("Demodulate ASK Modulated Signal")

    # File name for the modulated signal
    filename = "modulated_signal_ASK.txt"
    # filename = "modulated_signal_FSK.txt"

    try:
        modulated_signal = np.loadtxt(filename)
        st.subheader("Original Modulated Signal")
        plot_signal(modulated_signal, title="Original Modulated Signal")

        # Demodulate the ASK modulated signal
        demodulated_signal = demodulate_ask(modulated_signal)
        st.subheader("Demodulated Binary Signal")
        plot_signal(demodulated_signal, title="Demodulated Binary Signal")

        # Save the demodulated signal to a file
        demodulated_filename = "demodulated_signal.txt"
        np.savetxt(demodulated_filename, demodulated_signal)
        st.subheader("Demodulated Signal Saved")
       # st.write(f"Demodulated signal has been saved to {demodulated_filename}")

        # Estimate the period
        estimated_period = estimate_period(demodulated_signal)
        st.subheader("Estimated Period")
        if not np.isnan(estimated_period):
            st.write("Estimated Period:", 2.5*1000*estimated_period, "ms")
        else:
            st.write("Not enough transitions to estimate the period.")
    except Exception as e:
        st.error(f"An error occurred while reading the file: {e}")

if __name__ == "__main__":
    main()
