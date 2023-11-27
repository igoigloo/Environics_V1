import streamlit as st
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from PIL import Image
from io import BytesIO

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
    merged.plot(column='Count', ax=ax, legend=True, cmap='Greens', missing_kwds={
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

# Streamlit UI
st.title("Choropleth Map Generator for Permanent Residents")

# File uploader for Excel files
uploaded_file = st.file_uploader("Upload your Excel file", type=["xlsx"])
if uploaded_file is not None:
    # Process the Excel file
    data = pd.read_excel(uploaded_file, skiprows=4)  # Skip header rows

    # Updating column names based on the actual structure of your Excel file
    data.columns = ['Country', 'Description', 'Count', 'Percent', 'Base Count', 'Base Percent', 'Percent Penetration', 'Index']
    data = data[['Country', 'Count']]
    data = decode_country_codes(data)

    # Generate and display the choropleth map
    st.write("Choropleth Map:")
    map_image = generate_choropleth(data)
    st.image(map_image)
