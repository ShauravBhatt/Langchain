from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

llm = HuggingFaceEndpoint(
    model="meta-llama/Llama-3.1-8B-Instruct",
    task="conversational",
    provider="featherless-ai"
)

model = ChatHuggingFace(llm=llm)

# First prompt: generates the detailed report
prompt1 = PromptTemplate(
    template='Generate a detailed report on {topic}',
    input_variables=['topic']
)

parser = StrOutputParser()

# Second prompt: takes the previous output as {text}
# and asks the model to create a 5-point summary.
#
# NOTE: input_variables should be ['text'], because the
# template uses {text}, not {topic}.
prompt2 = PromptTemplate(
    template='Generate a 5 pointer summary from following text \n {text}',
    input_variables=['text']
)

# LCEL creates a sequential chain:
#
# topic
#  ↓
# prompt1 → model → parser
#                    ↓
#              detailed report
#                    ↓
#                 prompt2
#                    ↓
#                  model
#                    ↓
#                 parser
#                    ↓
#              final summary
#
# The output of each step automatically becomes
# the input of the next step.

chain = prompt1 | model | parser | prompt2 | model | parser

result = chain.invoke({'topic': 'Deep Learning'})

print(result)