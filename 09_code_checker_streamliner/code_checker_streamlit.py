'''
Create a streamlit ui that takes in a coding question and also the code that the user has written for the question.
the ui should have a button that when clicked should check the code adn return the output of the doe and whether the code is correct or not.

'''
import streamlit as st
from llama_index.core import PromptTemplate
from llama_index.core.chat_engine import SimpleChatEngine
from llama_index.llms.google_genai import GoogleGenAI
from dotenv import load_dotenv
import os

#load the openai key into environment variable named openai_api_key
load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
os.environ["GOOGLE_API_KEY"] = api_key

def check_code(code,question,language):

    #prompt templates
    question_template = """
    you are a program or a code check assistant.You will have four inputs - the programming question,the code,the language,and 
    the addition.you need to check if the provided code is correct to solve the given question and also provide feedback on the code
    if there is an invalidity in any of the input,you are to provide feeedback on that as well
    ** programming language : ** {language}\n\n 
    ** coding question : **{question}\n\n
    **Code: **{code}\n\n
    question to you as the code checker : is the provided code correct to solve the given question ?
    output that you must produce : you are return the output in a well formed json object.The json object should contain the following :
    -"correct" : Y/N (Y if the code is correct,N if the code is correct)
    -"feedback" : Feedback on the code.This should be a string.if the code is correct,the feedbck should be "the code is correct".
    -"output" : Excute the program and show the output
    """
    qa_template = PromptTemplate(template= question_template)

    prompt = qa_template.format(language=language,question=question,code = code)

    llm= GoogleGenAI(model="gemini-1.5-pro")

    chat_engine = SimpleChatEngine.from_defaults(llm=llm)
    response = chat_engine.chat(prompt)

    return response

#--------->

#list of programming languages 
languages = ["python","Java","C","C++","JavaScript","Ruby","Swift","Go","Kotlin"]

st.title("Coding question Checker")

#dropdown
language = st.selectbox("Select the Programming Language :",languages)

#text area for questions
question=st.text_area("Enter the coding question : ",height=5)

#text area for code 
code= st.text_area("write your code here : ",height=50)

#button to check code 
if st.button("Check Code"):
    if question and code:
        output = check_code(code,question,language)
        st.write("Output :")
        st.code(output)