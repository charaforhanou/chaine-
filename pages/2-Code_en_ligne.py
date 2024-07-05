import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

class BinaryTransmissionApp:
    def __init__(self, master):
        self.master = master
        master.title("Binary Transmission")
        
        self.filter_type = st.selectbox("Select filter type:", ["RZ", "NRZ", "Miller", "Manchester", "HDBN"])
        if self.filter_type == "HDBN":
            self.hdbn_order = st.number_input("HDBN Filter Order", min_value=1, step=1, value=3)
        else:
            self.hdbn_order = 3

        self.plot()

    def apply_filter(self, binary_sequence, filter_type):
        if filter_type == "RZ":
            return self.apply_RZ(binary_sequence)
        elif filter_type == "NRZ":
            return self.apply_NRZ(binary_sequence)
        elif filter_type == "Miller":
            return self.apply_Miller(binary_sequence)
        elif filter_type == "Manchester":
            return self.apply_Manchester(binary_sequence)
        elif filter_type == "HDBN":
            return self.apply_HDBN(binary_sequence)
        else:
            return binary_sequence

    def apply_RZ(self, binary_sequence):
        rz_sequence = []
        for bit in binary_sequence:
            rz_sequence.extend([1 if bit == 1 else  0])  # High for half period, zero for other half
        return rz_sequence

    def apply_NRZ(self, binary_sequence):
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
        zero_count = 0
        for bit in binary_sequence:
            if bit == 0:
                zero_count += 1
                if zero_count == self.hdbn_order:
                    hdbn_sequence.extend([0, 0, 0, -1])  # Insert violation
                    zero_count = 0
                else:
                    hdbn_sequence.append(0)
            else:
                hdbn_sequence.extend([1, -1])
                zero_count = 0
        return hdbn_sequence
    @staticmethod
    def DSP_NRZ(amp, Ts, f):
        return amp**2 * Ts * 0.001 * np.sinc(np.pi * f * Ts * 0.001)**2

    @staticmethod
    def DSP_RZ(amp, Ts, f):
        return amp**2 * Ts * 0.001 / 4 * np.sinc(np.pi * f * Ts * 0.001 / 2)**2

    @staticmethod
    def DSP_Miller(amp, Ts, f):
        return amp**2 * Ts * 10000 / 4 * 1 / (2 * (np.pi * f * Ts)**2 * (17 + 8 * np.cos(2 * np.pi * f * Ts * 0.001))) * \
            (23 - 2 * np.cos(np.pi * f * Ts * 0.001) - 22 * np.cos(2 * np.pi * f * Ts * 0.001) - 12 * np.cos(3 * np.pi * f * Ts * 0.001) + \
             5 * np.cos(4 * np.pi * f * Ts * 0.001) + 12 * np.cos(5 * np.pi * f * Ts * 0.001) + 2 * np.cos(6 * np.pi * f * Ts * 0.001) - \
             8 * np.cos(7 * np.pi * f * Ts * 0.001) + 2 * np.cos(8 * np.pi * f * Ts * 0.001))

    @staticmethod
    def DSP_Manchester(amp, Ts, f):
        return np.abs(amp**2 * Ts * 0.66 * 0.01 * np.sinc(np.pi * f * Ts * 0.001 / 2)**2 * np.sin(np.pi * f * Ts * 0.001 / 2)**2)

    @staticmethod
    def DSP_HDBN(amp, Ts, f, order):
        return np.abs(2 / 3 * amp**2 * Ts * 0.01 * np.sinc(np.pi * f * Ts * 0.001)**2)

    def plot(self):
        filename = "binary_sequence_and_period.txt"
        try:
            with open(filename, 'r') as file:
                lines = file.readlines()[1:]  # Skip the first line (header)
                binary_sequence = []
                for line in lines:
                    try:
                        binary_sequence.append(int(line.split()[0]))
                    except ValueError:
                        st.warning(f"Skipping non-numeric value: {line.split()[0]}")
                period_ms = float(lines[0].split()[1])
        except Exception as e:
            st.error("An error occurred while reading the file: {}".format(e))
            return

        # Apply selected filter
        filtered_sequence = self.apply_filter(binary_sequence, self.filter_type)

        # Create time array for binary sequence
        t = np.arange(0, len(binary_sequence) * period_ms, period_ms)

        # Plot original binary sequence
        fig, ax = plt.subplots(3, 1, figsize=(10, 6))

        ax[0].step(t, binary_sequence, where='post')
        ax[0].set_title('Binary Sequence')
        ax[0].set_xlabel('Time (ms)')
        ax[0].set_ylabel('Amplitude')
        ax[0].set_ylim(-0.1, 1.1)

        # Create clock signal
        clock_period_samples = int(1000 / period_ms)  # Number of samples per clock period
        num_clock_samples = len(binary_sequence) * clock_period_samples
        clock_signal = np.zeros(num_clock_samples)
        for i in range(0, num_clock_samples, clock_period_samples):
            clock_signal[i:i + int(clock_period_samples / 2)] = 1
        t_clock = np.linspace(0, len(binary_sequence) * period_ms, num_clock_samples)

        # Plot clock signal
        ax[1].plot(t_clock, clock_signal)
        ax[1].set_title('Clock Signal')
        ax[1].set_xlabel('Time (ms)')
        ax[1].set_ylabel('Amplitude')
        ax[1].set_ylim(-0.1, 1.1)

        # Plot filtered sequence
        t_filtered = np.linspace(0, len(binary_sequence) * period_ms, len(filtered_sequence))
        ax[2].step(t_filtered, filtered_sequence, where='post')
        ax[2].set_title(f'Filtered Binary Sequence ({self.filter_type})')
        ax[2].set_xlabel('Time (ms)')
        ax[2].set_ylabel('Amplitude')
        if self.filter_type in ["Manchester", "Miller","NRZ", "HDBN"]:
            ax[2].set_ylim(-2, 2)
        else:
            ax[2].set_ylim(-0.1, 1.1)

        # Show plots
        st.pyplot(fig)

        # Plot DSP for selected filter type
        fig_dsp, ax_dsp = plt.subplots(figsize=(8, 6))
        freq_range = np.linspace(-20, 20, 1000)  # Frequency range for DSP plot
        if self.filter_type == "RZ":
            ax_dsp.plot(freq_range, [self.DSP_RZ(1, period_ms, f) for f in freq_range])
            ax_dsp.set_title('DSP - RZ')
        elif self.filter_type == "NRZ":
            ax_dsp.plot(freq_range, [self.DSP_NRZ(1, period_ms, f) for f in freq_range])
            ax_dsp.set_title('DSP - NRZ')
        elif self.filter_type == "Miller":
            ax_dsp.plot(freq_range, [self.DSP_Miller(1, period_ms, f) for f in freq_range])
            ax_dsp.set_title('DSP - Miller')
        elif self.filter_type == "Manchester":
            ax_dsp.plot(freq_range, [self.DSP_Manchester(1, period_ms, f) for f in freq_range])
            ax_dsp.set_title('DSP - Manchester')
        elif self.filter_type == "HDBN":
            ax_dsp.plot(freq_range, [self.DSP_HDBN(1, period_ms, f, self.hdbn_order) for f in freq_range])
            ax_dsp.set_title(f'DSP - HDBN (Order: {self.hdbn_order})')

        ax_dsp.set_xlabel('Frequency (Hz)')
        ax_dsp.set_ylabel('Magnitude')
        ax_dsp.grid(True)

        # Show DSP plot
        st.pyplot(fig_dsp)

st.set_option('deprecation.showPyplotGlobalUse', False)
app = BinaryTransmissionApp(st)  # Pass st to the constructor