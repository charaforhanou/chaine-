import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

def plot_nyquist_signal(nyquist_signal):
    # Create time array for the Nyquist signal
    sampling_rate = 1000  # Assuming a sampling rate of 1000 Hz
    total_duration_ms = len(nyquist_signal) * (1000 / sampling_rate)
    t = np.linspace(0, total_duration_ms / 1000, len(nyquist_signal))

    # Plot the Nyquist signal
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.plot(t, nyquist_signal, label='Nyquist Signal', color='green')
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Amplitude')
    ax.set_title('Nyquist Signal')
    ax.legend()
    ax.grid(True)

    # Show plot in Streamlit
    st.pyplot(fig)

def main():
    st.title("Nyquist Signal Viewer")

    # File uploader to select the Nyquist signal file
    uploaded_file = "/workspaces/chaine-/nyquist_signal.txt"

    if uploaded_file is not None:
        # Read the Nyquist signal from the uploaded file
        nyquist_signal = np.loadtxt(uploaded_file)

        # Plot the Nyquist signal
        plot_nyquist_signal(nyquist_signal)

if __name__ == "__main__":
    main()
