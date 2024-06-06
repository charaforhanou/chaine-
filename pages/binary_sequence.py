import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

class BinaryTransmissionApp:
    def __init__(self):
        st.title("Binary Transmission")

        self.binary_sequence = st.text_input("Enter binary sequence (0 and 1):")
        self.period_ms = st.number_input("Enter symbol period (ms):", value=1.0, step=0.01)

        self.plot_button = st.button("Plot")
        if self.plot_button:
            self.plot()

    def plot(self):
        if not self.binary_sequence or not self.binary_sequence.isdigit():
            st.error("Please enter a valid binary sequence.")
            return

        binary_sequence = [int(bit) for bit in self.binary_sequence]

        # Create time array for binary sequence
        t = np.arange(0, len(binary_sequence) * self.period_ms, self.period_ms)

        # Create binary sequence plot
        fig, axs = plt.subplots(2, 1)
        axs[0].step(t, binary_sequence, where='post')
        axs[0].set_title('Binary Sequence')
        axs[0].set_xlabel('Time (ms)')
        axs[0].set_ylabel('Bit')
        axs[0].set_ylim(-0.1, 1.1)

        # Create clock signal
        clock_signal = np.zeros(len(t) * 2)  # Two samples per period for high and low
        for i in range(len(binary_sequence)):
            clock_signal[2 * i] = 1  # High part of the clock
            clock_signal[2 * i + 1] = 0  # Low part of the clock
        t_clock = np.arange(0, len(binary_sequence) * self.period_ms, self.period_ms / 2)

        # Create clock plot
        axs[1].step(t_clock, clock_signal, where='post')
        axs[1].set_title('Clock Signal')
        axs[1].set_xlabel('Time (ms)')
        axs[1].set_ylabel('Amplitude')
        axs[1].set_ylim(-0.1, 1.1)

        # Show plots
        st.pyplot(fig)

        # Save binary sequence and period to a text file
        data = np.column_stack((binary_sequence, np.full_like(binary_sequence, self.period_ms)))
        np.savetxt('binary_sequence_and_period.txt', data, fmt='%d %.2f', header='Binary Sequence   Period (ms)', comments='')

def main():
    app = BinaryTransmissionApp()

if __name__ == "__main__":
    main()
