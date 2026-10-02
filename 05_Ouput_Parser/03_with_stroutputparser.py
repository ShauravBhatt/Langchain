from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate

# NEW:
# StrOutputParser converts the model's AIMessage output
# into a simple Python string.
from langchain_core.output_parsers import StrOutputParser


load_dotenv()

llm = HuggingFaceEndpoint(
    model="meta-llama/Llama-3.1-8B-Instruct",
    task="conversational",
    provider="featherless-ai"
)

model = ChatHuggingFace(llm=llm)


template1 = PromptTemplate(
    template="Write a detailed report on {topic}",
    input_variables=["topic"]
)

template2 = PromptTemplate(
    # \n means newline. "/n" would just be normal characters.
    template="Write a 5 line summary on the following text.\n{text}",
    input_variables=["text"]
)


# Create the parser once and use it wherever we want
# the model's output as a plain string.
parser = StrOutputParser()


# LCEL sequence:
#
# template1
#    ↓
# model
#    ↓
# parser       → converts AIMessage → string
#    ↓
# template2   → receives that string as {text}
#    ↓
# model
#    ↓
# parser       → converts final AIMessage → string
#
# The important difference from the previous code:
# We don't manually write result1.content.
# StrOutputParser extracts the useful text for us.
chain = template1 | model | parser | template2 | model | parser


# "black hole" goes into template1.
# The complete chain then runs automatically.
result = chain.invoke({"topic": "black hole"})


# Because the final StrOutputParser converted the
# AIMessage into a plain string, we can directly print(result).
print(result)