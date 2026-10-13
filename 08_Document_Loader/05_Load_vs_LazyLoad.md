# Document Loader: Eager Loading vs Lazy Loading

Document loaders can load documents in two main ways:

- **Eager Loading → `load()`**
- **Lazy Loading → `lazy_load()`**

---

## 1. Eager Loading — `load()`

**Eager loading** means:

> Load **all documents immediately** and return them together as a list.

### Example

```python
from langchain_community.document_loaders import TextLoader

loader = TextLoader("notes.txt")

docs = loader.load()

print(docs)
print(len(docs))
```

### Working

```text
notes.txt
   ↓
load()
   ↓
All documents loaded into memory
   ↓
List[Document]
```

So `load()` waits until the loading is complete and then returns the complete list.

### Best when

- Number of documents is small
- Dataset easily fits in memory
- You need all documents immediately

---

# 2. Lazy Loading — `lazy_load()`

**Lazy loading** means:

> Documents are loaded **one at a time when you iterate over them**, instead of loading everything at once.

### Example

```python
loader = TextLoader("notes.txt")

docs = loader.lazy_load()

for doc in docs:
    print(doc)
```

Here, `lazy_load()` returns an **iterator**, not a complete list.

### Working

```text
Documents
   ↓
lazy_load()
   ↓
Document 1 → process
Document 2 → process
Document 3 → process
...
```

It does **not** load everything into memory at once.

---

# 3. `load()` vs `lazy_load()`

| Feature | `load()` | `lazy_load()` |
|---|---|---|
| Loading | All at once | One by one |
| Return | List | Iterator |
| Memory usage | Higher | Lower |
| Processing | After loading | During iteration |
| Useful for | Small datasets | Large datasets |

---

## Simple Mental Model

### `load()`

```python
docs = loader.load()
```

**"Pehle sab kuch load karo, phir mujhe do."**

### `lazy_load()`

```python
docs = loader.lazy_load()

for doc in docs:
    # Process one document
```

**"Jab mujhe next document chahiye, tab load karo."**

---

## Important Point

`lazy_load()` does **not** mean that the document is never loaded.

It means the documents are **loaded progressively/on demand**, rather than all being loaded into memory at once.

For large directories or datasets, lazy loading can be much more memory-efficient.