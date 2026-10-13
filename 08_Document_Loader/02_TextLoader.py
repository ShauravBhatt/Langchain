# TextLoader → reads a text file and returns LangChain Document objects
from langchain_community.document_loaders import TextLoader

# Hugging Face integration → connects LangChain with the LLM
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint

# Used to create prompts with variables like {text}
from langchain_core.prompts import PromptTemplate

# Converts the LLM response into a simple Python string
from langchain_core.output_parsers import StrOutputParser

# Loads API keys/configuration from the .env file
from dotenv import load_dotenv

load_dotenv()


# Create connection to the Hugging Face LLM
llm = HuggingFaceEndpoint(
    model="meta-llama/Llama-3.1-8B-Instruct",
    task="conversational",
    provider="featherless-ai"
)

# Convert the endpoint into a LangChain chat model
model = ChatHuggingFace(llm=llm)

# Parser → converts model output into plain text
parser = StrOutputParser()

# Create a reusable prompt
# {text} will be replaced with the actual document content
prompt = PromptTemplate(
    template='Write a summary for the topic \n {text}',
    input_variables=['text']
)

# Create a loader for the TXT file
loader = TextLoader("./02_file.txt", encoding="utf-8")

# Load the file
# Returns a list of Document objects
docs = loader.load()

# docs[0] → first Document
# page_content → actual text inside that Document


# LCEL chain:
# Prompt → LLM → Output Parser
chain = prompt | model | parser

# Pass the document text into {text}
# The chain generates the summary
result = chain.invoke({
    'text': docs[0].page_content
})

# Print the final summary
print(result)


# --------------------------------------------------
# USE CASE:
# Read a document and directly generate an LLM response
# such as summary, explanation, classification, etc.
#
# LIMITATION:
# Entire document is sent to the LLM.
# Very large documents may exceed the context window.
# Text splitting is needed for large documents.
#
# IMPORTANT:
# This is a simple Document → LLM pipeline.
# It is NOT RAG because there is no retrieval step.
# --------------------------------------------------