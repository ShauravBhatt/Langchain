# Document-Based Text Splitting

## 1. What is Document-Based Splitting?

**Document-based splitting** means splitting a document according to its **own structure and format**.

Different types of documents have different structures.

For example:

```text
Python Code
→ Class
→ Function
→ If/Else block
→ Statements
```

```text
Markdown
→ Heading
→ Subheading
→ Paragraph
→ List
```

```text
HTML
→ HTML tags
→ Sections
→ Paragraphs
→ Elements
```

The splitter uses this structure to create more meaningful chunks.

---

## 2. Why is it Different from Text-Structure Splitting?

In normal text splitting, we usually work with general separators:

```text
Paragraph
   ↓
Sentence
   ↓
Word
   ↓
Character
```

But in **document-based splitting**, we know the **type of document** and use its specific structure.

For example, for Python:

```text
Class
 ↓
Methods
 ↓
Statements
```

So instead of randomly cutting Python code, we try to keep related code together.

---

# 3. Example: Python Code

Consider:

```python
class Student:

    def __init__(self, name, age, marks):
        self.name = name
        self.age = age
        self.marks = marks

    def display_details(self):
        print("Student Name:", self.name)
        print("Student Age:", self.age)
```

A normal character-based splitter might cut like this:

```text
Chunk 1:
class Student:
    def __init__(self, name, age, marks):
        self.name = self.name
        ...

Chunk 2:
self.marks = self.marks
    def display_details(self):
        ...
```

This can break the logical structure of the code.

A Python-aware splitter tries to respect structures such as:

```text
Class
  ↓
Method
  ↓
Statements
```

So related code stays together as much as possible.

---

# 4. Your Code

Your code uses:

```python
RecursiveCharacterTextSplitter.from_language(
    language=Language.PYTHON,
    chunk_size=300,
    chunk_overlap=0
)
```

The important part is:

```python
Language.PYTHON
```

This tells LangChain:

> **"This is Python code, so use Python-specific separators and structure."**

The splitter then recursively tries Python-aware boundaries while keeping the chunks around the requested size.

---

## Important Parameters

### `language`

```python
language=Language.PYTHON
```

Tells the splitter what type of document/code it is processing.

For example:

```python
Language.PYTHON
Language.JS
Language.JAVA
Language.CPP
```

This allows it to use appropriate separators for that language.

---

### `chunk_size`

```python
chunk_size=300
```

The target maximum size of each chunk.

So the splitter tries to create chunks around **300 characters** while respecting the code structure.

---

### `chunk_overlap`

```python
chunk_overlap=0
```

No content is repeated between consecutive chunks.

If we use:

```python
chunk_overlap=20
```

some content from the previous chunk would be repeated in the next chunk.

---

# 5. Code

```python
from langchain_text_splitters import (
    RecursiveCharacterTextSplitter,
    Language
)

splitter = RecursiveCharacterTextSplitter.from_language(
    language=Language.PYTHON,
    chunk_size=300,
    chunk_overlap=0
)

chunks = splitter.split_text(text)

for chunk in chunks:
    print("----- CHUNK -----")
    print(chunk)
```

The rest of your code is simply the **Python document/code that we want to split**.

---

# 6. Advantages

### 1. Preserves Document Structure

It tries to keep logically related parts together.

### 2. Better for Code

For programming languages, it can avoid breaking code at completely random places.

### 3. Better Context

A chunk containing a complete method or related code gives the LLM better context.

### 4. Useful for Code RAG

If you are building a system that searches through a large codebase, meaningful code chunks are much more useful than random character chunks.

---

# 7. Disadvantages

### 1. Language/Format Specific

You need to know what type of document you are dealing with.

### 2. Not Perfect

If a function itself is larger than the `chunk_size`, it may still need to be split further.

### 3. More Limited Than General Splitting

It works best when the document has a known and recognizable structure.

---

# 8. When Should We Use It?

Use document-based splitting when the document has a **clear structure that the splitter understands**.

Examples:

```text
Python / Java / C++ code
Markdown documents
HTML
LaTeX
```

For example:

> If you have a large GitHub repository and want to build a **Code RAG**, document/language-aware splitting is much better than blindly cutting every 500 characters.