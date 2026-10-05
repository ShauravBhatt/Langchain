from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain_core.runnables import RunnableSequence, RunnableParallel, RunnablePassthrough
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

prompt = PromptTemplate(
    template='Write a joke on topic \n {topic}',
    input_variables=['topic']
)

prompt2 = PromptTemplate(
    template='Explain the following joke \n {joke} \n in one short line',
    input_variables=['joke']
)

parser = StrOutputParser()


# First generate the joke.
joke_gen_chain = RunnableSequence(prompt, model, parser)


# After the joke is generated, we need to use it in TWO places:
#
# 1. Keep the original joke
# 2. Send the joke to prompt2 for explanation
#
# RunnablePassthrough() simply forwards the input unchanged.
#
# So if input = "generated joke":
#
#     joke ───────────────→ joke
#          └──────────────→ prompt2 → model → explanation
#
# RunnableParallel collects both outputs into one dictionary.
parallel_chain = RunnableParallel({
    'joke': RunnablePassthrough(),
    'explanation': RunnableSequence(prompt2, model, parser)
})


# First generate the joke,
# then pass that joke into the parallel chain.
#
# joke_gen_chain output:
#     "generated joke"
#
# parallel_chain output:
#     {
#         'joke': 'generated joke',
#         'explanation': '...'
#     }
final_chain = RunnableSequence(
    joke_gen_chain,
    parallel_chain
)


output = final_chain.invoke({'topic': 'Hacking'})

print(output)