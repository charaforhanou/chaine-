import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

def whitening_filter(N, cutoff_freq):
    """
    Compute the frequency response of a whitening filter.
    
    Parameters:
    N (int): Number of samples
    cutoff_freq (float): Cutoff frequency of the whitening filter
    
    Returns:
    numpy.ndarray: Frequency response of the whitening filter
    """
    # Create the frequency axis
    f = np.linspace(0, 0.5, N//2+1)
    
    # Compute the frequency response
    H = np.sqrt(f / cutoff_freq)
    H[f > cutoff_freq] = 0
    
    return H

def plot_whitening_filter(N, cutoff_freq):
    """
    Plot the frequency response of the whitening filter.
    
    Parameters:
    N (int): Number of samples
    cutoff_freq (float): Cutoff frequency of the whitening filter
    """
    # Compute the frequency response
    H = whitening_filter(N, cutoff_freq)
    
    # Create the figure and axis
    fig, ax = plt.subplots(figsize=(8, 6))
    
    # Plot the frequency response
    ax.stem(np.linspace(0, 0.5, N//2+1), np.abs(H))
    ax.set_xlabel('Normalized Frequency')
    ax.set_ylabel('Magnitude')
    ax.set_title('Whitening Filter Frequency Response')
    
    # Display the plot in Streamlit
    st.pyplot(fig)

def plot_dsp(N, cutoff_freq):
    """
    Plot the discrete-time Fourier transform (DSP) of the whitening filter.
    
    Parameters:
    N (int): Number of samples
    cutoff_freq (float): Cutoff frequency of the whitening filter
    """
    # Compute the frequency response
    H = whitening_filter(N, cutoff_freq)
    
    # Create the figure and axis
    fig, ax = plt.subplots(figsize=(8, 6))
    
    # Plot the DSP
    ax.plot(np.linspace(-0.5, 0.5, N), np.abs(np.fft.fft(H, N)))
    ax.set_xlabel('Normalized Frequency')
    ax.set_ylabel('Magnitude')
    ax.set_title('Whitening Filter Discrete-Time Fourier Transform (DSP)')
    
    # Display the plot in Streamlit
    st.pyplot(fig)

# Streamlit app
st.title("Whitening Filter and DSP")

# Get user input for the number of samples and cutoff frequency
N = st.number_input("Number of Samples", min_value=100, max_value=10000, value=1000, step=100)
cutoff_freq = st.slider("Cutoff Frequency", min_value=0.01, max_value=0.5, value=0.2, step=0.01)

# Plot the whitening filter frequency response
st.subheader("Whitening Filter Frequency Response")
plot_whitening_filter(int(N), cutoff_freq)

# Plot the DSP
st.subheader("Whitening Filter Discrete-Time Fourier Transform (DSP)")
plot_dsp(int(N), cutoff_freq)
