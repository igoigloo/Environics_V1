import streamlit as st
import pandas as pd
import openai

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

def get_openai_insight(prompt, data_context, user_type):
    openai.api_key = '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'
    
    # Adjust prompt based on user type
    tailored_context = f"As a {user_type}, " + data_context
    full_prompt = f"{tailored_context}\n\n{prompt}\n"
    
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=full_prompt,
        max_tokens=500
    )
    return response.choices[0].text.strip()

def main():
    if not st.session_state.continue_clicked:
        welcome_page()
    else:
        st.title(f"Business Insight Generator for {st.session_state.user_type}")

        # File uploader for multiple files
        uploaded_files = st.file_uploader("Upload Excel files", type="xlsx", accept_multiple_files=True)

        # Initialize data context
        data_context = ""
        if uploaded_files:
            all_dfs = [read_excel(uploaded_file) for uploaded_file in uploaded_files]
            data_context = process_data_for_openai(all_dfs)

        # Generate insights based on provided categories
        if data_context:
            if st.button("Generate Business Idea"):
                with st.spinner('Generating business idea...'):
                    idea = get_openai_insight("Based off the following Data Identify which ethnic group should be the best to target and create a unique business idea tailored towards that group. The response should follow the format: 1) creative name of Business Idea 2) ethnic group you targeted 3) A detailed name of analysis of why you chose that group using numbers from the file and also using external information 4) create a detailed quarterly business implementation plan using real world information about the trade area. Please format your answer neatly", data_context, st.session_state.user_type)
                    st.write("Business Idea:", idea)

            if st.button("Generate Marketing Strategy"):
                with st.spinner('Generating marketing strategy...'):
                    strategy = get_openai_insight("Craft a marketing strategy that targets the diverse demographic composition detailed in the data, with a special focus on the significant permanent resident communities. Include culturally tailored messaging, appropriate media channels for these segments, and marketing tactics that resonate with their cultural values and consumption patterns. Propose ways to measure the impact and effectiveness of these culturally nuanced marketing efforts. Please list off real world things. and make sure to be specific and explain how you used the dataset given and what metrics you used to evaluate", data_context, st.session_state.user_type)
                    st.write("Marketing Strategy:", strategy)

            if st.button("Identify Best Products/Brands to Launch"):
                with st.spinner('Identifying best products/brands...'):
                    products = get_openai_insight("Analyze the demographic data to recommend products or brands that would appeal to the diverse community composition, especially focusing on the larger groups of permanent residents. Highlight potential products or services that align with the cultural preferences, lifestyle, and consumption habits of these groups. Also, consider any gaps in the current market offerings that these products or brands could fill. Please list off real world products and brands. and make sure to explain how you used the dataset given", data_context, st.session_state.user_type)
                    st.write("Best Products/Brands:", products)

            if st.button("Suggest CSR Initiatives"):
                with st.spinner('Suggesting CSR initiatives...'):
                    csr = get_openai_insight("Analyze the demographic data to recommend products or brands that would appeal to the diverse community composition, especially focusing on the larger groups of permanent residents from India and China. Highlight potential products or services that align with the cultural preferences, lifestyle, and consumption habits of these groups. Also, consider any gaps in the current market offerings that these products or brands could fill.", data_context, st.session_state.user_type)
                    st.write("CSR Initiatives:", csr)

if __name__ == "__main__":
    main()
