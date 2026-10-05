import random

# ============================================================
# 1. NAKLI LLM
# ============================================================
# In real LangChain:
#     LLM / ChatModel
#
# Here we are creating our own fake LLM just for learning.
# Its job is simple:
#
#     prompt → response
#
# This is our first "component".
# ============================================================

class NakliLLM:

    def __init__(self):
        print('LLM Created')

    # --------------------------------------------------------
    # This is the interface of our fake LLM.
    #
    # We give it a prompt,
    # it processes the prompt,
    # and gives us an output.
    #
    # In the old LangChain approach, LLMs had methods such
    # as predict().
    # --------------------------------------------------------
    def predict(self, prompt):

        response_list = [
            'Delhi is the capital of india',
            'Agentic AI is the next booming stuff',
            'AI stands for Artificial Intelligence'
        ]

        # Just randomly selecting a response
        # instead of actually calling an LLM.
        return {
            'response': random.choice(response_list)
        }


# Creating our LLM component
llm = NakliLLM()


# Manually calling the LLM
result = llm.predict("Tell me a fact")

print("Nakli LLM's Response: ", result['response'])


# ============================================================
# 2. NAKLI PROMPT TEMPLATE
# ============================================================
# Now we create another component.
#
# Its job is:
#
#     input variables
#           ↓
#     formatted prompt
#
# Again, this represents the kind of component LangChain
# provided.
# ============================================================

class NakliPromptTemplate:

    def __init__(self, template, input_variables):

        # Example:
        # "Write a {length} fact about {topic}"

        self.template = template

        # Variables required by this template
        # ['length', 'topic']
        self.input_variables = input_variables


    # --------------------------------------------------------
    # Old-style PromptTemplate interface:
    #
    #     format()
    #
    # We give it values for the variables and it generates
    # the final prompt.
    # --------------------------------------------------------
    def format(self, input_dict):

        return self.template.format(**input_dict)


# Creating our Prompt Template component
template = NakliPromptTemplate(
    template='Write a {length} fact about {topic}',
    input_variables=['length', 'topic']
)


# ------------------------------------------------------------
# We manually call format()
#
# Input:
#     length = short
#     topic = something
#
# Output:
#     "Write a short fact about something"
# ------------------------------------------------------------

prompt = template.format({
    'length': 'short',
    'topic': 'something'
})

print('Nakli Prompt : ', prompt)


# ------------------------------------------------------------
# And then manually pass that generated prompt to the LLM.
# ------------------------------------------------------------

result1 = llm.predict(prompt)

print(result1['response'])


# ============================================================
# 3. THE PROBLEM WITH THIS APPROACH
# ============================================================
#
# Look carefully at what WE are doing manually:
#
#     PromptTemplate
#            ↓
#        format()
#            ↓
#       final prompt
#            ↓
#        LLM.predict()
#            ↓
#        response
#
# We are writing the glue code ourselves.
#
# This is exactly the problem discussed in the lecture.
#
# The components are useful individually,
# BUT they don't automatically know how to work together.
#
# PromptTemplate has:
#       format()
#
# LLM has:
#       predict()
#
# Different interfaces!
#
# Therefore, we need some custom code to connect them.
# ============================================================



# ============================================================
# 4. NAKLI LLM CHAIN
# ============================================================
#
# Now we solve that problem by creating a Chain.
#
# The Chain's job is to connect:
#
#       PromptTemplate
#              +
#             LLM
#
# into one reusable workflow.
# ============================================================

class NakliLLMChain:

    def __init__(self, llm, prompt):

        # Store the LLM component
        self.llm = llm

        # Store the PromptTemplate component
        self.prompt = prompt


    # --------------------------------------------------------
    # Instead of manually doing:
    #
    #     prompt.format()
    #     llm.predict()
    #
    # the Chain does BOTH internally.
    #
    # So the developer only needs to call:
    #
    #     chain.run(input_dict)
    # --------------------------------------------------------

    def run(self, input_dict):

        # STEP 1:
        # Generate the final prompt using PromptTemplate
        final_prompt = self.prompt.format(input_dict)


        # STEP 2:
        # Send that generated prompt to the LLM
        result = self.llm.predict(final_prompt)


        # STEP 3:
        # Extract the actual response
        return result['response']


# ============================================================
# 5. CREATE THE COMPONENTS
# ============================================================

template1 = NakliPromptTemplate(
    template='Write a {length} fact on {topic}',
    input_variables=['length', 'topic']
)


llm1 = NakliLLM()


# ============================================================
# 6. CONNECT THE COMPONENTS USING A CHAIN
# ============================================================

chain = NakliLLMChain(
    llm1,
    template1
)


# ============================================================
# 7. RUN THE COMPLETE WORKFLOW
# ============================================================
#
# We only provide the INPUT.
#
# Behind the scenes:
#
#     input_dict
#         ↓
#     PromptTemplate.format()
#         ↓
#     final prompt
#         ↓
#     LLM.predict()
#         ↓
#     response
#
# We don't manually call format() and predict().
# The Chain handles that glue code for us.
# ============================================================

response = chain.run({
    'length': 'short',
    'topic': 'something'
})


print(response)