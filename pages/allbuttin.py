import streamlit as st
import subprocess

def main():
    st.title("Script Selector")

    button_list1 = [
        ("Sequence binaire emis", "https://zany-succotash-6j7v4r7547xcjrw-8501.app.github.dev/binaryT#binary-transmission"),
        ("Code en ligne", "Code_en_ligne.py"),
        ("Modulation", "Modulation.py")
    ]
    for button_text, url in button_list1:
        if st.button(button_text):
            if url.startswith("http"):
                st.markdown(f"[{button_text}]({url})")
            else:
                execute_script(url)

    button_list2 = [
        ("Canal de Propagation(avec Bruit)", "Canal_de_Propagation.py"),
        ("Sequence binaire recus", "binaryT.py"),
        ("decision", "decision.py"),
        ("Horloge", "Horloge.py"),
        ("Filtre de Reception", "Filtre_de_Reception.py"),
        ("Demodulation", "Demodulation.py"),
        ("Filtre d'émission", "Filtre_d_emission.py")
    ]
    for button_text, script_name in button_list2:
        if st.button(button_text):
            execute_script(script_name)

def execute_script(script_name):
    try:
        subprocess.Popen(["streamlit", "run", script_name])
    except FileNotFoundError:
        with open(script_name, "w") as file:
            file.write("# Placeholder script created!")
        subprocess.Popen(["streamlit", "run", script_name])

if __name__ == "__main__":
    main()
