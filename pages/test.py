import streamlit as st
from streamlit_webrtc import VideoTransformerBase, webrtc_streamer
import cv2

class VideoTransformer(VideoTransformerBase):
    def __init__(self):
        # Specify the full path to the haarcascade_frontalface_default.xml file
        self.face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

    def transform(self, frame):
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        gray = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        for (x, y, w, h) in faces:
            cv2.rectangle(frame_rgb, (x, y), (x+w, y+h), (255, 0, 0), 2)
        return frame_rgb

def main():
    st.title("Face Detection with OpenCV and Streamlit")

    webrtc_streamer(key="example", video_transformer_factory=VideoTransformer)

if __name__ == "__main__":
    main()
