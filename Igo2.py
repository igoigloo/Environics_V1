import streamlit as st
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import openai
import os
from PIL import Image
from io import BytesIO
from fpdf import FPDF

# Function to decode the country codes
def decode_country_codes(data):
    country_code_mapping = {
        'NC23Q1PRCIND': 'India',
        'NC23Q1PRCCHN': 'China',
        'NC23Q1PRCPHL': 'Philippines',
        'NC23Q1PRCNGA': 'Nigeria',
        'NC23Q1PRCUSA': 'United States of America',
        'NC23Q1PRCPAK': 'Pakistan',
        'NC23Q1PRCFRA': 'France',
        'NC23Q1PRCIRN': 'Iran',
        'NC23Q1PRCBRA': 'Brazil',
        'NC23Q1PRCKOR': 'South Korea',
        'NC23Q1PRCGBR': 'United Kingdom',
        'NC23Q1PRCMEX': 'Mexico',
        'NC23Q1PRCJAM': 'Jamaica',
        'NC23Q1PRCCOL': 'Colombia',
        'NC23Q1PRCVIE': 'Vietnam',
        'NC23Q1PRCBAN': 'Bangladesh',
        'NC23Q1PRCMOR': 'Morocco',
        'NC23Q1PRCALG': 'Algeria',
        'NC23Q1PRCUKR': 'Ukraine',
        'NC23Q1PRCHKG': 'Hong Kong',
        # Add more mappings if necessary
    }
    data['Country'] = data['Country'].map(country_code_mapping)
    return data.dropna()

# Function to generate choropleth map
def generate_choropleth(data):
    world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
    merged = world.merge(data, left_on='name', right_on='Country', how='left')
    fig, ax = plt.subplots(1, 1, figsize=(15, 10))
    merged.plot(column='Count', ax=ax, legend=True, cmap='OrRd', missing_kwds={
        "color": "lightgrey",
        "edgecolor": "black",
        "hatch": "///",
        "label": "Missing values"
    })
    ax.set_title('Permanent Resident Count by Country in Trade Area', fontsize=15)
    img_buf = BytesIO()
    fig.savefig(img_buf, format='png')
    img_buf.seek(0)
    return Image.open(img_buf)

# Define a function to reset the output page state
def reset_output_page_state():
    st.session_state.output_page = False
    st.session_state.output_content = ""

# Initializing session state variables for page management
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'home'
    reset_output_page_state()

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
    .stButton > button {
    width: 100%;  # Sets the width to 100% of the sidebar
    height: 50px; # Fixed height for all buttons
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
        max_tokens=100
    )
    return response.choices[0].text.strip()


def get_openai_insight2(question, data_context, user_type):
    openai.api_key = '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'
    
    # Instructions for a nicely formatted response
    instructions = (
        "Please provide a detailed and well-structured answer to the following question. "
        "Ensure the response is clear, concise, and formatted in a readable manner."
    )

    # Tailor the context and the question for the prompt
    tailored_context = f"As a {user_type}, based on the provided data: {data_context}"
    full_prompt = f"{tailored_context}\n\n{instructions}\n\nQuestion: {question}\n\nAnswer:"

    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=full_prompt,
        max_tokens=500
    )
    return response.choices[0].text.strip()


def save_idea_to_pdf_BIG(idea, user_type):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size = 12)  # Using Arial, a standard built-in font
    # Replace unsupported characters
    idea = idea.replace("’", "'")
    pdf.cell(200, 10, txt = f"Business Insight Generator for {user_type}", ln = True, align = 'C')
    pdf.multi_cell(0, 10, txt = idea)
    pdf_output = f"business_idea_{user_type}.pdf"
    pdf.output(pdf_output)
    return pdf_output

