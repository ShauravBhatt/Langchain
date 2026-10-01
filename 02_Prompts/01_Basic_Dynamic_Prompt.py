from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

# Connect to a Hugging Face model through an inference provider
llm = HuggingFaceEndpoint(
    model="TinyLlama/TinyLlama-1.1B-Chat-v1.0",
    task="conversational",
    provider="featherless-ai"
)

# Converts the HuggingFaceEndpoint into a chat-model interface
model = ChatHuggingFace(llm=llm)

# Streamlit UI
st.header("Research Tool")

# Takes input from the user
user_input = st.text_input("Enter your prompt")

# Runs only when the button is clicked
if st.button("Summarize"):

    # Send user's input to the model
    result = model.invoke(user_input)

    # Display only the generated text
    st.write(result.content)