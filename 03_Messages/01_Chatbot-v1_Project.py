from dotenv import load_dotenv
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain_core.messages import HumanMessage, AIMessage

load_dotenv()

# Connect to the Hugging Face model
llm = HuggingFaceEndpoint(
    model="Qwen/Qwen3-8B",
    task="conversational",
    provider="featherless-ai"
)

model = ChatHuggingFace(llm=llm)

# Stores the conversation
chat_history = []

while True:
    user_input = input("You: ")

    # Stop before adding "exit" to history
    if user_input == "exit":
        break

    # Store user's message with its role
    chat_history.append(HumanMessage(content=user_input))

    # Send complete conversation to the model
    result = model.invoke(chat_history)

    # Store AI's response with its role
    chat_history.append(AIMessage(content=result.content))

    print("AI:", result.content)

print(chat_history)