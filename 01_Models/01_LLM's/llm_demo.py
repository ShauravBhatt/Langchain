# Import OpenAI LLM from LangChain
from langchain_openai import OpenAI

# Used to load variables from the .env file
from dotenv import load_dotenv

# Load the environment variables
# This will load our OPENAI_API_KEY from the .env file
load_dotenv()


# Create an OpenAI LLM object
# Here we are telling LangChain which OpenAI model to use
llm = OpenAI(model="gpt-3.5-turbo-instruct")


# Send our question/prompt to the LLM
# invoke() sends the prompt and returns the model's response
result = llm.invoke("What is the capital of India?")


# Print the response on the screen
print(result)

"""
Note:
LangChain now recommends using Chat Models instead of the older
completion-style OpenAI models.

`OpenAI` is based on the older text-completion API, while modern
OpenAI models are designed to work through the Chat API.

So, for new projects, we generally use `ChatOpenAI`.
This code is mainly useful when following older tutorials.
"""