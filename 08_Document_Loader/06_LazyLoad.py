from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader

loader = DirectoryLoader(
    path='./04_Directory_Data',
    glob='*.pdf',
    loader_cls=PyPDFLoader
)

# lazy_load() → documents are loaded progressively,
# instead of loading the complete directory at once.
docs = loader.lazy_load()

# Each document is processed one by one
for doc in docs:
    print(doc.metadata)


# --------------------------------------------------
# ADVANTAGES OVER .load()
#
# 1. LOWER MEMORY USAGE
#    → .load() keeps all loaded Documents in memory.
#    → lazy_load() processes them progressively.
#
# 2. BETTER FOR LARGE DIRECTORIES
#    → Useful when there are many PDFs or thousands of pages.
#
# 3. PROCESSING CAN START EARLIER
#    → You don't have to wait for the entire directory
#      to finish loading before processing documents.
#
# 4. BETTER RESOURCE CONTROL
#    → You can process a document and move to the next one
#      instead of keeping the whole collection in memory.
#
# IMPORTANT:
# lazy_load() is not necessarily faster at reading each PDF.
# Its main benefit is MEMORY EFFICIENCY and PROGRESSIVE PROCESSING.
#
# .load()      → Load everything → Process
# lazy_load()  → Load → Process → Load → Process → ...
# --------------------------------------------------