def save_idea_to_pdf_GMS(idea, user_type):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size = 12)  # Using Arial, a standard built-in font
    # Replace unsupported characters
    idea = idea.replace("’", "'")
    pdf.cell(200, 10, txt = f"Marketing Strategy Generator for {user_type}", ln = True, align = 'C')
    pdf.multi_cell(0, 10, txt = idea)
    pdf_output = f"marketing_idea_{user_type}.pdf"
    pdf.output(pdf_output)
    return pdf_output

def save_idea_to_pdf_BPG(idea, user_type):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size = 12)  # Using Arial, a standard built-in font
    # Replace unsupported characters
    idea = idea.replace("’", "'")
    pdf.cell(200, 10, txt = f"Best Product Generator for {user_type}", ln = True, align = 'C')
    pdf.multi_cell(0, 10, txt = idea)
    pdf_output = f"product_idea_{user_type}.pdf"
    pdf.output(pdf_output)
    return pdf_output

def save_idea_to_pdf_CSR(idea, user_type):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size = 12)  # Using Arial, a standard built-in font
    # Replace unsupported characters
    idea = idea.replace("’", "'")
    pdf.cell(200, 10, txt = f"CSR Generator for {user_type}", ln = True, align = 'C')
    pdf.multi_cell(0, 10, txt = idea)
    pdf_output = f"CSR_idea_{user_type}.pdf"
    pdf.output(pdf_output)
    return pdf_output



# Conditional rendering based on the current page
if st.session_state.current_page == 'output':
    if st.session_state.output_page:
        st.title("Output Page")
        st.write(st.session_state.output_content)
        if st.button("Back to Home"):
            st.session_state.current_page = 'home'
            reset_output_page_state()
else:
    # The rest of your main page code goes here
    # ...
    pass
