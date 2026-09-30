from dotenv import load_dotenv
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint

load_dotenv()

# Connect to the Hugging Face model
llm = HuggingFaceEndpoint(
    model="Qwen/Qwen3-8B",
    task="conversational",
    provider="featherless-ai"
)

model = ChatHuggingFace(llm=llm)

# Create conversation messages with specific roles
messages = [

    # Defines the model's behavior/instructions
    SystemMessage(
        content="You are a helpful assistant, answer all the queries patiently and accurately."
    ),

    # User's message
    HumanMessage(content="Tell me about langchain.")
]

# Send the complete message list to the model
result = model.invoke(messages)

# Add the AI's response to the conversation history
messages.append(
    AIMessage(content=result.content)
)

# Print complete conversation
print(messages)