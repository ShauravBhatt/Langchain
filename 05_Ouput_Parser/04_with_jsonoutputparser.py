from langchain_core.prompt_values import PromptValue
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate

# NEW:
# JsonOutputParser tries to convert the LLM's response
# into a Python dictionary/list by parsing JSON.
from langchain_core.output_parsers import JsonOutputParser


load_dotenv()

llm = HuggingFaceEndpoint(
    model="meta-llama/Llama-3.1-8B-Instruct",
    task="conversational",
    provider="featherless-ai"
)

model = ChatHuggingFace(llm=llm)


parser = JsonOutputParser()


template = PromptTemplate(
    template="""Give me the name, age and city of a fictional person
{format_instruction}""",

    input_variables=[],

    # JsonOutputParser generates instructions telling the LLM
    # to return its answer in JSON format.
    #
    # For example, it may guide the model towards:
    # {
    #   "name": "...",
    #   "age": ...,
    #   "city": "..."
    # }
    partial_variables={
        "format_instruction": parser.get_format_instructions()
    }
)


# LLM output → JsonOutputParser → Python dictionary
chain = template | model | parser


result = chain.invoke({})


# JsonOutputParser returns Python data instead of a raw string.
# Usually this will be a dict in this example.
print(type(result))
print(result)


# ---------------------------------------------------------
# IMPORTANT LIMITATION OF JsonOutputParser
# ---------------------------------------------------------
#
# JsonOutputParser can tell the LLM:
# "Give me JSON"
#
# But here we have NOT defined a strict schema such as:
#
# {
#     "name": string,
#     "age": integer,
#     "city": string
# }
#
# So the parser mainly cares that the output is valid JSON.
# It does NOT give us strong validation of:
#
# - which fields must exist
# - exact field names
# - exact data types
# - allowed values
#
# For example, the model could potentially return:
#
# {
#     "name": "Rahul",
#     "age": "twenty one",
#     "country": "India"
# }
#
# This is valid JSON, so JsonOutputParser can parse it,
# but it does NOT match the structure we actually wanted.
#
# This is the main problem:
#
# JsonOutputParser
#      ↓
# Valid JSON
#      ↓
# But no strict schema validation
#
# Later, PydanticOutputParser solves this by letting us
# define the exact expected structure using a Pydantic model.
#
# PydanticOutputParser
#      ↓
# Schema + parsing + validation