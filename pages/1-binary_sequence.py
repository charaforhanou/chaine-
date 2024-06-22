import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

class BinaryTransmissionApp:
    def __init__(self):
        st.title("Binary Transmission")

        # Initialize session state variables
        if 'binary_sequence' not in st.session_state:
            st.session_state.binary_sequence = ""
        if 'period_ms' not in st.session_state:
            st.session_state.period_ms = 50

        self.binary_sequence_input = st.text_input("Enter binary sequence (0 and 1):", st.session_state.binary_sequence)
        self.period_ms_input = st.number_input("Enter symbol period (ms):", value=st.session_state.period_ms, step=50, format="%d")

        self.generate_random_button = st.button("Generate Random Binary Sequence")
        if self.generate_random_button:
            self.generate_random_sequence()

        self.plot_button = st.button("Plot")
        if self.plot_button:
            self.plot()

    def generate_random_sequence(self):
        sequence_length = st.number_input("Enter the length of the binary sequence:", min_value=1, value=10, step=1)
        st.session_state.binary_sequence = ''.join(np.random.choice(['0', '1'], size=sequence_length))
        st.text(f"Generated binary sequence: {st.session_state.binary_sequence}")

        periods = [50,10,15,20,25,30,35,40,60,70]
        st.session_state.period_ms = np.random.choice(periods)
        st.text(f"Selected period: {st.session_state.period_ms} ms")

        # Update the input fields with the generated values
        self.binary_sequence_input = st.session_state.binary_sequence
        self.period_ms_input = st.session_state.period_ms

    def plot(self):
        binary_sequence = self.binary_sequence_input
        period_ms = self.period_ms_input

        if not binary_sequence or not binary_sequence.isdigit():
            st.error("Please enter a valid binary sequence.")
            return

        binary_sequence = [int(bit) for bit in binary_sequence]

        # Create time array for binary sequence
        t = np.arange(0, len(binary_sequence) * period_ms, period_ms)

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
        t_clock = np.arange(0, len(binary_sequence) * period_ms, period_ms / 2)

        # Create clock plot
        axs[1].step(t_clock, clock_signal, where='post')
        axs[1].set_title('Clock Signal')
        axs[1].set_xlabel('Time (ms)')
        axs[1].set_ylabel('Amplitude')
        axs[1].set_ylim(-0.1, 1.1)

        # Show plots
        st.pyplot(fig)

        # Save binary sequence and period to a text file
        data = np.column_stack((binary_sequence, np.full_like(binary_sequence, period_ms)))
        np.savetxt('binary_sequence_and_period.txt', data, fmt='%d %.2f', header='Binary Sequence   Period (ms)', comments='')

def main():
    app = BinaryTransmissionApp()

if __name__ == "__main__":
    main()
