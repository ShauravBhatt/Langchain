from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import (
    RunnableLambda,
    RunnableParallel,
    RunnablePassthrough,
    RunnableSequence,
)
from langchain_core.runnables.branch import RunnableBranch
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint

load_dotenv()

llm = HuggingFaceEndpoint(
    model="meta-llama/Llama-3.1-8B-Instruct",
    task="conversational",
    provider="featherless-ai",
)

model = ChatHuggingFace(llm=llm)

prompt = PromptTemplate(
    template="Write a report on \n {topic}",
    input_variables=["topic"]
)

prompt2 = PromptTemplate(
    template="Summarize the following text and print it complete don't cut in between \n {text}",
    input_variables=["text"]
)

parser = StrOutputParser()


# Generate the report first.
report_gen_chain = RunnableSequence(prompt, model, parser)


# RunnableBranch adds conditional logic to the Runnable pipeline.
#
# Condition:
#     len(x.split()) > 500
#
# If TRUE:
#     send the report to prompt2 → model → parser
#
# If FALSE:
#     RunnablePassthrough → return the original report unchanged
#
# So it works like:
#
#     report
#       ↓
#   > 500 words?
#     /      \
#   YES      NO
#    ↓        ↓
# summarize  return as-is
branch_chain = RunnableBranch(
    (
        lambda x: len(x.split()) > 500,
        RunnableSequence(prompt2, model, parser)
    ),
    RunnablePassthrough()
)


# First generate the report,
# then apply the conditional branch to that report.
final_chain = RunnableSequence(
    report_gen_chain,
    branch_chain
)

result = final_chain.invoke({"topic": "AI Bubble"})

print(result)