# Semantic Meaning-Based Text Splitting

### 1. The Basic Idea

So far, we have seen:

1. **Length-Based Splitting** → split based on size.
2. **Structure-Based Splitting** → split based on paragraphs, sentences, words, etc.
3. **Document/Language-Based Splitting** → split according to the structure of a specific document or programming language.

But there is one important problem:

> Sometimes the **text structure does not match the meaning**.

For example:

```text
Farmers are facing problems because of low rainfall.
Modern irrigation techniques can help increase crop production.
Virat Kohli is one of the most famous players in the IPL.
He has played for Royal Challengers Bengaluru for many years.

Terrorism is a serious threat to national security.
Governments use different strategies to prevent terrorism.
```

Structurally, this may look like **two paragraphs**.

But semantically, there are actually **three topics**:

```text
Chunk 1 → Agriculture
Chunk 2 → IPL / Cricket
Chunk 3 → Terrorism
```

A structure-based splitter may keep the first two topics together because they are inside the same paragraph.

A **semantic splitter** tries to understand this difference in meaning.

---

# 2. What Does "Semantic" Mean?

**Semantic = meaning.**

Semantic Meaning-Based Text Splitting asks:

> "Are these two pieces of text talking about the same thing?"

If yes → keep them together.

If no → create a boundary.

So instead of asking:

```text
"Is this paragraph too large?"
```

we ask:

```text
"Did the topic/meaning change here?"
```

This is especially useful for **RAG**, because we want each chunk to represent a focused piece of information.

---

# 3. How Does It Actually Work?

The basic process is:

```text
Document
   ↓
Split into sentences
   ↓
Create embedding for every sentence
   ↓
Compare neighboring sentence embeddings
   ↓
Calculate similarity
   ↓
Detect sudden drop in similarity
   ↓
Create chunk boundary
```

Let's understand this properly.

---

## Step 1 — Split the document into sentences

Suppose we have:

```text
S1: Farmers are facing problems because of low rainfall.

S2: Modern irrigation can increase crop production.

S3: Virat Kohli is one of the famous IPL players.

S4: He has played for Royal Challengers Bengaluru.
```

First, we separate them:

```text
S1
S2
S3
S4
```

---

## Step 2 — Convert every sentence into an embedding

An **embedding model** converts text into a vector representing its meaning.

For example, conceptually:

```text
S1 → [0.21, 0.73, 0.14, ...]

S2 → [0.25, 0.69, 0.18, ...]

S3 → [0.91, 0.12, 0.67, ...]

S4 → [0.87, 0.15, 0.62, ...]
```

The actual vectors contain hundreds of dimensions. These numbers are just for understanding.

Because S1 and S2 are about agriculture, their vectors should be relatively close.

S3 and S4 are about IPL, so their vectors should also be close.

But S2 and S3 are about completely different topics.

---

# 4. Compare Consecutive Sentences

We compare:

```text
S1 ↔ S2
S2 ↔ S3
S3 ↔ S4
```

Usually we use **cosine similarity**.

Conceptually:

```text
High similarity
      ↓
Same/similar topic
      ↓
Keep together
```

and:

```text
Low similarity
      ↓
Possible topic change
      ↓
Split here
```

Example:

| Sentence Pair | Similarity |
|---|---:|
| S1 ↔ S2 | 0.86 |
| S2 ↔ S3 | 0.18 |
| S3 ↔ S4 | 0.91 |

Here:

```text
S1 ── 0.86 ── S2
               ↓
             0.18
               ↓
S3 ── 0.91 ── S4
```

The big drop between **S2 and S3** indicates a possible topic change.

Therefore:

```text
Chunk 1:
S1 + S2

Chunk 2:
S3 + S4
```

That's the core idea.

---

# 5. Why Is This Better Than Only Structure-Based Splitting?

Consider:

```text
Paragraph 1:

Farmers are facing problems because of low rainfall.
Modern irrigation can increase crop production.
Virat Kohli is one of the famous IPL players.
He has played for Royal Challengers Bengaluru.
```

A recursive splitter might see:

```text
One paragraph
      ↓
One chunk
```

But semantically:

```text
Agriculture
    ↓
TOPIC CHANGE
    ↓
IPL
```

So semantic splitting can produce:

```text
Chunk 1 → Agriculture

Chunk 2 → IPL
```

This is often better for **embeddings and retrieval**.

---

# 6. Why Is This Important in RAG?

Suppose the user asks:

> "What techniques can help farmers increase crop production?"

If your chunk contains:

```text
Agriculture + IPL + Cricket
```

the embedding represents multiple unrelated topics.

But if the chunk contains only:

```text
Farmers are facing problems because of low rainfall.
Modern irrigation can increase crop production.
```

its embedding is much more focused.

So:

```text
Focused chunk
      ↓
Focused embedding
      ↓
Better retrieval
      ↓
Better context for LLM
      ↓
Potentially better RAG answer
```

---

# 7. Modern Implementation with Hugging Face

Since we're learning this **now**, I would not use an old OpenAI-only example.

We can use a **free Hugging Face embedding model** locally.

A good lightweight starting model is:

**`sentence-transformers/all-MiniLM-L6-v2`**

It is:

- Free
- Open-source
- Small and fast
- Easy to run locally
- Good for learning semantic similarity
- Produces **384-dimensional embeddings**

For larger/multilingual projects, there are stronger models, but this is excellent for understanding the concept without needing an API key.

---

# 8. Install the Required Libraries

```bash
pip install langchain-experimental sentence-transformers
```

We can then use Hugging Face embeddings through LangChain.

---

# 9. Complete Example

