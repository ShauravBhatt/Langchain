from langchain_experimental.text_splitter import SemanticChunker
from langchain_huggingface import HuggingFaceEmbeddings

text = """
Farmers are facing problems because of low rainfall.
Modern irrigation techniques can increase crop production.
Virat Kohli is one of the most famous players in the IPL.
He has played for Royal Challengers Bengaluru for many years.
Terrorism is a serious threat to national security.
Governments use different strategies to prevent terrorism.
"""

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2",
    model_kwargs={"device": "cpu"},
    encode_kwargs={"normalize_embeddings": True}
)

splitter = SemanticChunker(
    embeddings,
    breakpoint_threshold_type="percentile",
    breakpoint_threshold_amount=90
)

chunks = splitter.split_text(text)

for i, chunk in enumerate(chunks, 1):
    print(f"\n--- Chunk {i} ---")
    print(chunk)