import streamlit as st
import openai
import os
import PyPDF2 as pdf
from dotenv import load_dotenv
import json

load_dotenv() ## load all our environment variables

# Configure OpenAI with your API key
openai.api_key = os.getenv("OPENAI_API_KEY")

def get_openai_response(input_text):
    response = openai.Completion.create(
        engine="gpt-3.5-turbo-instruct", 
        prompt=input_text,
        max_tokens=10,
    )
    return response.choices[0].text

def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in range(len(reader.pages)):
        page = reader.pages[page]
        text += str(page.extract_text())
    return text

# Prompt Template
input_prompt = """
Hey, act like a skilled or very experienced ATS (Application Tracking System)
with a deep understanding of the tech field, software engineering, data science, data analysis,
and big data engineering. Your task is to evaluate the resume based on the given job description.
You must consider that the job market is very competitive and you should provide the
best assistance for improving the resumes. Assign the percentage match based 
on JD and
the missing keywords with high accuracy.
resume: {text}
description: {jd}

I want the response in one single string having the structure
{{"JD Match": "%", "Missing Keywords": [], "Profile Summary": ""}}
"""

st.title("Smart ATS")
st.text("Improve Your Resume ATS")
jd = st.text_area("Paste the Job Description")
uploaded_file = st.file_uploader("Upload Your Resume", type="pdf", help="Please upload the PDF")

submit = st.button("Submit")

if submit:
    if uploaded_file is not None:
        text = input_pdf_text(uploaded_file)
        prompt = input_prompt.format(text=text, jd=jd)
        response = get_openai_response(prompt)
        st.subheader(response)
