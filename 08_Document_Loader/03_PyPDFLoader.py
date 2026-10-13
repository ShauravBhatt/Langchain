from langchain_community.document_loaders import PyPDFLoader

# NEW:
# PyPDFLoader → loads a PDF and usually creates
# one Document object for each page.
loader = PyPDFLoader("./03_file.pdf")

docs = loader.load()

# Number of Document objects = usually number of PDF pages
print(len(docs))

# First page's Document
print(docs[0])


# --------------------------------------------------
# DIFFERENT PDF LOADERS / USE CASES
#
# 1. PyPDFLoader
#    → General-purpose PDF loading
#    → Usually one Document per page
#    → Good for normal text-based PDFs
#
# 2. PyMuPDFLoader
#    → Uses PyMuPDF
#    → Generally faster and provides richer PDF metadata
#    → Useful when processing many PDFs
#
# 3. PDFPlumberLoader
#    → Good when PDF contains tables
#    → Useful for extracting structured/tabular content
#
# 4. UnstructuredPDFLoader
#    → Extracts different document elements
#      such as text, tables, and titles
#    → Useful for complex layouts
#
# 5. Math / scanned / image-heavy PDFs
#    → Normal PDF loaders may not extract the actual text
#    → OCR-based processing may be required
#
# IMPORTANT:
# Choose the loader based on the PDF type,
# not simply because it is a PDF.
#
# LIMITATION:
# A normal PDF loader cannot magically understand
# text that exists only as an image.
#
# KEY TAKEAWAY:
# PyPDFLoader = simple, general-purpose PDF → Documents.
# For tables, complex layouts, or scanned PDFs,
# a more specialized approach may be better.
# --------------------------------------------------