import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import welch

st.set_option('deprecation.showPyplotGlobalUse', False)

def plot_signal(signal, title="Signal"):
    sampling_rate = 1000  # Assuming a sampling rate of 1000 Hz
    total_duration_ms = len(signal) * (1000 / sampling_rate)
    t = np.linspace(0, total_duration_ms / 1000, len(signal))

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.plot(t, signal, label=title, color='blue')
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Amplitude')
    ax.set_title(title)
    ax.legend()
    ax.grid(True)

    st.pyplot(fig)

def add_noise(signal, noise_level=0.1):
    noise = np.random.normal(0, noise_level, len(signal))
    noisy_signal = signal + noise
    return noisy_signal

def main():
    st.title("Read Modulated Signal and Add Noise")

    # File name for the modulated signal
    filename = "modulated_signal_ASK.txt"

    try:
        modulated_signal = np.loadtxt(filename)
        st.subheader("Original Modulated Signal")
        plot_signal(modulated_signal, title="Original Modulated Signal")

        # Add noise to the modulated signal with a fixed noise level of 0.1
        noise_level = 0.1
        noisy_signal = add_noise(modulated_signal, noise_level=noise_level)

        st.subheader("Noisy Modulated Signal")
        plot_signal(noisy_signal, title="Noisy Modulated Signal")

        # Save the noisy signal to a file
        noisy_filename = "noisy_modulated_signal.txt"
        np.savetxt(noisy_filename, noisy_signal, fmt='%f', header="Noisy Modulated Signal")
       # st.markdown(f"Download Noisy Modulated Signal: [Noisy Modulated Signal]({noisy_filename})")
    except Exception as e:
        st.error(f"An error occurred while reading the file: {e}")

if __name__ == "__main__":
    main()
#nyquist_with_nrz_and_addnoise