```python
from langchain_experimental.text_splitter import SemanticChunker
from langchain_huggingface import HuggingFaceEmbeddings

text = """
Farmers are facing problems because of low rainfall.
Modern irrigation techniques can increase crop production.
Virat Kohli is one of the most famous players in the IPL.
He has played for Royal Challengers Bengaluru for many years.
Terrorism is a serious threat to national security.
Governments use different strategies to prevent terrorism.
"""

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2",
    model_kwargs={"device": "cpu"},
    encode_kwargs={"normalize_embeddings": True}
)

splitter = SemanticChunker(
    embeddings,
    breakpoint_threshold_type="percentile",
    breakpoint_threshold_amount=90
)

chunks = splitter.split_text(text)

for i, chunk in enumerate(chunks, 1):
    print(f"\n--- Chunk {i} ---")
    print(chunk)
```

---

# 10. Understanding the Embedding Configuration

This part is important.

### `model_name`

```python
model_name="sentence-transformers/all-MiniLM-L6-v2"
```

This tells LangChain which Hugging Face embedding model to use.

The model converts:

```text
Text
 ↓
384-dimensional vector
```

---

### `model_kwargs`

```python
model_kwargs={"device": "cpu"}
```

This tells the model to run on CPU.

If you have a properly configured GPU environment, you can use:

```python
model_kwargs={"device": "cuda"}
```

For normal learning/laptop use:

```python
"cpu"
```

is perfectly fine.

---

### `normalize_embeddings`

```python
encode_kwargs={"normalize_embeddings": True}
```

This normalizes the embedding vectors.

This is useful when comparing embeddings using similarity measures such as cosine similarity.

For our semantic splitting use case, keeping it `True` is a sensible configuration.

---

# 11. Understanding `SemanticChunker`

```python
splitter = SemanticChunker(
    embeddings,
    breakpoint_threshold_type="percentile",
    breakpoint_threshold_amount=90
)
```

There are two important ideas here.

### `embeddings`

```python
embeddings
```

This is the embedding model we created.

The splitter uses it to understand how similar neighboring pieces of text are.

---

### `breakpoint_threshold_type`

```python
breakpoint_threshold_type="percentile"
```

This tells the splitter **how to decide what counts as a significant semantic change**.

One useful approach is:

```text
Percentile
```

Instead of manually saying:

> "Similarity below 0.4 means split."

we let the splitter look at the distribution of the semantic differences in the document and identify unusually large changes.

---

### `breakpoint_threshold_amount`

```python
breakpoint_threshold_amount=90
```

This controls how sensitive the splitter is.

Think of it approximately like:

```text
Lower threshold
      ↓
More sensitive
      ↓
More chunks
```

while:

```text
Higher threshold
      ↓
Less sensitive
      ↓
Fewer chunks
```

So don't blindly use `90` for every dataset. It is a parameter you should experiment with.

---

# 12. Other Breakpoint Strategies

Modern `SemanticChunker` supports different ways of determining semantic breakpoints.

Common options include:

```text
percentile
standard_deviation
interquartile
gradient
```

The idea remains the same:

```text
Calculate semantic differences
          ↓
Find unusually large changes
          ↓
Mark them as breakpoints
```

The difference is simply **how we decide that a change is unusually large**.

---

# 13. A Very Important Point

Semantic splitting does **not** mean:

> "The model completely understands the document like a human."

It is still fundamentally working with **embeddings and numerical similarity**.

So:

```text
Sentence
   ↓
Embedding
   ↓
Similarity / distance
   ↓
Breakpoint decision
```

It is a statistical approximation of semantic change.

That's why it can sometimes make imperfect boundaries.

---

# 14. Advantages

### 1. Meaning-aware

It considers semantic similarity instead of only character count.

### 2. Can detect hidden topic changes

Even when two topics are inside the same paragraph:

```text
Agriculture → IPL
```

it may identify the change.

### 3. Useful for RAG

Focused chunks can produce more focused embeddings and potentially improve retrieval.

### 4. Flexible chunk sizes

Chunks don't have to all have exactly the same length.

For example:

```text
Chunk 1 → 2 sentences
Chunk 2 → 5 sentences
Chunk 3 → 3 sentences
```

depending on the semantic boundaries.

---

# 15. Disadvantages

### 1. More computationally expensive

Unlike simple character splitting, we need embeddings.

```text
Text
 ↓
Sentences
 ↓
Embedding model
 ↓
Similarity calculations
 ↓
Chunks
```

This requires more computation.

### 2. Depends on embedding quality

If the embedding model doesn't capture your domain well, semantic boundaries may be poor.

### 3. Can produce unexpected chunks

A semantic boundary isn't always exactly where a human would put it.

### 4. Threshold needs tuning

Different documents may require different settings.

### 5. Not always necessary

For many RAG applications:

```text
RecursiveCharacterTextSplitter
```

is already a very strong and practical choice.

You don't automatically get a better RAG system just because you use semantic splitting.

---

# 16. Semantic vs Recursive Character Splitter

| Feature | Recursive Character | Semantic |
|---|---|---|
| Main idea | Structure | Meaning |
| Uses embeddings | ❌ | ✅ |
| Computational cost | Low | Higher |
| Chunk size | More predictable | Variable |
| Understands topic change | Limited | Better |
| Easy to use | Very easy | More setup |
| RAG usage | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| General-purpose | Excellent | More specialized |

### Practical recommendation

For most projects, start with:

```text
RecursiveCharacterTextSplitter
```

Then consider semantic splitting if you have a genuine problem where structural splitting is producing poor semantic boundaries.
