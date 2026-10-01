from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

# Load the OPENAI_API_KEY from the .env file
load_dotenv()


# Create a Chat Model using OpenAI
# temperature controls how random/creative the response can be
# max_completion_tokens limits the maximum number of output tokens
model = ChatOpenAI(
    model="gpt-4",
    temperature=0.5,
    max_completion_tokens=50
)


# Send the question to the chat model
result = model.invoke("What is the capital of India?")


# ChatOpenAI returns an AIMessage object,
# so .content is used to get only the actual text response
print(result.content)