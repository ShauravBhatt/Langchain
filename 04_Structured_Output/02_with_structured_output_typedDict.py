from dotenv import load_dotenv
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from typing import TypedDict

load_dotenv()

# Connect to the Hugging Face hosted LLM.
llm = HuggingFaceEndpoint(
    model="meta-llama/Llama-3.1-8B-Instruct",
    task="conversational",
    provider="featherless-ai"
)

# Convert the endpoint into a LangChain chat model.
model = ChatHuggingFace(llm=llm)


# Define the structure we want from the LLM.
class Review(TypedDict):
    summary: str
    sentiment: str


# Tell the model to return output in the Review structure.
structured_model = model.with_structured_output(Review)


# Ask the LLM to analyze the review.
result = structured_model.invoke(
    """The hardware is great, but the software feels bloated.
    There are too many pre-installed apps that I can't remove.
    Also, the UI looks outdated compared to other brands.
    Hoping for a software update to fix this."""
)

print(result)
print(type(result))

# Access individual structured fields.
print(result["summary"])
print(result["sentiment"])


"""
CONCEPT:

with_structured_output(Review)
→ tells LangChain the exact output structure we want.

Instead of normal text, we get something like:

{
    "summary": "...",
    "sentiment": "..."
}

So `result` behaves like a structured dictionary.
"""