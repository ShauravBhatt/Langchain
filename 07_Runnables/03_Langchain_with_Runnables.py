import random
from abc import ABC, abstractmethod


# ============================================================
# 1. COMMON RUNNABLE INTERFACE
# ============================================================
# Every Runnable must follow the same interface: invoke()
#
# This solves the old problem where:
#     LLM            → predict()
#     PromptTemplate → format()
#
# Now both can be called using:
#     runnable.invoke(input)
#
# This common interface is what makes components composable.
# ============================================================

class Runnable(ABC):

    @abstractmethod
    def invoke(self, input_data):
        pass


# ============================================================
# 2. NAKLI LLM
# ============================================================
# Our fake LLM is now a Runnable.
#
# Input:
#     prompt
#
# Output:
#     response
# ============================================================

class NakliLLM(Runnable):

    def __init__(self):
        print('LLM Created')

    # Common Runnable interface
    def invoke(self, prompt):

        response_list = [
            'Delhi is the capital of india',
            'Agentic AI is the next booming stuff',
            'AI stands for Artificial Intelligence'
        ]

        return {
            'response': random.choice(response_list)
        }

    # Old-style method.
    # Kept only to compare with the previous approach.
    def predict(self, prompt):

        response_list = [
            'Delhi is the capital of india',
            'Agentic AI is the next booming stuff',
            'AI stands for Artificial Intelligence'
        ]

        return {
            'response': random.choice(response_list)
        }


# ============================================================
# 3. NAKLI PROMPT TEMPLATE
# ============================================================
# This is also a Runnable.
#
# Input:
#     {'length': 'long', 'topic': 'AI'}
#
# Output:
#     "Write a long fact about AI"
# ============================================================

class NakliPromptTemplate(Runnable):

    def __init__(self, template, input_variables):

        self.template = template
        self.input_variables = input_variables

    # Common Runnable interface
    def invoke(self, input_dict):

        return self.template.format(**input_dict)

    # Old-style method.
    # Earlier we used format() directly.
    def format(self, input_dict):

        return self.template.format(**input_dict)


# ============================================================
# 4. GENERIC RUNNABLE CONNECTOR
# ============================================================
# This replaces our previous NakliLLMChain.
#
# The important difference:
#
# We don't need to create a special Chain for every
# combination of components.
#
# Any object having invoke() can be connected.
#
# Example:
#
#     Prompt → LLM → Parser
#
# The connector simply passes the output of one Runnable
# as the input of the next Runnable.
# ============================================================

class RunnableConnector(Runnable):

    def __init__(self, runnable_list):

        self.runnable_list = runnable_list

    def invoke(self, input_data):

        for runnable in self.runnable_list:

            # Every component follows the same interface.
            # So we don't care whether it is:
            #     Prompt
            #     LLM
            #     Parser
            #     Another Chain
            #
            # We simply call invoke().
            input_data = runnable.invoke(input_data)

        return input_data


# ============================================================
# 5. CREATE PROMPT + LLM
# ============================================================

template = NakliPromptTemplate(
    template='Write a {length} fact about {topic}',
    input_variables=['length', 'topic']
)

llm = NakliLLM()


# ============================================================
# 6. CONNECT TWO RUNNABLES
# ============================================================
#
# Flow:
#
#     Input Dictionary
#           ↓
#     PromptTemplate
#           ↓
#     Formatted Prompt
#           ↓
#     LLM
#           ↓
#     Response Dictionary
# ============================================================

chain = RunnableConnector([
    template,
    llm
])


output = chain.invoke({
    'length': 'long',
    'topic': 'something'
})

print(output['response'])


# ============================================================
# 7. OUTPUT PARSER
# ============================================================
# LLM returns:
#
#     {'response': 'AI stands for Artificial Intelligence'}
#
# But suppose we only want the actual string.
#
# So we create another Runnable.
#
# Input:
#     response dictionary
#
# Output:
#     response string
# ============================================================

