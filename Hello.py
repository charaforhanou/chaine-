import os
import streamlit as st

def run():
    st.set_page_config(
        page_title="Chaînes de transformation numérique",
        page_icon="🚀"
    )

    # Sidebar on the left side
    absolute_path = os.path.join(os.path.dirname(__file__), "OIP.jpg")
    st.sidebar.image(absolute_path, use_column_width=True)


    # # Custom sidebar on the right side
    # st.markdown(
    #     """
    #     <div style="position: fixed; right: 0; top: 0; width: 200px; background-color: #f8f9fa; padding: 20px;">
    #     <h2 style="text-align: center;">Custom Sidebar</h2>
    #     <div style="text-align: center;">
    #         <img src="OIP.jpg" alt="Logo" style="max-width: 100%; height: auto;">
    #     </div>
    #     <p>This is a custom sidebar on the right side.</p>
    #     </div>
    #     """,
    #     unsafe_allow_html=True
    # )




    st.write("# ----------------*master IT*-------------------")

    st.write("# Chaînes de transformation numérique")
   
    st.write("Les chaînes de transformation numérique sont utilisées pour convertir des données d'un format à un autre.")

    st.markdown(
        """
        ### Filtres communs :
        - **Filtre de réception** : Utilisé pour filtrer les signaux reçus et éliminer le bruit.
        - **Filtre d'émission** : Appliqué avant l'émission pour optimiser le signal à transmettre.
        - **Filtre de démodulation** : Utilisé pour extraire l'information du signal modulé.        """
    )

if __name__ == "__main__":
    run()
