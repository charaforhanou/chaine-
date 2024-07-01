import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

class BinaryTransmissionApp:
    def __init__(self):
        st.title("Binary Transmission")
        self.filter_type = st.selectbox("Select filter type:", ["RZ", "NRZ", "Miller", "Manchester", "HDBN"])
        if self.filter_type == "HDBN":
            self.hdbn_order = st.number_input("HDBN Filter Order", min_value=1, step=1, value=3)
        else:
            self.hdbn_order = 3

        self.plot()

    def apply_filter(self, binary_sequence, Ts, filter_type):
        if filter_type == "RZ":
            return self.apply_RZ(binary_sequence, Ts)
        elif filter_type == "NRZ":
            return self.apply_NRZ(binary_sequence, Ts)
        elif filter_type == "Miller":
            return self.apply_Miller(binary_sequence)
        elif filter_type == "Manchester":
            return self.apply_Manchester(binary_sequence)
        elif filter_type == "HDBN":
            return self.apply_HDBN(binary_sequence)
        else:
            return binary_sequence

    def apply_RZ(self, binary_sequence, Ts):
        rz_sequence = []
        for bit in binary_sequence:
            rz_sequence.append(1 if bit == 1 else 0)
            # if bit == 1:
            #     rz_sequence.extend([1, 0])
            # else:
            #     rz_sequence.extend([0, 0])
        return rz_sequence

    def apply_NRZ(self, binary_sequence, Ts):
        nrz_sequence = []
        for bit in binary_sequence:
            nrz_sequence.append(1 if bit == 1 else -1)
        return nrz_sequence

    def apply_Miller(self, binary_sequence):
        miller_sequence = []
        prev_bit = 1  # Assuming the previous bit before the sequence starts is 1 to handle the initial condition
        for i, bit in enumerate(binary_sequence):
            if bit == 0:
                if prev_bit == 0:
                    miller_sequence.extend([1, -1])  # Transition at the end of the bit
                else:
                    miller_sequence.extend([1, 1])  # No transition
            elif bit == 1:
                miller_sequence.extend([-1, 1])  # Transition in the middle of the bit
            prev_bit = bit
        return miller_sequence

    def apply_Manchester(self, binary_sequence):
        manchester_sequence = []
        for bit in binary_sequence:
            manchester_sequence.extend([1, -1] if bit == 0 else [-1, 1])
        return manchester_sequence

    def apply_HDBN(self, binary_sequence):
        hdbn_sequence = []
        violation_counter = 0  # To keep track of B violation count
        for bit in binary_sequence:
            if bit == 0:
                if violation_counter == self.hdbn_order - 1:
                    hdbn_sequence.extend([0, 0, 0, 1])  # B violation (replace 4 consecutive 0s with 0001)
                    violation_counter = 0
                else:
                    hdbn_sequence.append(0)
                    violation_counter += 1
            else:
                hdbn_sequence.append(1)
                violation_counter = 0
        return hdbn_sequence

    def plot(self):
        # Read binary sequence and period from file
        filename = "binary_sequence_and_period.txt"
        try:
            with open(filename, 'r') as file:
                lines = file.readlines()[1:]  # Skip the first line (header)
                binary_sequence = []
                period_ms = None
                for line in lines:
                    parts = line.split()
                    binary_sequence.append(int(parts[0]))
                    period_ms = float(parts[1])
        except Exception as e:
            st.error("An error occurred while reading the file: {}".format(e))
            return

        Ts = period_ms  # Define Ts based on the period in milliseconds

        # Apply selected filter
        filtered_sequence = self.apply_filter(binary_sequence, Ts, self.filter_type)

        # Create time array for binary sequence
        t = np.arange(0, len(binary_sequence) * period_ms, period_ms)

        # Plot original binary sequence
        fig, ax = plt.subplots(2, 1, figsize=(10, 8))

        ax[0].step(t, binary_sequence, where='post')
        ax[0].set_title('Original Binary Sequence')
        ax[0].set_xlabel('Time (ms)')
        ax[0].set_ylabel('Amplitude')
        ax[0].set_ylim(-0.1, 1.1)
        ax[0].annotate(f'Period: {period_ms:.2f} ms', xy=(0.05, 0.9), xycoords='axes fraction')

        # Create time array for filtered sequence
        filtered_t = np.linspace(0, len(filtered_sequence) * (Ts / 2), len(filtered_sequence))

        # Plot filtered sequence
        ax[1].step(filtered_t, filtered_sequence, where='post')
        ax[1].set_title(f'Filtered Sequence ({self.filter_type})')
        ax[1].set_xlabel('Time (ms)')
        ax[1].set_ylabel('Amplitude')

        st.pyplot(fig)

if __name__ == "__main__":
    BinaryTransmissionApp()
