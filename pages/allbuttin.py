import streamlit as st
import webbrowser
import subprocess  # Only needed for local script execution

def main():
    st.title("Script Selector")

    def run_or_open(url):
        if url.startswith("http"):
            webbrowser.open_new_tab(url)
        else:
            # Streamlit Cloud: Consider alternative methods (file upload, etc.)
            # Locally, use subprocess (with appropriate error handling)
            if "local" not in st.session_state:  # Check if running on Streamlit Cloud
                try:
                    subprocess.Popen(["streamlit", "run", url])
                    st.success(f"Script '{url}' launched successfully!")
                except FileNotFoundError:
                    with open(url, "w") as file:
                        file.write("# Placeholder script created!")
                    subprocess.Popen(["streamlit", "run", url])
                except Exception as e:  # Catch other potential errors
                    st.error(f"Error launching script '{url}': {e}")

    button_list1 = [
        ("Sequence binaire emis", "https://zany-succotash-6j7v4r7547xcjrw-8501.app.github.dev/binaryT#binary-transmission"),
        ("Code en ligne", "Code_en_ligne.py"),
        ("Modulation", "Modulation.py")
    ]
    for button_text, url in button_list1:
        if st.button(button_text):
            run_or_open(url)

    button_list2 = [
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

if __name__ == "__main__":
    main()