def main():
    if not st.session_state.continue_clicked:
        welcome_page()
    else:
        st.title(f"Business Insight Generator for {st.session_state.user_type}")

        # File uploader for multiple files
        uploaded_files = st.file_uploader("Upload Excel files", type="xlsx", accept_multiple_files=True)
        if 'uploaded_file' in st.session_state and st.session_state.uploaded_file is not None:
             #st.set_page_config(layout='wide')
             st.file_uploader("Upload Excel files", type="xlsx", accept_multiple_files=True)

        # Initialize data context
        data_context = ""
        if uploaded_files:
            all_dfs = [read_excel(uploaded_file) for uploaded_file in uploaded_files]
            data_context = process_data_for_openai(all_dfs)

        # Section for asking questions
        st.subheader("Ask a Question")
        user_question = st.text_input("Enter your question based on the data:")
        if st.button("Get Answer"):
            with st.spinner('Generating answer...'):
                # Generate answer using OpenAI based on the user's question and data context
                answer = get_openai_insight2(user_question, data_context, st.session_state.user_type)
                st.write("Answer:", answer)

        # Generate insights based on provided categories
        if data_context:
            if st.sidebar.title("Digital Consultant"):
    
                if st.sidebar.button("Generate Business Idea"):
                    with st.spinner('Generating business idea...'):
                        idea = get_openai_insight("Based off the following Data Identify which ethnic group should be the best to target and create a unique business idea tailored towards that group. The response should follow the format: 1) creative name of Business Idea 2) ethnic group you targeted 3) A detailed name of analysis of why you chose that group using numbers from the file and also using external information 4) create a detailed quarterly business implementation plan using real world information about the trade area. Please provide a detailed and well-structured answer to the question. Ensure the response is clear, concise, and formatted in a readable manner.Also add links to each external source you used", data_context, st.session_state.user_type)
                        st.write("Business Idea:", idea)

                        # Save to PDF
                        pdf_file = save_idea_to_pdf_BIG(idea, st.session_state.user_type)
                        with open(pdf_file, "rb") as file:
                            st.download_button(
                                label="Download Business Idea as PDF",
                                data=file,
                                file_name=pdf_file,
                                mime="application/octet-stream"
                            )

                        # Optional: Clean up the file after download
                        os.remove(pdf_file)

        
                if st.sidebar.button("Generate Marketing Strategy"):
                    with st.spinner('Generating marketing strategy...'):
                        strategy = get_openai_insight("Craft a marketing strategy that targets the diverse demographic composition detailed in the data, with a special focus on the significant permanent resident communities. Include culturally tailored messaging, appropriate media channels for these segments, and marketing tactics that resonate with their cultural values and consumption patterns. Propose ways to measure the impact and effectiveness of these culturally nuanced marketing efforts. Please list off real world things. and make sure to be specific and explain how you used the dataset given and what metrics you used to evaluate", data_context, st.session_state.user_type)
                        st.write("Marketing Strategy:", strategy)

                        
                        # Save to PDF
                        pdf_file = save_idea_to_pdf_GMS(strategy, st.session_state.user_type)
                        with open(pdf_file, "rb") as file:
                            st.download_button(
                                label="Download Marketing Strategy Idea as PDF",
                                data=file,
                                file_name=pdf_file,
                                mime="application/octet-stream"
                            )

                        # Optional: Clean up the file after download
                        os.remove(pdf_file)

                if st.sidebar.button("Identify Best Products/Brands to Launch"):
                    with st.spinner('Identifying best products/brands...'):
                        products = get_openai_insight("Analyze the demographic data to recommend products or brands that would appeal to the diverse community composition, especially focusing on the larger groups of permanent residents. Highlight potential products or services that align with the cultural preferences, lifestyle, and consumption habits of these groups. Also, consider any gaps in the current market offerings that these products or brands could fill. Please list off real world products and brands. and make sure to explain how you used the dataset given", data_context, st.session_state.user_type)
                        st.write("Best Products/Brands:", products)

                        # Save to PDF
                        pdf_file = save_idea_to_pdf_BPG(products, st.session_state.user_type)
                        with open(pdf_file, "rb") as file:
                            st.download_button(
                                label="Download Products Idea as PDF",
                                data=file,
                                file_name=pdf_file,
                                mime="application/octet-stream"
                            )

                        # Optional: Clean up the file after download
                        os.remove(pdf_file)

                if st.sidebar.button("Suggest CSR Initiatives"):
                    with st.spinner('Suggesting CSR initiatives...'):
                        csr = get_openai_insight("Analyze the demographic data to recommend products or brands that would appeal to the diverse community composition, especially focusing on the larger groups of permanent residents from India and China. Highlight potential products or services that align with the cultural preferences, lifestyle, and consumption habits of these groups. Also, consider any gaps in the current market offerings that these products or brands could fill.", data_context, st.session_state.user_type)
                        st.write("CSR Initiatives:", csr)

                        # Save to PDF
                        pdf_file = save_idea_to_pdf_CSR(csr, st.session_state.user_type)
                        with open(pdf_file, "rb") as file:
                            st.download_button(
                                label="CSR Idea as PDF",
                                data=file,
                                file_name=pdf_file,
                                mime="application/octet-stream"
                            )

                        # Optional: Clean up the file after download
                        os.remove(pdf_file)

                if st.sidebar.button("Choropleth Map"):
                    with st.spinner('Suggesting CSR initiatives...'):
                        # Process the Excel file
                        data = pd.read_excel(uploaded_files, skiprows=4)  # Skip header rows

                        # Updating column names based on the actual structure of your Excel file
                        data.columns = ['Country', 'Description', 'Count', 'Percent', 'Base Count', 'Base Percent', 'Percent Penetration', 'Index']
                        data = data[['Country', 'Count']]
                        data = decode_country_codes(data)

                        # Generate and display the choropleth map
                        st.write("Choropleth Map:")
                        map_image = generate_choropleth(data)
                        st.image(map_image)


if __name__ == "__main__":
    main()

if 'output_page' in st.session_state and st.session_state.output_page:
    # Output code goes here
    pass
