import streamlit as st  
st.set_page_config(page_title="Image Recognition App" , page_icon=":camera:", layout="centered", initial_sidebar_state="expanded")

from dotenv import load_dotenv
load_dotenv()

import os
import google.generativeai as genai
from PIL import Image
import base64
import random

os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model=genai.GenerativeModel("gemini-1.5-flash")
def get_gemini_response(input, image):
    if input != "":
        response = model.generate_content([input, image])
    else:
        response = model.generate_content(image)
    return response.text

def set_background(image_files):
    image_file = random.choice(image_files)
    with open(image_file, "rb") as f:
        data = f.read()
    encoded = base64.b64encode(data).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url(data:image/png;base64,{encoded});
            background-size: cover;
            animation: fadeIn 2s ease-in-out;
        }}
        @keyframes fadeIn {{
            0% {{ opacity: 0; }}
            100% {{ opacity: 1; }}
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Set the background image
set_background(["image 1.jpg", "image 2.jpg", "image 3.jpg"])

st.markdown("<center><h1 style='font-style: Bold;'>ChatBot with Image Recognition</h1></center>", unsafe_allow_html=True)
input = st.text_input(" ChatBox: ", key="input")

uploaded_file = st.file_uploader("Upload or Drag and Drop an image... ", type=["jpg", "jpeg", "png"])
image = ""
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image.', use_container_width=True)

st.markdown(
    """
    <style>
    .stButton>button {
        transition: all 0.3s ease;
        box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        background-color: #28a745;
        color: white;
        border: 2px solid white;
    }
    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0 0 20px rgba(0, 0, 0, 0.2);
        background-color: #218838;
    }
    </style>
    """,
    unsafe_allow_html=True
)

submit=st.button("Generate Response")

if submit:
    if image is None:
        st.warning("Please upload an image first.", icon="⚠️")
    else:
        with st.spinner("Generating response..."):
            response = get_gemini_response(input, image)
        st.success("Response generated!", icon="✅")
        st.write(response)