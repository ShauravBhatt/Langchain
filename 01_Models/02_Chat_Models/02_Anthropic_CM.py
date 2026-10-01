from langchain_anthropic import ChatAnthropic
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()


# Create a Claude chat model
# temperature controls how creative/random the response can be
model = ChatAnthropic(
    model_name="claude-3-5-sonnet-20241022",
    temperature=1.5
)


# Send the prompt to the model
result = model.invoke("Write a 5 line poem on engineering")


# .content gives us only the actual text response
print(result.content)