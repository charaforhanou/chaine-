import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

class BinaryTransmissionApp:
    def __init__(self, binary_sequence, period_ms):
        self.binary_sequence = binary_sequence
        self.period_ms = period_ms

    def plot(self):
        if not self.binary_sequence or not self.binary_sequence.isdigit():
            st.error("Please enter a valid binary sequence.")
            return

        binary_sequence = [int(bit) for bit in self.binary_sequence]
        t = np.arange(0, len(binary_sequence) * self.period_ms, self.period_ms)
        clock_period_samples = int(1000 / self.period_ms)
        clock_signal = np.zeros(len(binary_sequence) * clock_period_samples)
        clock_signal[::clock_period_samples] = 1
        t_clock = np.arange(0, len(clock_signal))
        rect_width = int(clock_period_samples / 2)
        rect_signal = np.zeros_like(clock_signal)
        for i in range(0, len(clock_signal), clock_period_samples):
            rect_signal[i:i + rect_width] = 1

        # Create binary sequence plot
        fig, axs = plt.subplots(2, 1)
        axs[0].step(t, binary_sequence, where='post')
        axs[0].set_title('Binary Sequence')
        axs[0].set_xlabel('Time (ms)')
        axs[0].set_ylabel('Bit')
        axs[0].set_ylim(-0.1, 1.1)

        # Create clock plot
        axs[1].plot(t_clock, rect_signal)
        axs[1].set_title('Clock Signal')
        axs[1].set_xlabel('Time (ms)')
        axs[1].set_ylabel('Amplitude')
        axs[1].set_ylim(-0.1, 1.1)

        # Show plots
        st.pyplot(fig)

def read_binary_sequence_and_period(file_path):
    try:
        with open(file_path, "r") as file:
            lines = file.readlines()
            if len(lines) >= 2:
                binary_sequence = lines[0].strip().split()[2]  # Extract binary sequence from file
                period_ms = float(lines[1].strip().split()[2])  # Extract period (ms) from file
                return binary_sequence, period_ms
            else:
                st.error("File doesn't contain enough lines.")
    except FileNotFoundError:
        st.error("File not found.")

def main():
    st.title("Script Selector")

    button_list1 = [
        ("Sequence binaire emis", "BinaryTransmissionApp")
    ]
    for button_text, url in button_list1:
        if st.button(button_text):
            if url == "BinaryTransmissionApp":
                binary_sequence, period_ms = read_binary_sequence_and_period("/workspaces/chaine-/binary_sequence_and_period.txt")
                if binary_sequence and period_ms:
                    app = BinaryTransmissionApp(binary_sequence, period_ms)
                    app.plot()

    button_list2 = [
        ("Code en ligne", "Code_en_ligne.py"),
        ("Modulation", "Modulation.py"),
        ("Canal de Propagation(avec Bruit)", "Canal_de_Propagation.py"),
        ("Sequence binaire recus", "binaryT.py"),
        ("decision", "decision.py"),
        ("Horloge", "Horloge.py"),
        ("Filtre de Reception", "Filtre_de_Reception.py"),
        ("Demodulation", "Demodulation.py"),
        ("Filtre d'émission", "Filtre_d_emission.py")
        # Add other scripts here
    ]
    for button_text, script_name in button_list2:
        if st.button(button_text):
            run_or_open(script_name)

def run_or_open(url):
    # Your run_or_open function remains unchanged
    pass

if __name__ == "__main__":
    main()
