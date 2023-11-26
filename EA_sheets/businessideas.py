import openai
import streamlit 
import pandas as pd

###
##streamlit app design

###

pre_prompt = """

Summarize the following information and provide three business ideas
for this area given the results:

"""

df = pd.read_csv("trade_area.csv")

for row in df:
  add_line = f"""
  
  The number of people in this area from {row["origin"]} is {row["count"]}, with index {row["index"]}.
  
  """
  
  pre_prompt = pre_prompt + add_line
  

response = openai.ChatCompletion.create(
model = "gpt-3.5-turbo"
messages = [{"role":"user", "content": pre_prompt}]
)