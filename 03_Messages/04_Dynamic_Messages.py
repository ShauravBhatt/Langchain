from langchain_core.prompts import ChatPromptTemplate

"""
Note:
The previous approach using SystemMessage and HumanMessage
is not being used here because ChatPromptTemplate is specifically
designed to create chat messages from role-based templates.

So instead of manually creating:
SystemMessage(...)
HumanMessage(...)

we can use the simpler tuple format:
("system", "...")
("human", "...")

This makes the prompt reusable with variables like {domain} and {topic}.
"""

# Create a chat prompt using role + message template
chat_template = ChatPromptTemplate([
    
    # System message → defines AI's role
    ("system", "You are a helpful {domain} expert"),

    # Human message → user's question
    ("human", "Explain in simple terms, what is the {topic}")
])

# Replace {domain} and {topic} with actual values
prompt = chat_template.invoke({
    "domain": "cricket",
    "topic": "Dusra"
})

# Print the generated prompt messages
print(prompt)