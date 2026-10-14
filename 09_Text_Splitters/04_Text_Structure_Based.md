# Text-Structure-Based Splitting

## 1. What is it?

**Text-structure-based splitting** means splitting text according to its natural structure instead of blindly cutting it after a fixed number of characters.

For example, text has a natural hierarchy:

```text
Paragraph
   ↓
Sentence
   ↓
Words
   ↓
Characters
```

The most commonly used splitter for this in LangChain is:

> **RecursiveCharacterTextSplitter**

It tries to keep the text meaningful while still keeping each chunk within the required size.

---

# 2. Recursive Character Text Splitter

The important word here is **Recursive**.

It means:

> **It tries a larger separator first. If the resulting piece is still too large, it moves to a smaller separator and splits again.**

Its usual hierarchy is:

```text
Paragraph
    ↓
Sentence
    ↓
Word
    ↓
Character
```

Conceptually, it uses separators like:

```text
"\n\n"  → paragraph
"\n"    → line
" "     → word
""      → character
```

So it does **not immediately cut characters**.

---

# 3. Example

Let's take four small sentences:

```text
S1: I love Python.
S2: Python is easy to learn.
S3: I am learning machine learning.
S4: Machine learning is used in AI.
```

Assume our text is:

```text
I love Python. Python is easy to learn.

I am learning machine learning. Machine learning is used in AI.
```

Notice that there is a blank line between the two groups.

So structurally we have:

```text
Paragraph 1
→ S1 + S2

Paragraph 2
→ S3 + S4
```

---

# 4. Suppose `chunk_size = 100`

The first separator is:

```text
"\n\n"
```

It tries to split by paragraphs.

Our paragraphs are already smaller than 100 characters.

So we get:

```text
Chunk 1
→ I love Python.
  Python is easy to learn.

Chunk 2
→ I am learning machine learning.
  Machine learning is used in AI.
```

It stops here because both chunks fit inside `100`.

---

# 5. Now `chunk_size = 50`

Now the paragraphs may be too large.

So the splitter goes one level deeper.

```text
Paragraph
   ↓
Sentences
```

It splits:

```text
Paragraph 1
→ S1
→ S2

Paragraph 2
→ S3
→ S4
```

Now it tries to combine nearby sentences while keeping the chunk within 50 characters.

Possible result:

```text
Chunk 1
→ I love Python.

Chunk 2
→ Python is easy to learn.

Chunk 3
→ I am learning machine learning.

Chunk 4
→ Machine learning is used in AI.
```

The exact grouping depends on the actual text length and splitter settings.

---

# 6. Now `chunk_size = 25`

Suppose even a sentence is too large.

For example:

```text
"I am learning machine learning."
```

is larger than the allowed size.

The splitter goes further down:

```text
Paragraph
    ↓
Sentence
    ↓
Words
```

So it may break the sentence around words:

```text
Chunk 1 → I am learning
Chunk 2 → machine learning.
```

If a piece is still too large, it can finally go to:

```text
Characters
```

So the hierarchy is:

```text
"\n\n"
   ↓
"\n"
   ↓
" "
   ↓
""
```

**Large separator → smaller separator → character level**

This is why it is called **Recursive**.

---

# 7. Why is it Better?

Imagine we simply use a character splitter:

```text
I love Python. Python is e
asy to learn. I am learnin
g machine learning.
```

This can break words and sentences.

Recursive splitting tries to avoid this.

It prefers:

```text
I love Python.
Python is easy to learn.
```

rather than:

```text
I love Python. Python is e
asy to learn.
```

So it tries to create chunks that are both:

**small enough + meaningful**

---

# 8. Advantages

### 1. Preserves Meaning

It tries to keep sentences and paragraphs together.

### 2. Better for RAG

Meaningful chunks generally give better results for:

- Embeddings
- Semantic search
- Retrieval
- Question answering

### 3. Flexible

You can control:

```text
chunk_size
chunk_overlap
separators
```

### 4. Handles Different Text Sizes

If a paragraph is small → keep it.

If it is too large → split into sentences.

If a sentence is too large → split into words.

So it adapts to the text.

---

# 9. Disadvantages

### 1. Slightly More Complex

It is more complicated than simply splitting every fixed number of characters.

### 2. Still Not Truly Semantic

It understands **structure**, not actual meaning.

For example, it knows where sentences end, but it does not truly understand whether two sentences discuss the same topic.

### 3. Chunk Size Is Not Always Exact

The final chunks may not be exactly the specified size because the splitter tries to respect natural boundaries.

---

# 10. Why is it Used So Much?

Because it gives a very useful balance:

```text
Fixed Character Splitting
        ↓
Simple but can destroy meaning

Recursive Splitting
        ↓
Simple + respects text structure
        ↓
Good chunks for RAG
```

That's why **RecursiveCharacterTextSplitter is one of the most commonly used general-purpose text splitters in LangChain.**

---

# 11. Small Code

```python
from langchain_text_splitters import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(
    chunk_size=100,
    chunk_overlap=20
)

chunks = splitter.split_text(text)

for chunk in chunks:
    print(chunk)
```

You can also explicitly provide the hierarchy:

```python
splitter = RecursiveCharacterTextSplitter(
    chunk_size=100,
    chunk_overlap=20,
    separators=["\n\n", "\n", " ", ""]
)
```

Here:

```text
\n\n → paragraph
\n   → line
" "  → word
""   → character
```

The splitter tries them **in this order**, moving to the next one only when necessary.