# Import Hugging Face classes for LangChain
from langchain_huggingface import ChatHuggingFace, HuggingFacePipeline

# Create a local Hugging Face pipeline
llm = HuggingFacePipeline.from_model_id(
    # Hugging Face model to download and run locally
    model_id="Qwen/Qwen3-0.6B",

    # Task for text generation
    task="text-generation",

    # Settings for how the model generates text
    pipeline_kwargs=dict(
        # Controls randomness in the generated response
        temperature=0.5,

        # Maximum number of tokens the model can generate
        max_new_tokens=200
    )
)

# Wrap the HuggingFace pipeline as a LangChain chat model
chat_model = ChatHuggingFace(llm=llm)

# Send a question to the model
response = chat_model.invoke("What is the capital of India?")

# Print only the text/content of the response
print(response.content)