import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import welch

st.set_option('deprecation.showPyplotGlobalUse', False)

def plot_nyquist_signal(nyquist_signal, title="Nyquist Signal"):
    sampling_rate = 1000  # Assuming a sampling rate of 1000 Hz
    total_duration_ms = len(nyquist_signal) * (1000 / sampling_rate)
    t = np.linspace(0, total_duration_ms / 1000, len(nyquist_signal))

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.plot(t, nyquist_signal, label=title, color='green')
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Amplitude')
    ax.set_title(title)
    ax.legend()
    ax.grid(True)

    st.pyplot(fig)

def modulate_signal(signal, modulation_type, sampling_rate=1000, f0=10):
    t = np.arange(len(signal)) / sampling_rate
    if modulation_type == 'ASK':
        modulated_signal = signal * np.cos(2 * np.pi * f0 * t)
    elif modulation_type == 'FSK':
        f1, f2 = f0, 2 * f0
        modulated_signal = np.cos(2 * np.pi * (f1 * t + (f2 - f1) * np.cumsum(signal) / sampling_rate))
    elif modulation_type == 'PSK':
        modulated_signal = np.cos(2 * np.pi * f0 * t + np.pi * signal)
    else:
        st.error("Unsupported modulation type selected.")
        return np.zeros_like(signal)
    return modulated_signal

def calculate_dsp(signal, sampling_rate=1000):
    freqs, psd = welch(signal, fs=sampling_rate, nperseg=1024)
    return freqs, psd

def plot_dsp(freqs, psd, title="Power Spectral Density"):
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.semilogy(freqs, psd, label=title, color='purple')
    ax.set_xlabel('Frequency (Hz)')
    ax.set_ylabel('Power/Frequency (dB/Hz)')
    ax.set_title(title)
    ax.legend()
    ax.grid(True)

    st.pyplot(fig)

def main():
    st.title("Nyquist Signal Viewer and Modulation")

    # Relative path to the Nyquist signal file
    filename = "nyquist_signal.txt"

    try:
        nyquist_signal = np.loadtxt(filename)
        st.subheader("Nyquist Signal")
        plot_nyquist_signal(nyquist_signal)

        modulation_type = st.selectbox("Choose Modulation Type", ["ASK", "FSK", "PSK"])

        if modulation_type:
            modulated_signal = modulate_signal(nyquist_signal, modulation_type)

            st.subheader(f"{modulation_type} Modulated Signal")
            plot_nyquist_signal(modulated_signal, title=f"{modulation_type} Modulated Signal")

            # Save the modulated signal to a file
            modulated_filename = f"modulated_signal_{modulation_type}.txt"
            np.savetxt(modulated_filename, modulated_signal, fmt='%f', header=f"{modulation_type} Modulated Signal")

            freqs, psd = calculate_dsp(modulated_signal)

            st.subheader(f"{modulation_type} Modulated Signal Power Spectral Density")
            plot_dsp(freqs, psd, title=f"{modulation_type} Power Spectral Density")
    except Exception as e:
        st.error(f"An error occurred while reading the file: {e}")

if __name__ == "__main__":
    main()
# saveed data 