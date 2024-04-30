import streamlit as st

def run():
    st.set_page_config(
        page_title="Chaînes de transformation numérique",
        page_icon="🚀"
    )
    st.write("# ----------------*master IT*-------------------")

    st.write("# Chaînes de transformation numérique")
   
    st.write("Les chaînes de transformation numérique sont utilisées pour convertir des données d'un format à un autre.")

    st.markdown(
        """
        ### Filtres communs :
        - **Filtre de réception** : Utilisé pour filtrer les signaux reçus et éliminer le bruit.
        - **Filtre d'émission** : Appliqué avant l'émission pour optimiser le signal à transmettre.
        - **Filtre de démodulation** : Utilisé pour extraire l'information du signal modulé.
        ### Plus d'informations :

        """
    )

if __name__ == "__main__":
    run()
