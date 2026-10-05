from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain_core.runnables import RunnableSequence
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

# Create the Hugging Face LLM
llm = HuggingFaceEndpoint(
    model="meta-llama/Llama-3.1-8B-Instruct",
    task="conversational",
    provider="featherless-ai"
)

# Wrap the LLM so it works as a ChatModel
model = ChatHuggingFace(llm=llm)


# First prompt:
# Input → topic
# Output → joke about that topic
prompt = PromptTemplate(
    template='Make a joke on topic \n {topic}',
    input_variables=['topic']
)


# Second prompt:
# Input → joke
# Output → short explanation of that joke
prompt2 = PromptTemplate(
    template='Explain the following joke \n {joke} \n in one short line',
    input_variables=['joke']
)


# Converts the model's output into a simple string
parser = StrOutputParser()


# RunnableSequence executes everything from left → right:
#
# topic
#   ↓
# prompt
#   ↓
# model → generates joke
#   ↓
# parser → converts joke to string
#   ↓
# prompt2 → puts joke inside the second prompt
#   ↓
# model → explains joke
#   ↓
# parser → final string
#
# Each component's output automatically becomes
# the next component's input.
chain = RunnableSequence(
    prompt,
    model,
    parser,
    prompt2,
    model,
    parser
)


# Start the complete sequence with the initial input
response = chain.invoke({'topic': 'AI'})

print(response)

# Problem:
# We only get the final explanation.
# The intermediate joke is passed forward but is not returned separately.
#
# Passthrough Runnable will solve this problem in the upcoming lecture
# by allowing us to keep/pass the intermediate value.