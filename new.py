import os
import streamlit as st
from dotenv import load_dotenv
import json
import requests
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure the Google API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to load OpenAI model and get responses
def get_gemini_response(question):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(question)
    # Extract text from response parts
    text_parts = [part.text for part in response.parts if hasattr(part, 'text')]
    return ' '.join(text_parts)

# Function to fetch shopping data
def fetch_shopping_data(query):
    url = "https://google.serper.dev/shopping"
    payload = json.dumps({"q": query})
    headers = {
        'X-API-KEY': os.getenv("SERPER_API_KEY"),
        'Content-Type': 'application/json'
    }
    response = requests.post(url, headers=headers, data=payload)
    if response.status_code == 200:
        shopping_data = response.json()  # Parse JSON response
        return shopping_data
    else:
        st.write(f"Error fetching shopping data: {response.text}")
        return None

# Initialize our Streamlit app
st.set_page_config(page_title="Fashion Genie")

st.header("Fashion Genie")

# User inputs
size = st.text_input("Enter Your Size: ", key="size")
gender = st.text_input("Enter your Gender:", key="gender")
color = st.text_input("Enter your Favourite Colour: ", key="color")
occasion = st.text_input("Which type of occasion or event would you like to wear?", key="occasion")
budget = st.text_input("What is your budget?", key="budget")

submit = st.button("Go FashionGenie")

# If ask button is clicked
if submit:
    prompt = f"Hey my size is {size} and I'm {gender}. My favourite and preferred color is {color} and I want to wear it for {occasion} and my budget is {budget}. Give me a perfect and simple outfit suggestion based on the prompts I gave! Just give the outfit suggestion like the top and the bottom. That's all!"
    response_gemini = get_gemini_response(prompt)
    st.subheader("The Response is")
    st.write(response_gemini)

    # Fetch shopping data based on the response
    shopping_data = fetch_shopping_data(response_gemini)
    if shopping_data:
        refined_prompt = f"Here are some shopping suggestions: {shopping_data}\n\nPlease present these suggestions in a structured manner,  separated as individual outfits with hyperlink of its shopping links."
        refined_response = get_gemini_response(refined_prompt)

        st.subheader("Shopping Suggestions")
        st.write(refined_response)
    else:
        st.write("Could not fetch shopping data at this time.")
