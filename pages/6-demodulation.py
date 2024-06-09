import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

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

def demodulate_ask(modulated_signal, threshold=0):
    # Demodulate by detecting positive and negative values
    demodulated_signal = np.where(modulated_signal >= threshold, 1, 0)
    
    return demodulated_signal

def decode_binary_sequence(demodulated_signal, fixed_period, sampling_rate=1000):
    # Determine the bit duration based on the fixed period
    bit_duration = int(fixed_period * sampling_rate)
    
    # Decode the binary sequence
    binary_sequence = []
    for i in range(0, len(demodulated_signal), bit_duration):
        bit_segment = demodulated_signal[i:i+bit_duration]
        # Determine the value of the bit (majority rule)
        bit_value = 1 if np.mean(bit_segment) > 0.5 else 0
        binary_sequence.append(bit_value)
    
    return binary_sequence

def main():
    st.title("Demodulate ASK Modulated Signal")

    # File name for the modulated signal
    filename = "modulated_signal_ASK.txt"

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
        st.write(f"Demodulated signal has been saved to {demodulated_filename}")

        # Set the fixed period to 100 ms
        fixed_period = 0.1  # in seconds

        # Decode the binary sequence using the fixed period
        binary_sequence = decode_binary_sequence(demodulated_signal, fixed_period)
        st.subheader("Detected Binary Sequence")
        st.write("".join(map(str, binary_sequence)))

    except Exception as e:
        st.error(f"An error occurred while reading the file: {e}")

if __name__ == "__main__":
    main()
