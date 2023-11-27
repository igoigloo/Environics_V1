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
    .top-banner {
        border-style: solid;
        border-color: green;
        padding: 20px;
        text-align: center;
    }
    .banner-title {
        color: white;  /* Use black for title text color */
        font-size: 40px;
    }
    .banner-description {
        color: white;  /* Use black for description text color */
        font-size: 16px;
    }
    .stPlotly {
        background-color: #4CAF50;  /* Use green for Plotly chart background */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Initialize session states
if 'continue_clicked' not in st.session_state:
    st.session_state.continue_clicked = False

if 'user_type' not in st.session_state:
    st.session_state.user_type = None

    

def welcome_page():
    st.title("Welcome to the Business Insight Generator App!")
    st.write("This application allows you to upload Excel files and generates business insights based on the data. The insights are generated using OpenAI's GPT-3.")

    # User type selection
    user_type = st.radio("Select your workplace type:", ('Big Retail Firm', 'Grocery Store', 'Vendor'))

    if st.button("Continue"):
        st.session_state.continue_clicked = True
        st.session_state.user_type = user_type

def read_excel(uploaded_file):
    if uploaded_file.name.endswith('.xlsx') or uploaded_file.name.endswith('.xls'):
        return pd.read_excel(uploaded_file)
    else:
        st.error("Uploaded file is not an Excel file.")
        return pd.DataFrame()

def process_data_for_openai(dataframes):
    combined_data = pd.concat(dataframes, ignore_index=True)
    return combined_data.to_string()









def main():


if __name__ == "__main__":
    main()
