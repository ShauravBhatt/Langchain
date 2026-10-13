from langchain_community.document_loaders import CSVLoader
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

# CSVLoader reads the CSV and converts each row into a Document
loader = CSVLoader(file_path='./08_file.csv')

data = loader.load()

# Each row generally becomes one Document
# data[0] → first row
# len(data) → number of rows loaded

prompt = PromptTemplate(
  template="Give me a complete concised summary of important trend or pattern you can find from the following data \n {data}",
  input_variables=['data']
)

chain = prompt | model | parser

# Send the loaded CSV data to the LLM for analysis
result = chain.invoke({'data': data})

# print(len(data))
# print(data[0])
print(result)


# --------------------------------------------------
# USE CASE:
# → Quickly summarize CSV datasets
# → Find basic patterns/trends using an LLM
# → Convert raw tabular data into human-readable insights
#
# LIMITATIONS:
# → LLM is not a replacement for proper data analysis.
# → Large CSVs can exceed the context window.
# → Numerical calculations/trends may be inaccurate.
# → Complex datasets should be analyzed with Pandas/SQL
#   before sending relevant results to the LLM.
#
# IMPORTANT:
# CSVLoader mainly converts CSV rows into Documents.
# It does NOT perform statistical analysis itself.
#
# FLOW:
# CSV → CSVLoader → Documents/Rows → Prompt → LLM → Insights
# --------------------------------------------------