

import PyPDF2
def read_pdf(path):
    pdf_reader = PyPDF2.PdfReader(path)
    page_text = ""
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        page_text += page.extract_text().lower()
    return page_text

def clean_text(text):
    #text = text.replace('\n', ' ')
    #text = text.replace('\t', ' ')
    text = text.replace('  ', ' ')
    text = text.replace('_', '_ ')
    return text

import streamlit as st
def space(n):
    for _ in range(n):
        st.text("")

def extract_content(question_id, text):
    start = text.find(question_id)
    if start == -1:
        print('No match found for', question_id)
        return None

    end = text.find("?", start)
    if end == -1:
        return f"No '?' found after {question_id}"

    return text[start:end]

import openai
def call_gpt(prompt, question_id=None, model="gpt-3.5-turbo", temperature=0.5):
    system_msg = f"""
    Find the question in the following text. Just returns the question.
    """
    completion = openai.ChatCompletion.create(model="gpt-3.5-turbo",
                                            messages=[{"role": "system", "content": system_msg},
                                                        {"role": "user", "content": prompt}],
                                              temperature=temperature)
    output = completion["choices"][0]["message"]["content"]
    return output