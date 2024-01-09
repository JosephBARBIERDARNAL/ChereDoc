import streamlit as st
import pandas as pd
from src.func import *
from openai import OpenAI, BadRequestError
client = OpenAI(api_key=st.secrets["api_key"])

# load the questionnaire
df = pd.read_csv('data/doc.csv')

st.title('From question id to question')
space(2)

# get the right wave questionnaire
wave_number = st.selectbox(
    'Choose a wave',
    ['Wave ' + str(val) for val in range(1, 9+1)])
wave_number = wave_number[-1]
wave_name = f"w{wave_number}_main_en.pdf"
wave_quest = df[df['name']==wave_name]['text']
wave_quest = wave_quest.values[0]

# get the question id
column_names = []
with open(f'data/column_names/column_names_wave{wave_number}.txt', 'r') as file:
    for line in file:
        column_names.append(line.strip())
question_id = st.selectbox(
    'Choose a question id',
    column_names)

# keep ony 5 first letters
if len(question_id) in [6,7]:
    question_id = question_id[:5]

# get run validation
run = st.button('Run')
if run:
    
    # find the part correspond to the question id in the questionnaire
    content = extract_content(question_id, wave_quest)

    # ask gpt to find the question in text
    try:
        question_found = call_gpt(client, content)
        st.write(question_id)
        st.success(question_found)
    except BadRequestError:
        st.error("Question not found")
    
    


