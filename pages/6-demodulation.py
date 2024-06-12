


import os
import numpy as np
import scipy.signal as signal
import streamlit as st
import matplotlib.pyplot as plt

st.set_option('deprecation.showPyplotGlobalUse', False)

def read_signal(filename):
    """Reads the modulated signal from a file."""
    with open(filename, 'r') as file:
        lines = file.readlines()
        signal_data = np.array([float(line.strip()) for line in lines if not line.startswith("#")])
    return signal_data

def apply_nrz(signal_data):
    """Apply NRZ decoding to convert the signal to binary data."""
    binary_data = ((signal_data > 0).astype(int) * 1) - ((signal_data <= 0).astype(int) * 1)

    # binary_data = (signal_data > 0).astype(int)
    return binary_data

def apply_nyquist_filter(binary_data):
    """Apply a Nyquist filter to the binary data."""
    # Assuming a simple moving average filter for demonstration
    window_size = 10  # Adjust window size as needed
    filtered_data = np.convolve(binary_data, np.ones(window_size) / window_size, mode='same')
    return filtered_data

def demodulate_signal(filtered_data):
    """Demodulate the filtered binary data to recover the original binary sequence."""
    recovered_binary_sequence = (filtered_data > 0.5).astype(int) - (filtered_data <= 0.5).astype(int)
    return recovered_binary_sequence

def main():
    st.set_page_config(
        page_title="Binary Signal Recovery",
        page_icon="🔍"
    )

    st.title("Binary Signal Recovery")

    # Parameters
    filename = 'modulated_signal_ASK.txt'

    # Read the modulated signal
    try:
        modulated_signal = read_signal(filename)

         # Apply Nyquist filter
        filtered_data = apply_nyquist_filter(modulated_signal)

        # Apply NRZ decoding
        binary_data = apply_nrz(filtered_data)

       
        # Demodulate the filtered binary data
        recovered_binary_sequence = demodulate_signal(binary_data)

        # Display the results
        st.subheader("Recovered Binary Sequence")
        st.text(recovered_binary_sequence)

        # Plot each signal separately for visualization
        fig, axs = plt.subplots(4, 1, figsize=(10, 12))

        axs[0].plot(modulated_signal)
        axs[0].set_title('Modulated Signal')

        axs[1].plot(binary_data)
        axs[1].set_title('Binary Data (After NRZ Decoding)')

        axs[2].plot(filtered_data)
        axs[2].set_title('Filtered Data (After Nyquist Filter)')

        axs[3].plot(recovered_binary_sequence)
        axs[3].set_title('Recovered Binary Sequence')

        # Adjust layout
        plt.tight_layout()

        # Show plot in Streamlit
        st.pyplot(fig)

    except Exception as e:
        st.error(f"An error occurred while reading the file: {e}")

if __name__ == "__main__":
    main()




























# import os
# import numpy as np
# import scipy.signal as signal
# import streamlit as st
# import matplotlib.pyplot as plt

# st.set_option('deprecation.showPyplotGlobalUse', False)

# def read_signal(filename):
#     """Reads the modulated signal from a file."""
#     with open(filename, 'r') as file:
#         lines = file.readlines()
#         signal_data = np.array([float(line.strip()) for line in lines if not line.startswith("#")])
#     return signal_data

# def apply_nrz(signal_data):
#     """Apply NRZ decoding to convert the signal to binary data."""
#     binary_data = (signal_data > 0).astype(int)
#     return binary_data

# def apply_nyquist_filter(binary_data):
#     """Apply a Nyquist filter to the binary data."""
#     # Assuming a simple moving average filter for demonstration
#     window_size = 10  # Adjust window size as needed
#     filtered_data = np.convolve(binary_data, np.ones(window_size) / window_size, mode='same')
#     return filtered_data

# def demodulate_signal(filtered_data):
#     """Demodulate the filtered binary data to recover the original binary sequence."""
#     recovered_binary_sequence = (filtered_data > 0.5).astype(int)
#     return recovered_binary_sequence

# def main():
#     st.set_page_config(
#         page_title="Binary Signal Recovery",
#         page_icon="🔍"
#     )

#     st.title("Binary Signal Recovery")

#     # Parameters
#     filename = 'modulated_signal_ASK.txt'

#     # Read the modulated signal
#     try:
#         modulated_signal = read_signal(filename)

#         # Apply NRZ decoding
#         binary_data = apply_nrz(modulated_signal)

#         # Apply Nyquist filter
#         filtered_data = apply_nyquist_filter(binary_data)

#         # Demodulate the filtered binary data
#         recovered_binary_sequence = demodulate_signal(filtered_data)

#         # Display the results
#         st.subheader("Recovered Binary Sequence")
#         st.text(recovered_binary_sequence)

#         # Plot the signals for visualization
#         plt.figure(figsize=(10, 6))
#         plt.plot(modulated_signal, label='Modulated Signal')
#         plt.plot(binary_data, label='Binary Data (After NRZ Decoding)')
#         plt.plot(filtered_data, label='Filtered Data (After Nyquist Filter)')
#         plt.plot(recovered_binary_sequence, label='Recovered Binary Sequence')
#         plt.xlabel('Sample')
#         plt.ylabel('Amplitude / Binary Value')
#         plt.title('Signal Processing Steps')
#         plt.legend()
#         plt.grid(True)
#         st.pyplot(plt)

#     except Exception as e:
#         st.error(f"An error occurred while reading the file: {e}")

# if __name__ == "__main__":
#     main()
