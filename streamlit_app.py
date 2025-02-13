import streamlit as st
import pandas as pd
import numpy as np
import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
#import math
#from pathlib import Path


os.environ["GOOGLE_API_KEY"] = st.secrets["GOOGLE_API_KEY"]

prompt = st.text_input("enter your prompt :")


#def get_model():
#prompt_template

@st.cache_data
def generate_response(prompt):
    return "Hello world" + prompt