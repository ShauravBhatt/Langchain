from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage


chat_template = ChatPromptTemplate([
    # Defines the AI's role
    ("system", "You are a helpful customer support agent"),

    # Inserts previous conversation here
    MessagesPlaceholder(variable_name="chat_history"),

    # Takes the current user query
    ("human", "{query}")
])


chat_history = []

# Read previous chat history
with open("./05_Chat_History.txt", "r") as f:
    for line in f.readlines():

        # Convert each line into the correct message type
        if line.startswith("HumanMessage"):
            chat_history.append(HumanMessage(content=line))

        elif line.startswith("AIMessage"):
            chat_history.append(AIMessage(content=line))


print(chat_history)


# Insert chat history + current query into the template
prompt = chat_template.invoke({
    "chat_history": chat_history,
    "query": "Where is my refund"
})

print(prompt)