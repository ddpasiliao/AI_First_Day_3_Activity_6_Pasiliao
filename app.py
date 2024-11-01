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

import streamlit as st
import warnings
from streamlit_option_menu import option_menu
from streamlit_extras.mention import mention
from PIL import Image

warnings.filterwarnings('ignore')

# Configure Streamlit app
st.set_page_config(page_title="One Piece Knowledge Tool", page_icon="🏴‍☠️", layout="wide")

# Load the Jolly Roger image
try:
    jolly_roger_path = "./One Piece Jolly Roger.png"
    jolly_roger_image = Image.open(jolly_roger_path)
except FileNotFoundError:
    st.error("Jolly Roger image not found. Please ensure the file 'One Piece Jolly Roger.png' is in the same directory as this script.")

# Sidebar with OpenAI API key input
with st.sidebar:
    openai.api_key = st.text_input("OpenAI API Key", type="password")
    if not (openai.api_key.startswith('sk') and len(openai.api_key) == 164):
        st.warning("Please enter a valid OpenAI API key", icon="⚠️")
    else:
        st.success("API key is valid", icon="✅")

    # Display the Jolly Roger image in the sidebar if it was loaded
    if 'jolly_roger_image' in locals():
        st.image(jolly_roger_image, width=60)

    options = option_menu(
        "Dashboard", 
        ["Home", "About Us", "Model"],
        icons=['house', 'info-circle', 'robot'],
        menu_icon="compass", 
        default_index=0,
        styles={
            "icon": {"color": "#dec960", "font-size": "20px"},
            "nav-link": {"font-size": "17px", "text-align": "left", "margin": "5px", "--hover-color": "#262730"},
            "nav-link-selected": {"background-color": "#262730"}          
        })

# Session states for storing messages and chat session
if 'messages' not in st.session_state:
    st.session_state.messages = []

if 'chat_session' not in st.session_state:
    st.session_state.chat_session = None

# Page navigation
if options == "Home":
    st.title("Welcome to the One Piece Knowledge Tool")
    st.write("Explore and interact with information about the One Piece world!")

elif options == "About Us":
    st.title("About Us")
    st.write("This tool provides insights and knowledge based on the One Piece world by Eiichiro Oda.")

elif options == "Model":
    st.title("One Piece Knowledge Model")
    col1, col2, col3 = st.columns([1, 2, 3])

    with col2:
        one_piece_input = st.text_input("Ask about the One Piece world", placeholder="Enter your question here")
        submit_button = st.button("Get Answer")

    if submit_button:
        with st.spinner("Retrieving knowledge..."):
            # Replace the prompt with a One Piece-specific prompt
            System_Prompt = """You are a highly advanced AI language model knowledgeable in the world of One Piece by Eiichiro Oda. Your main objective is to provide accurate and relevant information based on user queries related to the One Piece universe."""

            struct = [{'role': 'system', 'content': System_Prompt}]
            struct.append({"role": "user", "content": one_piece_input})

            # Call OpenAI's Chat API
            chat = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=struct
            )

            response = chat.choices[0].message.content
            struct.append({"role": "assistant", "content": response})
            st.write(response)
