# RAG and Document Loaders

## 1. What is RAG?

**RAG (Retrieval-Augmented Generation)** is a technique where an LLM first retrieves relevant information from external data and then uses that information to generate an answer.

### Why do we need RAG?

An LLM has limitations:

- It may not know private or custom data.
- Its knowledge may not contain the latest information.
- It can sometimes generate incorrect information.

RAG helps by giving the model relevant information from an external knowledge source before generating the answer.

### Basic RAG Flow

**User Query → Retrieve Relevant Data → Give Data to LLM → Generate Answer**

---

# 2. Four Main Components of RAG

A basic RAG system has four major components:

## 1. Document Loader

Loads data from different sources such as:

- PDF
- Text files
- Word documents
- Websites
- CSV files
- Databases

**Purpose:** Convert external data into a form that the RAG pipeline can work with.

---

## 2. Text Splitter

Large documents are divided into smaller pieces called **chunks**.

**Purpose:**

- Make documents easier to process.
- Retrieve only the relevant portion.
- Fit useful information into the LLM context window.

**Flow:**

`Document → Smaller Chunks`

---

## 3. Embeddings + Vector Store

Each text chunk is converted into a numerical representation called an **embedding**.

The embeddings are stored in a **vector store/vector database**.

**Purpose:** Find chunks that are semantically similar to the user's query.

**Flow:**

`Text Chunk → Embedding → Vector Store`

---

## 4. Retriever + LLM

The **retriever** searches the vector store and returns the most relevant chunks.

The retrieved chunks are then given to the **LLM**, which uses them as context to generate the final answer.

**Flow:**

`Query → Retriever → Relevant Chunks → LLM → Answer`

---

# 3. Complete RAG Pipeline

The complete process can be understood in two stages.

### Indexing Stage

`Documents → Document Loader → Text Splitter → Embeddings → Vector Store`

This prepares the knowledge base.

### Query Stage

`User Query → Retriever → Relevant Chunks → LLM → Final Answer`

This retrieves the required information and generates the response.

---

# 4. Document Loader

A **Document Loader** is a component that reads data from a specific source and converts it into a standard document format that the RAG pipeline can process.

### Simple Idea

Different sources have different formats:

- PDF has pages.
- CSV has rows and columns.
- Website has HTML.
- Word files have paragraphs.
- Text files contain plain text.

The document loader handles the source-specific reading and gives the pipeline a common representation.

### Working

`Data Source → Loader → Document Objects`

A document object generally contains:

- **page_content** → actual text
- **metadata** → information about the source

Example metadata can include:

- file name
- page number
- source
- document type

---

# 5. Types of Document Loaders

Document loaders are generally selected according to the type of data source.

## 1. PDF Loader

Used to load text from PDF documents.

**Example use:** Research papers, books, reports, manuals.

Conceptually:

`PDF → PDF Loader → Documents`

---

## 2. Text File Loader

Used for plain `.txt` files.

`TXT File → Text Loader → Documents`

---

## 3. CSV Loader

Used to load structured data from CSV files.

`CSV → CSV Loader → Documents`

Each row can be represented as document content with associated metadata.

---

## 4. Word Document Loader

Used to load content from Word documents such as `.docx`.

`DOCX → Word Loader → Documents`

---

## 5. Web/HTML Loader

Used to extract content from web pages.

`Web Page → Web Loader → Documents`

Useful when building RAG systems over website content.

---

## 6. Database Loader

Used to retrieve data from databases.

`Database → Database Loader → Documents`

Useful when the knowledge source is stored in structured database records.

---

# 6. Basic Conceptual Code

The exact loader class depends on the source.

```python
loader = SomeDocumentLoader("file_path")

documents = loader.load()
```

The important idea is:

```text
Source
   ↓
Document Loader
   ↓
Document Objects
   ↓
Text Splitter
   ↓
Embeddings
   ↓
Vector Store
```

You do not need to memorize loader classes right now. First understand **which loader is suitable for which data source and what output a loader produces**.

---

# 7. Key Takeaway

**Document Loader = Bridge between the raw data source and the RAG pipeline.**

It does not perform retrieval or generate answers.

Its main job is:

**Read → Extract → Standardize → Return Documents**
