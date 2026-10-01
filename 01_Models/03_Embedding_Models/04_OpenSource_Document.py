from langchain_huggingface import HuggingFaceEmbeddings

embedding = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')

documents = [
  "Hello i am shaurav",
  "I am learning Artificial Learning",
  "What about you ??"
]

vector = embedding.embed_documents(documents)

print(str(vector))