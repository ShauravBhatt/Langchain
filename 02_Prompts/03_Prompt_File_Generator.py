from langchain_core.prompts import PromptTemplate
from langchain_core.load import dumps

# Create a reusable prompt template
template = PromptTemplate(
    template="""
    You are a research paper explanation assistant.

    Explain the following research paper according to the user's selected preferences.

    Research Paper:
    {paper}

    Explanation Style:
    {style}

    Explanation Length:
    {length}

    Instructions:
    - Explain the main idea clearly.
    - Cover the important concepts and contributions.
    - Use examples where helpful.
    - Keep the explanation appropriate to the selected style and length.
    - Do not add unnecessary information.

    Now provide the explanation.
    """,

    # Variables that will be filled later
    input_variables=["paper", "style", "length"],

    # Validate that template variables are correctly defined
    validate_template=True
)

# Open/create a JSON file
with open("03_templates.json", "w") as f:

    # Convert the LangChain template object into JSON
    f.write(dumps(template))