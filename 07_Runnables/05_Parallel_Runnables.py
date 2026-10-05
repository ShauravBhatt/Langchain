from langchain_core.runnables.base import RunnableSequence
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain_core.runnables import RunnableParallel, RunnableSequence
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

llm2 = HuggingFaceEndpoint(
    model="Qwen/Qwen2.5-7B-Instruct",
    task="conversational",
    provider="featherless-ai"
)

model2 = ChatHuggingFace(llm=llm2)

prompt = PromptTemplate(
    template='Write a beautiful and knowledgable tweet for X.com and topic is \n {topic}',
    input_variables=['topic']
)

prompt2 = PromptTemplate(
    template='Write a beautiful and knowledgable linekdin post on topic \n {topic}',
    input_variables=['topic']
)

parser = StrOutputParser()


# RunnableParallel runs multiple Runnables at the SAME TIME
# using the SAME input.
#
# Input:
#     {'topic': 'AI'}
#
#                ┌── prompt → model → parser → tweet
# topic ─────────┤
#                └── prompt2 → model2 → parser → linkedin
#
# Each branch is independent, but both receive the same input.
parallel_chain = RunnableParallel({
    'tweet': RunnableSequence(prompt, model, parser),
    'linkedin': RunnableSequence(prompt2, model2, parser)
})


# The output is a dictionary containing the result
# of every parallel branch.
result = parallel_chain.invoke({'topic': 'AI'})

print(result['tweet'])
print(result['linkedin'])