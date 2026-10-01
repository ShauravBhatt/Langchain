# Import Hugging Face chat model classes from LangChain
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from dotenv import load_dotenv

# Load environment variables (e.g. HF_TOKEN)
load_dotenv()

# Connect to a Hugging Face model running through an inference provider
llm = HuggingFaceEndpoint(
      # Model we want to use
      model="TinyLlama/TinyLlama-1.1B-Chat-v1.0",

      # Task the model is designed for
      task="conversational",

      # Provider that will run the model
      provider="featherless-ai",

      # Maximum number of tokens generated in the response
      max_new_tokens=50
)

# Convert the HuggingFaceEndpoint into a LangChain chat model
chat = ChatHuggingFace(llm=llm)

# Send a question to the chat model
result = chat.invoke("What is the capital of India")

# Print only the model's text response
print(result.content)