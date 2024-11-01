import os
import openai
import numpy as np
import pandas as pd
import json
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import CSVLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.prompts import ChatPromptTemplate
from langchain.vectorstores import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from openai.embeddings_utils import get_embedding
from PIL import Image

import streamlit as st
import warnings
from streamlit_option_menu import option_menu
from streamlit_extras.mention import mention

warnings.filterwarnings('ignore')

st.set_page_config(page_title="One Piece Knowledge Tool", page_icon="🏴‍☠️", layout="wide")


# Load the Jolly Roger image
try:
    jolly_roger_path = "./One Piece Jolly Roger.png"
    jolly_roger_image = Image.open(jolly_roger_path)
except FileNotFoundError:
    st.error("Jolly Roger image not found. Please ensure the file 'One Piece Jolly Roger.png' is in the same directory as this script.")

with st.sidebar:
    openai.api_key = st.text_input("OpenAI API Key", type="password")
    if not (openai.api_key.startswith('sk') and len(openai.api_key) == 164):
        st.warning("Please enter a valid OpenAI API key", icon="⚠️")
    else:
        st.success("API key is valid", icon="✅")

    with st.container() :
        l, m, r = st.columns((1, 3, 1))
        with l : st.empty()
        with m : st.empty()
        with r : st.empty()

    options = option_menu(
        "Dashboard", 
        ["🏠 Home", " 🏴‍☠️About One Piece", "☠️ Model"],
        icons = ['book', 'globe', 'tools'],
        menu_icon = "book", 
        default_index = 0,
        styles = {
            "icon" : {"color" : "#dec960", "font-size" : "20px"},
            "nav-link" : {"font-size" : "17px", "text-align" : "left", "margin" : "5px", "--hover-color" : "#262730"},
            "nav-link-selected" : {"background-color" : "#262730"}          
        })


# System prompt for better accuracy
system_prompt = """
You are an expert on the One Piece universe, providing precise and factual information solely based on the series. Please adhere to the following guidelines:

    Ensure all responses are factually accurate and strictly derived from the One Piece universe.
    Avoid speculation or information that does not pertain to One Piece lore.
    Be concise yet comprehensive, including relevant details as necessary.
    If a question is ambiguous or cannot be answered based on the source material, respond with: "I am unable to answer that question accurately.
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
submit_button = st.button("Generate Answer")

if submit_button and one_piece_input:
    with st.spinner("Retrieving knowledge..."):
        # Get the answer using OpenAI's API
        response = get_one_piece_answer(one_piece_input)
        st.write(response)
st.markdown('</div>', unsafe_allow_html=True)
