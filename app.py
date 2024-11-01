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

warnings.filterwarnings('ignore')

# Configure Streamlit app title and icon
st.set_page_config(page_title="One Piece Knowledge Assistant", page_icon="🏴‍☠️", layout="wide")

with st.sidebar:
    openai.api_key = st.text_input("OpenAI API Key", type="password")
    if not (openai.api_key.startswith('sk') and len(openai.api_key) == 164):
        st.warning("Please enter a valid OpenAI API key", icon="⚠️")
    else:
        st.success("API key is valid", icon="✅")

    with st.container():
        l, m, r = st.columns((1, 3, 1))
        with l:
            st.image("path_to_strawhat_jollyroger.png", width=60)
        with m:
            st.empty()
        with r:
            st.empty()

    # Side menu
    options = option_menu(
        "Dashboard", 
        ["Home", "About Us", "Model"],
        icons=['house', 'info-circle', 'robot'],
        menu_icon="book", 
        default_index=0,
        styles={
            "icon": {"color": "#dec960", "font-size": "20px"},
            "nav-link": {"font-size": "17px", "text-align": "left", "margin": "5px", "--hover-color": "#262730"},
            "nav-link-selected": {"background-color": "#262730"}          
        })

# Session states
if 'messages' not in st.session_state:
    st.session_state.messages = []

if 'chat_session' not in st.session_state:
    st.session_state.chat_session = None

# Pages
if options == "Home":
    st.title("One Piece Knowledge Assistant")
    st.image("path_to_one_piece_background.jpg", use_column_width=True)
    st.write("Welcome to the One Piece Knowledge Assistant! Ask me anything about the One Piece world created by Eiichiro Oda.")

elif options == "About Us":
    st.title("About the One Piece Knowledge Assistant")
    st.write("This assistant is dedicated to providing information and answering questions about the world of One Piece.")

elif options == "Model":
    st.title("One Piece Knowledge Base")
    col1, col2, col3 = st.columns([1, 2, 3])

    with col2:
        query = st.text_input("Ask about One Piece", placeholder="Enter your question here...")
        submit_button = st.button("Get Answer")

    if submit_button:
        with st.spinner("Retrieving information..."):
            System_Prompt = """You are a highly advanced AI language model specialized in the world of One Piece created by Eiichiro Oda. You are knowledgeable about the characters, story arcs, locations, Devil Fruits, Haki, and important events within the One Piece universe. Your goal is to provide informative, accurate, and interesting responses about the One Piece world.

Key Elements to Address:
    Characters: Describe key characters, their backstories, affiliations, powers, and significant events they are involved in.
    Story Arcs: Provide summaries and major events of different story arcs.
    Locations: Explain notable locations, islands, seas, and their significance in the story.
    Devil Fruits: Explain Devil Fruits, their types, and abilities.
    Haki: Discuss types of Haki and its users.
    Other Lore: Share lore, such as the Void Century, World Government, Yonko, and more.

Response Style:
    - Be descriptive, accurate, and engaging.
    - Avoid spoilers for readers who may not be caught up, if possible.
    - Tailor responses to specific user questions and elaborate as needed.
"""

            user_message = query
            struct = [{'role': 'system', 'content': System_Prompt}]
            struct.append({"role": "user", "content": user_message})

            chat = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=struct
            )

            response = chat.choices[0].message.content
            struct.append({"role": "assistant", "content": response})
            st.write(response)
