import os
import streamlit as st

def run():
    st.set_page_config(
        page_title=" Chaînes de transmission  numérique ",
        page_icon="🚀"
    )

    # Paths to the images
    image2_path = os.path.join(os.path.dirname(__file__), "image.jpg")
    image1_path = os.path.join(os.path.dirname(__file__), "image.png")

    # Create a layout with two columns
    col1,col4, col2, col3 = st.columns([1.5,2, 2, 1.5])

    with col1:
        st.image(image1_path, use_column_width=True)

    with col2:
        # st.subheader(" Chaînes de transformation numérique")
        # st.write("Les chaînes de transformation numérique sont utilisées pour convertir des données d'un format à un autre.")
        st.markdown(
            """
    
"""
        )

    with col3:
        st.image(image2_path, use_column_width=True)
    st.subheader(" Chaînes de transformation numérique")
    st.write("Les chaînes de transmission numérique sont des systèmes complexes qui permettent de transférer des informations numériques d'un point à un autre..")
    st.markdown(
            """
    ### Filtres communs :

    - **Filtre d'émission** : Appliqué avant l'émission pour optimiser le signal à transmettre.
    - **Filtre de réception** : Utilisé pour filtrer les signaux reçus et éliminer le bruit.
    - **Modulateur** : Utilisé pour encoder l'information numérique sur une onde porteuse analogique, 
        facilitant ainsi la transmission sur une distance plus longue ou dans des conditions de bruit.
    - **Filtre de démodulation** : Utilisé pour extraire l'information du signal modulé.
            """
        )
    st.write("""Ces chaînes de transmission jouent un rôle essentiel dans de nombreux domaines tels que les télécommunications,
              l'informatique, l'électronique industrielle ou encore l'internet des objets.""")
    col7,col8, col9, col6 = st.columns([1.5,2, 2, 1.5])
    
    with col6:
        st.subheader(" charaf orhanou")
if __name__ == "__main__":
    run()
