# LangChain — Important Document Loaders

> Note: These notes cover only the important loaders not already discussed.
> Already covered: TextLoader, PyPDFLoader, DirectoryLoader, CSVLoader, WebBaseLoader, load(), lazy_load().

---

# 1. YouTube Transcript Loader

## What does it do?

A YouTube video contains audio/video, but for RAG we mainly need its **text content**.

A YouTube Transcript Loader:
- takes a YouTube video
- gets its available transcript/captions
- converts that text into LangChain `Document` objects

### Flow

YouTube Video → Transcript → Document → Text Splitter → Embeddings → Vector Store

So, it does **not understand the video visually**. It mainly works with the transcript.

## Example

The exact import/package can vary with the current LangChain integration, so verify the current official integration docs before using the import.

Conceptually:

```python
# Load the transcript of a YouTube video
loader = YouTubeTranscriptLoader(video_url)

# Convert transcript into LangChain Documents
docs = loader.load()

print(docs[0].page_content)
print(docs[0].metadata)
```

## Why is it useful?

Very useful when you want to build:
- YouTube lecture summarizers
- Video Q&A systems
- YouTube-based RAG
- Educational knowledge bases

### Example

Suppose you have a 2-hour ML lecture.

Instead of watching the whole video every time:

User: "Explain vanishing gradient from this lecture."

RAG can retrieve the relevant transcript chunks and give an answer.

## Limitations

- Transcript/captions may not be available.
- Auto-generated captions can contain mistakes.
- Visual information such as diagrams, slides, and demonstrations is not captured.
- Quality depends on the transcript language and accuracy.

---

# 2. GitHub / Repository Loader

Used when your source is a **code repository**.

It can collect files from a repository and turn them into Documents.

### Useful for

- Codebase Q&A
- Documentation search
- Repository RAG
- Understanding large projects

Example use:

```text
GitHub Repository
       ↓
Repository Loader
       ↓
Documents
       ↓
Text Splitter
       ↓
Embeddings + Vector Store
```

---

# 3. Notion / Google Drive Loaders

These are useful when your knowledge is stored in productivity tools instead of local files.

### Notion

Useful for:
- company documentation
- study notes
- project documentation
- internal knowledge bases

### Google Drive

Useful when documents are stored centrally in Drive.

Typical flow:

```text
Notion / Google Drive
        ↓
Loader
        ↓
Documents
        ↓
RAG Pipeline
```

Main point: **the loader connects an external data source to the RAG pipeline.**

---

# 4. JSON / Markdown / DOCX Loaders

These are straightforward file-based loaders.

### JSON Loader

Useful when data is stored as JSON.

Common use:
- API responses
- configuration/structured data
- knowledge stored in JSON

### Markdown Loader

Useful for:
- README files
- documentation
- technical notes
- Markdown-based knowledge bases

### DOCX Loader

Useful for:
- Word documents
- reports
- assignments
- business documents

The important idea is the same:

```text
File → Loader → Document
```

---

# 5. Custom Document Loader

This is an important concept.

Sometimes your data source is **not supported by an existing loader**.

For example:

```text
Your Company API
Internal Database
Custom File Format
Private System
        ↓
   Custom Loader
        ↓
   LangChain Document
```

You create your own loader that fetches the data and converts it into LangChain `Document` objects.

## Basic Example

```python
from langchain_core.documents import Document


class MyLoader:

    def load(self):
        data = self.get_data()

        return [
            Document(
                page_content=data,
                metadata={
                    "source": "custom_api"
                }
            )
        ]

    def get_data(self):
        return "Data from my custom source"


loader = MyLoader()

docs = loader.load()

print(docs[0].page_content)
print(docs[0].metadata)
```

### What is happening?

`get_data()`  
→ gets data from your source

`Document(...)`  
→ converts that data into LangChain's standard format

`metadata`  
→ stores useful information such as source, ID, URL, category, etc.

The key requirement is:

**Your custom loader should ultimately return LangChain `Document` objects.**

## When should you create one?

Create a custom loader when:
- no suitable built-in loader exists
- you have an internal API
- you have a proprietary file format
- you need custom authentication
- you need special preprocessing before creating Documents

---

# Important Package Note

You may see imports like:

```python
from langchain_community.document_loaders import ...
```

LangChain's integration ecosystem has been changing, and some integrations have moved toward dedicated packages.

So:

- Don't assume every loader has a new one-to-one package.
- For new projects, check the **current official LangChain integration documentation** for the exact loader/import.
- Older tutorials may still use `langchain_community`.

For learning the concepts, the older examples are still useful.

