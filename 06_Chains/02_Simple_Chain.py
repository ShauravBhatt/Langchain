from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
# langchain_huggingface provides Hugging Face integrations.
# ChatHuggingFace = chat-model wrapper
# HuggingFaceEndpoint = connects to a Hugging Face hosted model

from langchain_core.prompts import PromptTemplate
# Creates reusable prompts with variables like {topic}

from dotenv import load_dotenv
# Loads environment variables from the .env file

from langchain_core.output_parsers import StrOutputParser
# Converts the model's output into a plain string


load_dotenv()
# Loads API keys/configuration stored in .env


llm = HuggingFaceEndpoint(
    model="meta-llama/Llama-3.1-8B-Instruct",
    task="conversational",
    provider="featherless-ai"
)
# Creates the connection to the Hugging Face model


model = ChatHuggingFace(llm=llm)
# Wraps the HuggingFaceEndpoint as a chat model


prompt = PromptTemplate(
    template="Generate 5 interesting facts about {topic}",
    input_variables=["topic"]
)
# {topic} is a variable that will be filled when the chain runs


parser = StrOutputParser()
# Parser that converts the model response into a normal string


# LCEL connects these components from left to right:
#
# input → prompt → model → parser → output
chain = prompt | model | parser


# Runs the complete chain with the given input.
result = chain.invoke({"topic": "AI"})

print(result)


# get_graph() gives the chain's structure.
# print_ascii() prints that structure in the terminal.
#
# It only VISUALIZES the chain; it does not run it.
chain.get_graph().print_ascii()


# Graph roughly represents:
#
# PromptInput
#      ↓
# PromptTemplate
#      ↓
# ChatHuggingFace
#      ↓
# StrOutputParser
#      ↓
# StrOutputParserOutput