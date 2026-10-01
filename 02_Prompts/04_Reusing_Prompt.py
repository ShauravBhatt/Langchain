from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from dotenv import load_dotenv
from langchain_core.load import loads
import streamlit as st

load_dotenv()


# Connect to the Hugging Face model
llm = HuggingFaceEndpoint(
    model="Qwen/Qwen3-8B",
    task="conversational",
    provider="featherless-ai"
)

# Convert endpoint into a chat model
model = ChatHuggingFace(llm=llm)


# Streamlit UI
st.header("📚 Research Paper Summarizer")

paper = st.selectbox(
    "Select Research Paper",
    [
        "Attention Is All You Need",
        "BERT: Pre-training of Deep Bidirectional Transformers",
        "GPT-3: Language Models are Few-Shot Learners",
        "Diffusion Models Beat GANs on Image Synthesis",
        "ResNet: Deep Residual Learning for Image Recognition"
    ]
)

style = st.selectbox(
    "Select Explanation Style",
    [
        "Beginner-Friendly",
        "Technical",
        "Research-Oriented",
        "Mathematical"
    ]
)

length = st.selectbox(
    "Select Summary Length",
    [
        "Short (1-2 paragraphs)",
        "Medium (3-5 paragraphs)",
        "Detailed Summary"
    ]
)


# Read the saved JSON file
with open("03_templates.json", "r") as f:

    # Convert JSON back into the original LangChain object
    template = loads(f.read())


if st.button("🔍 Summarize Paper"):

    # Fill the template with user's selections
    prompt = template.invoke({
        "paper": paper,
        "style": style,
        "length": length
    })

    # Send the completed prompt to the model
    result = model.invoke(prompt)

    # Display the model's response
    st.subheader("📄 Summary")
    st.write(result.content)