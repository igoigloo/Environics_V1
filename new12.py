import streamlit as st
import pandas as pd
import openai

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
        engine="text-ada-001",
        prompt=full_prompt,
        max_tokens=150
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
                    prompt_part1 = get_openai_insight(
                        "As a chief business strategist, analyze the provided data to identify a business idea "
                        "that caters specifically to the unique needs and preferences of the selected demographic group. "
                        "Focus on how the metrics in the dataset reveal specific opportunities or needs within the group. "
                        "Your initial output should include: "
                        "1. The name of the business idea. "
                        "2. A description of the business idea. "
                        , data_context, st.session_state.user_type
                    )

                    prompt_part2 = get_openai_insight(
                        "Continuing with the business idea identified, detail the specific metrics from the dataset that support this idea. "
                        "Explain how these metrics demonstrate the viability and potential success of the business idea in addressing the "
                        "needs and preferences of the target demographic group. Include: "
                        "1. The metrics used from the dataset, specifying with numbers."
                        , data_context, st.session_state.user_type
                    )

                    prompt_part3a = get_openai_insight(
                        "Based on the previously identified business idea, outline the practical steps for implementing this idea "
                        "within the trade region. Focus on the initial stages of implementation, considering the specific requirements "
                        "and challenges of the selected trade area. This part should include: "
                        "1. Practical steps for implementing the business idea in the selected trade area."
                        , data_context, st.session_state.user_type
                    )

                    prompt_part3b = get_openai_insight(
                        "Continuing with the development of the business implementation plan, consider external market factors, trends, "
                        "and demographic insights that support the viability and success of the business idea. Develop specific strategies "
                        "to engage with the target demographic group, based on the identified needs and preferences. This part should cover: "
                        "1. How external market factors, trends, and demographic insights support the viability and success of the business idea. "
                        "2. Specific strategies to engage with the target demographic group based on the identified needs and preferences."
                        , data_context, st.session_state.user_type
                    )


                    idea = prompt_part1 + prompt_part2 + prompt_part3a + prompt_part3b
                    st.write("Business Idea:", idea)

            if st.button("Generate Marketing Strategy"):
                with st.spinner('Generating marketing strategy...'):
                    strategy = get_openai_insight("Craft a marketing strategy that targets the diverse demographic composition detailed in the data, with a special focus on the significant permanent resident communities. Include culturally tailored messaging, appropriate media channels for these segments, and marketing tactics that resonate with their cultural values and consumption patterns. Propose ways to measure the impact and effectiveness of these culturally nuanced marketing efforts.", data_context, st.session_state.user_type)
                    st.write("Marketing Strategy:", strategy)

            if st.button("Identify Best Products/Brands to Launch"):
                with st.spinner('Identifying best products/brands...'):
                    products = get_openai_insight("Analyze the demographic data to recommend products or brands that would appeal to the diverse community composition, especially focusing on the larger groups of permanent residents. Highlight potential products or services that align with the cultural preferences, lifestyle, and consumption habits of these groups. Also, consider any gaps in the current market offerings that these products or brands could fill. Please list off real world products and brands", data_context, st.session_state.user_type)
                    st.write("Best Products/Brands:", products)

            if st.button("Suggest CSR Initiatives"):
                with st.spinner('Suggesting CSR initiatives...'):
                    csr = get_openai_insight("Analyze the demographic data to recommend products or brands that would appeal to the diverse community composition, especially focusing on the larger groups of permanent residents from India and China. Highlight potential products or services that align with the cultural preferences, lifestyle, and consumption habits of these groups. Also, consider any gaps in the current market offerings that these products or brands could fill.", data_context, st.session_state.user_type)
                    st.write("CSR Initiatives:", csr)

if __name__ == "__main__":
    main()
