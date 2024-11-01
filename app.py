import os
import openai
import streamlit as st
from PIL import Image

# Configure Streamlit app with a wide layout and a custom title
st.set_page_config(page_title="One Piece Knowledge Tool", page_icon="🏴‍☠️", layout="wide")

# Load the Jolly Roger image
try:
    jolly_roger_path = "./One Piece Jolly Roger.png"
    jolly_roger_image = Image.open(jolly_roger_path)
except FileNotFoundError:
    st.error("Jolly Roger image not found. Please ensure the file 'One Piece Jolly Roger.png' is in the same directory as this script.")

# CSS for background image
background_css = """
<style>
    .stApp {{
        background-image: url('GrandlineMap.png');
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    /* Style for the main content box to make it stand out */
    .main-content {{
        background-color: rgba(255, 255, 255, 0.8);
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }}
</style>
"""

# Inject CSS into the Streamlit app
st.markdown(background_css, unsafe_allow_html=True)

# Sidebar with OpenAI API key input
with st.sidebar:
    openai.api_key = st.text_input("OpenAI API Key", type="password")
    if not (openai.api_key.startswith('sk') and len(openai.api_key) == 164):
        st.warning("Please enter a valid OpenAI API key", icon="⚠️")
    else:
        st.success("API key is valid", icon="✅")

    # Display the Jolly Roger image in the sidebar if it was loaded
    if 'jolly_roger_image' in locals():
        st.image(jolly_roger_image, width=80, caption="Straw Hat Pirates Jolly Roger")

# System prompt for better accuracy
system_prompt = """
You are an AI expert on the One Piece universe. Your task is to provide accurate and precise information directly related to Eiichiro Oda’s One Piece series.
Follow these guidelines:
1. Be factually accurate and only answer with information from the One Piece universe.
2. Do not speculate or provide any information outside of One Piece lore.
3. Be concise but thorough, providing relevant details where appropriate.
4. If a question is unclear or unanswerable from the source material, reply with "I am unable to answer that question accurately."
"""

# Function to get the answer from OpenAI
def get_one_piece_answer(query):
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": query}
    ]
    try:
        # Making the OpenAI call with a lower temperature for accuracy
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=messages,
            temperature=0.2  # Lower temperature for more focused and accurate answers
        )
        answer = response.choices[0].message.content.strip()
        
        # Validate answer length or content to retry if off-track
        if "One Piece" not in answer and len(answer.split()) < 10:
            return "I'm unable to answer that question accurately."
        return answer

    except Exception as e:
        return f"Error: {e}"

# Main content container with styling
st.markdown('<div class="main-content">', unsafe_allow_html=True)
st.title("One Piece Knowledge Tool")
st.write("Explore and interact with information about the One Piece world!")

# Input for user questions
one_piece_input = st.text_input("Ask about the One Piece world", placeholder="Enter your question here")
submit_button = st.button("Get Answer")

if submit_button and one_piece_input:
    with st.spinner("Retrieving knowledge..."):
        # Get the answer using OpenAI's API
        response = get_one_piece_answer(one_piece_input)
        st.write(response)
st.markdown('</div>', unsafe_allow_html=True)
