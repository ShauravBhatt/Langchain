# Length-Based Text Splitting

## 1. What is Length-Based Splitting?

Length-based splitting means:

> **Breaking a large text into smaller chunks based on their length.**

The main question is:

> **"How much text should each chunk contain?"**

For example, if we set:

```python
chunk_size = 100
```

the splitter tries to create chunks of around **100 characters**.

```text
Large Text
    ↓
Text Splitter
    ↓
Chunk 1 → 100 characters
Chunk 2 → 100 characters
Chunk 3 → 100 characters
...
```

It is one of the **simplest and fastest** ways to split text.

---

# 2. Advantages

### 1. Simple

It is easy to understand and implement.

### 2. Predictable Size

We can control how large our chunks should be.

### 3. Useful for Large Documents

Large documents can be divided into smaller pieces that models can process more easily.

### 4. Fast

The splitter does not need to deeply understand the meaning of the text, so the process is relatively fast.

---

# 3. Disadvantages

### 1. It Can Break Sentences

The splitter mainly cares about **length**, not meaning.

For example:

```text
Chunk 1:
"Machine learning is a method of"

Chunk 2:
"teaching computers to learn from data."
```

The sentence was split in the middle.

### 2. It Can Break Context

Information belonging to the same idea may end up in different chunks.

### 3. Not Always Ideal for RAG

If important information is split badly, retrieving the correct information can become more difficult.

---

# 4. Basic Code

Using LangChain:

```python
from langchain_text_splitters import CharacterTextSplitter

text = """
Machine learning is a branch of artificial intelligence.
It allows computers to learn from data.
Deep learning uses neural networks.
"""

splitter = CharacterTextSplitter(
    chunk_size=100,
    chunk_overlap=0,
    separator=""
)

chunks = splitter.split_text(text)

for chunk in chunks:
    print(chunk)
```

The splitter takes the `text` and creates smaller `chunks`.

---

# 5. Important Parameters

There are three important parameters here:

```python
chunk_size = 100
chunk_overlap = 0
separator = ""
```

---

## 5.1 `chunk_size`

```python
chunk_size=100
```

It controls the **size of each chunk**.

In this example, the splitter tries to keep each chunk around **100 characters**.

For example:

```text
Original:
ABCDEFGHIJKLMNOPQRSTUVWXYZ

chunk_size = 10

Chunk 1 → ABCDEFGHIJ
Chunk 2 → KLMNOPQRST
Chunk 3 → UVWXYZ
```

So:

> **`chunk_size` = How large should each chunk be?**

---

## 5.2 `chunk_overlap`

```python
chunk_overlap=0
```

Overlap means **repeating some content from the previous chunk in the next chunk**.

Suppose:

```python
chunk_size = 10
chunk_overlap = 3
```

Then conceptually:

```text
Chunk 1 → ABCDEFGHIJ
Chunk 2 → HIJKLMNO
          ↑↑↑
        repeated
```

The last 3 characters of the previous chunk are included in the next chunk.

Why?

Because it helps **preserve context between chunks**.

If:

```python
chunk_overlap = 0
```

there is no repeated content.

So:

> **`chunk_overlap` = How much content should be shared between consecutive chunks?**

---

## 5.3 `separator`

```python
separator=""
```

A separator tells the splitter **where it can try to split the text**.

Common separators are:

```python
separator = ""
```

Split directly without using a specific separator.

```python
separator = " "
```

Use spaces as boundaries.

```python
separator = "\n"
```

Use new lines as boundaries.

For example:

```text
Hello world
This is AI
I am learning RAG
```

With:

```python
separator = "\n"
```

the splitter can use the new lines as splitting points.

So:

> **`separator` = Which character or boundary should be used for splitting?**