class NakliStrOuputParser(Runnable):

    def __init__(self):
        pass

    def invoke(self, input_data):

        return input_data['response']


strParser = NakliStrOuputParser()


# ============================================================
# 8. CONNECT THREE RUNNABLES
# ============================================================
#
# Now our pipeline becomes:
#
#     Input
#       ↓
#     PromptTemplate
#       ↓
#     LLM
#       ↓
#     OutputParser
#       ↓
#     Final String
#
# All three components are different,
# but all three follow the same invoke() interface.
# ============================================================

chain = RunnableConnector([
    template,
    llm,
    strParser
])


output = chain.invoke({
    'length': 'long',
    'topic': 'something'
})

print(output)


# ============================================================
# 9. TWO CHAINS
# ============================================================
# Now comes the powerful part.
#
# Because RunnableConnector itself inherits from Runnable,
# a complete chain is ALSO a Runnable.
#
# Therefore:
#
#     Chain 1 → Chain 2
#
# is possible.
#
# Example:
#
#     Chain 1 = Generate something
#     Chain 2 = Explain that something
# ============================================================


# -------------------------
# Chain 1: Generate
# -------------------------

template1 = NakliPromptTemplate(
    template='Write a short fact about {topic}',
    input_variables=['topic']
)

chain1 = RunnableConnector([
    template1,
    llm,
    strParser
])


# -------------------------
# Chain 2: Explain
# -------------------------
# Chain 2 expects:
#
#     {'text': 'some generated text'}
#
# So we create a second prompt.

template2 = NakliPromptTemplate(
    template='Explain this: {text}',
    input_variables=['text']
)


# ============================================================
# 10. SMALL ADAPTER
# ============================================================
# Chain 1 returns a STRING.
#
# Chain 2 expects a DICTIONARY.
#
# So we need a small Runnable to convert:
#
#     string
#       ↓
#     {'text': string}
#
# This is just an example of adapting one Runnable's output
# to another Runnable's expected input.
# ============================================================

class TextToDict(Runnable):

    def invoke(self, input_data):

        return {
            'text': input_data
        }


adapter = TextToDict()


# ============================================================
# 11. CHAIN 2
# ============================================================

chain2 = RunnableConnector([
    template2,
    llm,
    strParser
])


# ============================================================
# 12. CHAIN OF CHAINS
# ============================================================
#
# Remember:
#
#     chain1 is a Runnable
#     adapter is a Runnable
#     chain2 is a Runnable
#
# Therefore our generic RunnableConnector can connect
# all of them.
#
# Final flow:
#
#     Input
#       ↓
#     Chain 1
#       ↓
#     Generated Text
#       ↓
#     Adapter
#       ↓
#     Dictionary
#       ↓
#     Chain 2
#       ↓
#     Final Answer
#
# This is the core idea of Runnable Composition.
# ============================================================

final_chain = RunnableConnector([
    chain1,
    adapter,
    chain2
])


output = final_chain.invoke({
    'topic': 'Artificial Intelligence'
})

print(output)


# ============================================================
# FINAL MENTAL MODEL
# ============================================================
#
# Before Runnables:
#
#     LLM.predict()
#     Prompt.format()
#     Parser.parse()
#          ↓
#     Different interfaces
#          ↓
#     Custom glue code
#          ↓
#     Specialized Chains
#
#
# With Runnables:
#
#     LLM.invoke()
#     Prompt.invoke()
#     Parser.invoke()
#          ↓
#     COMMON INTERFACE
#          ↓
#     Connect them directly
#          ↓
#     Runnable Workflow
#          ↓
#     Workflow itself is a Runnable
#          ↓
#     Connect workflows again
#
#
# The key idea:
#
#     COMPONENT → COMPONENT → COMPONENT
#                  ↓
#              Runnable
#
#     CHAIN → CHAIN → CHAIN
#              ↓
#          Bigger Runnable
#
# In short:
#
#     "If everything speaks invoke(),
#      everything can be composed."
# ============================================================