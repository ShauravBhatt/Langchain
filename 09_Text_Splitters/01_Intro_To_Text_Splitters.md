# Text Splitters

## 1. What is Text Splitting?

Suppose we have a very large PDF with **1,000 pages**.

Processing the complete PDF at once can be difficult for an LLM or other AI models.

So, we break the large document into smaller pieces called **chunks**.

```text
Large Document
      ↓
 Text Splitter
      ↓
 ┌────────┐
 │ Chunk 1│
 ├────────┤
 │ Chunk 2│
 ├────────┤
 │ Chunk 3│
 ├────────┤
 │ Chunk 4│
 └────────┘
```

This process is called **Text Splitting**.

The tool/code that performs this operation is called a **Text Splitter**.

### Definition

> **Text Splitting is the process of breaking a large text into smaller, manageable pieces called chunks so that AI models can process the information effectively.**

---

# 2. Why is Text Splitting Important?

There are **three main reasons**.

## 2.1 Overcoming Model Limitations

Every LLM and embedding model has a limit on how much text it can process as input.

This is related to its **context length**.

For example:

```text
Model limit = 50,000 tokens
Document   = 100,000 tokens
```

The complete document cannot be given to the model at once.

So we split it:

```text
100,000 tokens
      ↓
Chunk 1 → 20,000
Chunk 2 → 20,000
Chunk 3 → 20,000
Chunk 4 → 20,000
Chunk 5 → 20,000
```

Now each chunk can be processed separately.

**Note:** Tokens and words are not exactly the same. The numbers above are only for understanding the concept.

---

# 3. Better Results in Downstream Tasks

**Downstream tasks** are the tasks we perform after processing the text.

In LLM/RAG applications, common downstream tasks include:

- Embedding
- Semantic Search
- Summarization
- Question Answering
- Retrieval

Text splitting can improve the quality of these tasks.

---

## 3.1 Embedding

An embedding model converts text into a **numerical vector** that represents its meaning.

Suppose a document contains:

```text
Paragraph 1 → CSK
Paragraph 2 → Mumbai Indians
Paragraph 3 → RCB
```

If we create one embedding for the complete document, one vector has to represent all these different topics.

Instead:

```text
CSK information       → Vector 1
Mumbai Indians        → Vector 2
RCB information       → Vector 3
```

Each vector represents a smaller and more focused piece of information.

So, splitting can help embeddings capture the **semantic meaning of individual topics more effectively**.

---

## 3.2 Semantic Search

Semantic search finds information based on **meaning**, not just exact keyword matching.

Suppose we have:

```text
Chunk 1 → RCB information
Chunk 2 → Mumbai Indians information
Chunk 3 → CSK information
```

User asks:

> "Which IPL team does Virat Kohli play for?"

The query is converted into an embedding and compared with the chunk embeddings.

```text
Query
  ↓
Query Vector
  ↓
Compare with chunk vectors
  ↓
Most similar chunk → RCB
```

Because the document was split into meaningful chunks, the system can retrieve **more relevant information**.

---

## 3.3 Summarization

Very large documents can also be difficult for an LLM to summarize effectively.

The model may:

- Lose important information
- Drift away from the topic
- Produce inaccurate information
- Sometimes hallucinate

Instead, we can split the document into smaller chunks and process them separately.

```text
Large Document
      ↓
    Chunks
      ↓
Individual Summaries
      ↓
Final Summary
```

This allows the model to focus on smaller amounts of information at a time.

---

# 4. Better Computational Resource Usage

Text splitting can also make processing more efficient.

Processing one huge text can require more:

- Memory
- Computation
- Processing resources

With smaller chunks, processing becomes more manageable.

Chunks can also sometimes be processed **in parallel**.

```text
Large Document
      ↓
 Small Chunks
   ↓   ↓   ↓
 Task Task Task
```

So text splitting can help with:

- Memory efficiency
- Computational efficiency
- Parallel processing

---

# 5. Text Splitting in a RAG Application

A typical RAG pipeline looks like:

```text
Documents
    ↓
Document Loader
    ↓
Text Splitter
    ↓
Chunks
    ↓
Embeddings
    ↓
Vector Database
```

Later:

```text
User Query
    ↓
Query Embedding
    ↓
Semantic Search
    ↓
Relevant Chunks
    ↓
LLM
    ↓
Answer
```

Therefore, **text splitting is an important step in RAG** because the chunks created here are later used for embedding, retrieval, and answering questions.

---

# 6. Four Types of Text Splitting

The main question in text splitting is:

> **"Where should we split the text?"**

There are four common approaches.

### 1. Length-Based Splitting

Split according to the **size of the text**.

Example:

```text
Every 500 characters
Every 1,000 characters
Every 500 tokens
```

---

### 2. Text-Structure-Based Splitting

Split according to the **structure of the text**.

For example:

```text
Paragraph
   ↓
Sentence
   ↓
Words
```

The splitter tries to use these natural text boundaries.

---

### 3. Document-Structure-Based Splitting

Split according to the **structure of the document**.

For example:

```text
Book
 ↓
Chapter
 ↓
Section
 ↓
Subsection
```

This is useful when the document has a clear hierarchy.

---

### 4. Semantic-Based Splitting

Split according to the **meaning of the text**.

The goal is to keep sentences discussing the **same topic or idea** together and split when the topic changes.

**Example:**

```text
Rahul is a software engineer.
He works with Python and Django.
He builds web applications.

      ↓ Topic changes

He also enjoys playing cricket.
He plays cricket every weekend.
```

So:

```text
Chunk 1 → Software / Work
Chunk 2 → Cricket / Hobby
```

**Key idea:** Same meaning → keep together. New meaning → split.