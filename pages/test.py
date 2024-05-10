import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

def plot_impulses(binary_sequence):
    # Créer un tableau de temps pour chaque échantillon
    time = np.arange(len(binary_sequence))
    
    # Créer le graphe
    plt.figure(figsize=(8, 4))
    
    # Plot des impulsions
    plt.stem(time, binary_sequence, linefmt='b-', markerfmt='bo', basefmt=' ')
    
    # Étiquettes et titre
    plt.xlabel('Temps')
    plt.ylabel('Impulsions')
    plt.title('Conversion du signal d\'entrée en impulsions')
    
    # Afficher le graphe
    st.pyplot(plt)

# Application Streamlit
st.title("Conversion de signal en impulsions")
file_path = "binary_sequence_and_period.txt"
with open(file_path, 'r') as f:
        lines = f.readlines()

binary_sequence = []
period = []
for line in lines[1:]:  # Ignorer la première ligne (en-tête)
    values = line.strip().split()
    binary_sequence.append(int(values[0]))
    period.append(float(values[1]))
# Convertir la saisie en une liste d'entiers

# Tracer les impulsions
if binary_sequence:
    plot_impulses(binary_sequence)
