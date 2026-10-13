from langchain_community.document_loaders import WebBaseLoader
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser

load_dotenv()


llm = HuggingFaceEndpoint(
    model="meta-llama/Llama-3.1-8B-Instruct",
    task="conversational",
    provider="featherless-ai"
)

model = ChatHuggingFace(llm=llm)

parser = StrOutputParser()

# URL of the webpage we want to extract content from
url = "https://www.amazon.in/ASUS-Marshmallow-Keyboard-Lightweight-Bluetooth/dp/B0CFF1XMT4/ref=sr_1_3?_encoding=UTF8&sr=8-3"

# WebBaseLoader fetches the webpage and extracts its readable content
loader = WebBaseLoader(url)

# Loads the webpage content into Document object(s)
docs = loader.load()

prompt = PromptTemplate(
  template="Give me a very concise summary of whole product including people reviews sentiment and all too in pointers format with proper formatting \n {content}",
  input_variables=['content']
)

# print(docs[0].page_content)

# Connect Prompt → LLM → Output Parser
chain = prompt | model | parser

# Send extracted webpage content to the LLM
result = chain.invoke({
    'content': docs[0].page_content
})

print(result)


# --------------------------------------------------
# USE CASE:
# → Extract content from webpages
# → Summarize articles/products/documentation
# → Build website-based Q&A or RAG systems
#
# LIMITATIONS:
# → JavaScript-heavy pages may not extract properly.
# → Login/protected pages may not be accessible.
# → Website structure can affect extraction.
# → Extracted content may be incomplete.
#
# IMPORTANT:
# WebBaseLoader only extracts webpage content.
# The LLM performs the actual analysis/summarization.
#
# In this example:
# WebBaseLoader → Product page content
# LLM → Product summary + review sentiment
#
# Review sentiment is reliable only if the actual
# review content was successfully extracted.
# --------------------------------------------------