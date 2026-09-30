from dotenv import load_dotenv
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

load_dotenv()

# Connect to the Hugging Face model
llm = HuggingFaceEndpoint(
    model="Qwen/Qwen3-8B",
    task="conversational",
    provider="featherless-ai"
)

model = ChatHuggingFace(llm=llm)

# SystemMessage defines the AI's overall behavior
chat_history = [
    SystemMessage(
        content="You are a helpful assistant, willing to answer my queries in accurate and best creative way using facts and figures."
    )
]

while True:
    user_input = input("You: ")

    # Check exit before adding it to conversation history
    if user_input == "exit":
        break

    # Add user's message to history
    chat_history.append(
        HumanMessage(content=user_input)
    )

    # Send the complete conversation to the model
    result = model.invoke(chat_history)

    # Add AI's response to history
    chat_history.append(
        AIMessage(content=result.content)
    )

    print("AI:", result.content)

print(chat_history)