from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from dotenv import load_dotenv
import streamlit as st
from langchain_core.prompts import PromptTemplate

load_dotenv()

# Connect to the Hugging Face model
llm = HuggingFaceEndpoint(
    model="Qwen/Qwen3-8B",
    task="conversational",
    provider="featherless-ai"
)

# Convert the endpoint into a chat model
model = ChatHuggingFace(llm=llm)

st.header("Research Tool")

# User selects which paper to explain
paper = st.selectbox(
    "Select Research Paper Name",
    [
        "Select...",
        "Attention Is All You Need",
        "BERT: Pre-training of Deep Bidirectional Transformers",
        "GPT-3: Language Models are Few-Shot Learners",
        "Diffusion Models Beat GANs on Image Synthesis"
    ]
)

# User selects explanation style
style = st.selectbox(
    "Select Explanation Style",
    [
        "Beginner-Friendly",
        "Technical",
        "Code-Oriented",
        "Mathematical"
    ]
)

# User selects desired answer length
length = st.selectbox(
    "Select Explanation Length",
    [
        "Short (1-2 paragraphs)",
        "Medium (3-5 paragraphs)",
        "Long (detailed explanation)"
    ]
)

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

    # These are the variables that must be supplied to the template
    input_variables=["paper", "style", "length"],

    # Checks that all declared variables exist in the template
    validate_template=True
)

# Fill the template with the user's selections
prompt = template.invoke({
    "paper": paper,
    "style": style,
    "length": length
})

# Run the model when the button is clicked
if st.button("Summarize"):

    # Send the prepared prompt to the model
    result = model.invoke(prompt)

    # Display the AI's text response
    st.write(result.content)