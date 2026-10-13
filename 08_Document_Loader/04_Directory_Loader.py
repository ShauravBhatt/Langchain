from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader, TextLoader

# Load all PDF files from the directory
pdf_loader = DirectoryLoader(
    path='./04_Directory_Data',
    glob='*.pdf',
    loader_cls=PyPDFLoader
)

# Load all TXT files from the same directory
text_loader = DirectoryLoader(
    path='./04_Directory_Data',
    glob='*.txt',
    loader_cls=TextLoader
)

# Eagerly loads ALL matching PDF files
pdf_docs = pdf_loader.load()

# Eagerly loads ALL matching TXT files
text_docs = text_loader.load()

# Combine both document lists
docs = pdf_docs + text_docs

print(len(docs))
print(docs[5])


# --------------------------------------------------
# PROBLEMS WITH .load() ON LARGE DIRECTORIES
#
# 1. HIGH MEMORY USAGE
#    → .load() loads everything into memory at once.
#    → Large PDFs + many files = high RAM usage.
#
# 2. SLOW INITIAL LOADING
#    → It waits for ALL files to finish loading
#      before returning the result.
#
# 3. PDF PAGE EXPANSION
#    → A large PDF can create many Document objects
#      because pages are usually separate Documents.
#
# 4. NOT IDEAL FOR LARGE DATASETS
#    → Thousands of files/pages can make eager loading
#      expensive and slow.
#
# BETTER APPROACH:
#    Use lazy_load() when you want to process documents
#    progressively instead of keeping everything in memory.
#
# Example:
#
# for doc in pdf_loader.lazy_load():
#     process(doc)
#
# KEY TAKEAWAY:
# .load() → simple and convenient for small datasets.
# lazy_load() → better suited for large document collections.
# --------------------------------------------------