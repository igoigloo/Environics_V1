import streamlit as st
import pandas as pd
import openai
from fpdf import FPDF
import os

# Create a Streamlit app with improved design
st.set_page_config(page_title="Atlas Analytics")
# Custom CSS to style the app
st.markdown(
    """
    <style>
    .stButton > button {
        background-color: #4CAF50;  /* Use green color for the buttons */
        color: white;
        font-weight: bold;
        border: none;
        padding: 15px 30px;  /* Larger button */
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 18px;
        border-radius: 5px;
        cursor: pointer;
    }
    .stButton > button:hover {
        background-color: #45a049;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Initialize session states
if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'user_type' not in st.session_state:
    st.session_state.user_type = None
if 'data_context' not in st.session_state:
    st.session_state.data_context = ''

# Define functions for each page
def home_page():
    st.title("Welcome to the Business Insight Generator App!")
    st.write("This application allows you to upload Excel files and generates business insights based on the data. The insights are generated using OpenAI's GPT-3.")

    user_type = st.radio("Select your workplace type:", ('Big Retail Firm', 'Grocery Store', 'Vendor'))
    st.session_state.user_type = user_type

    if st.button("Continue"):
        st.session_state.page = 'main'

def main_page():
    st.title(f"Business Insight Generator for {st.session_state.user_type}")
    uploaded_files = st.file_uploader("Upload Excel files", type="xlsx", accept_multiple_files=True)

    if uploaded_files:
        all_dfs = [read_excel(uploaded_file) for uploaded_file in uploaded_files]
        st.session_state.data_context = process_data_for_openai(all_dfs)

    user_question = st.text_input("Enter your question based on the data:")
    if st.button("Get Answer"):
        with st.spinner('Generating answer...'):
            answer = get_openai_insight2(user_question, st.session_state.data_context, st.session_state.user_type)
            st.write("Answer:", answer)

    if st.button("AI Consultant"):
        st.session_state.page = 'ai_consultant'

def ai_consultant_page():
    st.title("AI Consultant")

    if st.button("Generate Business Idea"):
        with st.spinner('Generating business idea...'):
            idea = get_openai_insight("Business Idea Prompt", st.session_state.data_context, st.session_state.user_type)
            st.write("Business Idea:", idea)

    # Add more buttons for other functionalities

# Helper functions
def read_excel(uploaded_file):
    if uploaded_file.name.endswith('.xlsx') or uploaded_file.name.endswith('.xls'):
        return pd.read_excel(uploaded_file)
    else:
        st.error("Uploaded file is not an Excel file.")
        return pd.DataFrame()

def process_data_for_openai(dataframes):
    combined_data = pd.concat(dataframes, ignore_index=True)
    return combined_data.to_string()

def get_openai_insight(prompt, data_context, user_type):
    openai.api_key = 'YOUR_OPENAI_API_KEY'
    
    tailored_context = f"As a {user_type}, " + data_context
    full_prompt = f"{tailored_context}\n\n{prompt}\n"
    
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=full_prompt,
        max_tokens=500
    )
    return response.choices[0].text.strip()

def get_openai_insight2(question, data_context, user_type):
    openai.api_key = 'YOUR_OPENAI_API_KEY'
    
    instructions = (
        "Please provide a detailed and well-structured answer to the following question. "
        "Ensure the response is clear, concise, and formatted in a readable manner."
    )

    tailored_context = f"As a {user_type}, based on the provided data: {data_context}"
    full_prompt = f"{tailored_context}\n\n{instructions}\n\nQuestion: {question}\n\nAnswer:"

    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=full_prompt,
        max_tokens=500
    )
    return response.choices[0].text.strip()

def main():
    if st.session_state.page == 'home':
        home_page()
    elif st.session_state.page == 'main':
        main_page()
   
