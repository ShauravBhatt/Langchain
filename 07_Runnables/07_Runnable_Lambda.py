from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import (
    RunnableLambda,
    RunnableParallel,
    RunnablePassthrough,
    RunnableSequence,
)
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint

load_dotenv()

llm = HuggingFaceEndpoint(
    model="meta-llama/Llama-3.1-8B-Instruct",
    task="conversational",
    provider="featherless-ai",
)

model = ChatHuggingFace(llm=llm)

prompt = PromptTemplate(
    template="Write a joke on topic \n {topic}",
    input_variables=["topic"]
)

parser = StrOutputParser()


# Normal Python function that performs our custom logic.
# Here, it counts the number of words in the text.
def word_counter(text):
    return len(text.split())


joke_gen_chain = RunnableSequence(prompt, model, parser)


# RunnableLambda converts a normal Python function
# into a Runnable.
#
# So word_counter can now participate in the chain
# just like other Runnables.
#
# Same input (generated joke) goes to both:
#
# joke ───────────────→ RunnablePassthrough → joke
#      └──────────────→ RunnableLambda → word count
parallel_chain = RunnableParallel(
    {
        "joke": RunnablePassthrough(),
        "total_words": RunnableLambda(word_counter)
    }
)


# First generate the joke,
# then pass that joke into the parallel chain.
final_chain = RunnableSequence(
    joke_gen_chain,
    parallel_chain
)

print(final_chain.invoke({"topic": "AI"}))

# Output will look like:
# {
#     'joke': '...',
#     'total_words': 15
# }