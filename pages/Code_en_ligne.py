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
        return np.repeat(binary_sequence, 2)

    def apply_NRZ(self, binary_sequence):
        return np.repeat(binary_sequence, 2)

    def apply_Miller(self, binary_sequence):
        miller_sequence = []
        for bit in binary_sequence:
            miller_sequence.extend([1, 0] if bit == 0 else [0, 1])
        return miller_sequence

    def apply_Manchester(self, binary_sequence):
        manchester_sequence = []
        for bit in binary_sequence:
            manchester_sequence.extend([1, -1] if bit == 0 else [-1, 1])
        return manchester_sequence

    def apply_HDBN(self, binary_sequence):
        hdbn_sequence = []
        prev_bit = -1
        for bit in binary_sequence:
            if bit == prev_bit:
                hdbn_sequence.extend([0] * self.hdbn_order + [bit])
            else:
                hdbn_sequence.extend([1, -1] if bit == 0 else [-1, 1])
            prev_bit = bit
        return hdbn_sequence

    @staticmethod
    def DSP_NRZ(amp, Ts, f):
        return amp**2 * Ts *0.001 * np.sinc(np.pi * f * Ts *0.001)**2

    @staticmethod
    def DSP_RZ(amp, Ts, f):
        return amp**2 * Ts *0.001/4 * np.sinc(np.pi * f * Ts *0.001/2)**2

    @staticmethod
    def DSP_Miller(amp, Ts, f):
        return amp**2 * Ts * 10000/4 * 1/(2*(np.pi*f*Ts)**2*(17+8*np.cos(2*np.pi*f*Ts*0.001)))\
            *(23-2*np.cos(np.pi*f*Ts*0.001)-22*np.cos(2*np.pi*f*Ts*0.001)-12*np.cos(3*np.pi*f*Ts*0.001)+5*np.cos(4*np.pi*f*Ts*0.001)\
                +12*np.cos(5*np.pi*f*Ts*0.001)+2*np.cos(6*np.pi*f*Ts*0.001)-8*np.cos(7*np.pi*f*Ts*0.001)+2*np.cos(8*np.pi*f*Ts*0.001))

    @staticmethod
    def DSP_Manchester(amp, Ts, f):
        return np.abs(amp**2 * Ts * 0.66 * 0.01 * np.sinc(np.pi * f * Ts*0.001/2)**2 * np.sin(np.pi * f * Ts*0.001/2)**2)

    @staticmethod
    def DSP_HDBN(amp, Ts, f, order):
        return np.abs(2/3*amp**2 * Ts * 0.01 * np.sinc(np.pi * f * Ts*0.001)**2)

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
        plt.figure(figsize=(10, 6))
        plt.subplot(3, 1, 1)
        plt.step(t, binary_sequence, where='post')
        plt.title('Binary Sequence')
        plt.xlabel('Time (ms)')
        plt.ylabel('Amplitude')
        plt.ylim(-0.1, 1.1)

        # Create clock signal
        clock_period_samples = int(1000 / period_ms)  # Number of samples per clock period
        num_clock_samples = len(binary_sequence) * clock_period_samples
        clock_signal = np.zeros(num_clock_samples)
        for i in range(0, num_clock_samples, clock_period_samples):
            clock_signal[i:i + int(clock_period_samples/2)] = 1
        t_clock = np.linspace(0, len(binary_sequence) * period_ms, num_clock_samples)

        # Plot clock signal
        plt.subplot(3, 1, 2)
        plt.plot(t_clock, clock_signal)
        plt.title('Clock Signal')
        plt.xlabel('Time (ms)')
        plt.ylabel('Amplitude')
        plt.ylim(-0.1, 1.1)

        # Plot filtered sequence
        t_filtered = np.linspace(0, len(binary_sequence) * period_ms, len(filtered_sequence))
        plt.subplot(3, 1, 3)
        plt.step(t_filtered, filtered_sequence, where='post')
        plt.title(f'Filtered Binary Sequence ({self.filter_type})')
        plt.xlabel('Time (ms)')
        plt.ylabel('Amplitude')
        if self.filter_type in ["Manchester", "Miller" , "HDBN"]:
            plt.ylim(-2, 2)
        else:
            plt.ylim(-1.1, 1.1)

        # Show plots
        st.pyplot()

        # Plot DSP for selected filter type
        plt.figure(figsize=(8, 6))
        freq_range = np.linspace(-20, 20, 1000)  # Frequency range for DSP plot
        if self.filter_type == "RZ":
            plt.plot(freq_range, [self.DSP_RZ(1, period_ms, f) for f in freq_range])
            plt.title('DSP - RZ')
        elif self.filter_type == "NRZ":
            plt.plot(freq_range, [self.DSP_NRZ(1, period_ms, f) for f in freq_range])
            plt.title('DSP - NRZ')
        elif self.filter_type == "Miller":
            plt.plot(freq_range, [self.DSP_Miller(1, period_ms, f) for f in freq_range])
            plt.title('DSP - Miller')
        elif self.filter_type == "Manchester":
            plt.plot(freq_range, [self.DSP_Manchester(1, period_ms, f) for f in freq_range])
            plt.title('DSP - Manchester')
        elif self.filter_type == "HDBN":
            plt.plot(freq_range, [self.DSP_HDBN(1, period_ms, f, self.hdbn_order) for f in freq_range])
            plt.title(f'DSP - HDBN (Order: {self.hdbn_order})')

        plt.xlabel('Frequency (Hz)')
        plt.ylabel('Magnitude')
        plt.grid(True)

        # Show DSP plot
        st.pyplot()

st.set_option('deprecation.showPyplotGlobalUse', False)
app = BinaryTransmissionApp(st)  # Pass st to the constructor
