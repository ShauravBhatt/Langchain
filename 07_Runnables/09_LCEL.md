# LCEL — LangChain Expression Language

## 1. What is LCEL?

**LCEL = LangChain Expression Language**

LCEL is the expression-style way of **composing Runnables into chains/workflows**.

The basic idea is:

```text
Runnable → Runnable → Runnable
```

Because LangChain components follow the Runnable interface, LCEL can connect them easily.

---

## 2. Why LCEL?

Without LCEL, we may manually pass outputs between components:

```python
prompt_output = prompt.invoke(input)
model_output = model.invoke(prompt_output)
final_output = parser.invoke(model_output)
```

With LCEL:

```python
chain = prompt | model | parser
```

Then:

```python
result = chain.invoke(input)
```

The `|` operator connects the output of one Runnable to the input of the next.

```text
Input
  ↓
Prompt
  ↓
Model
  ↓
Parser
  ↓
Output
```

---

## 3. Basic LCEL Syntax

```python
chain = runnable1 | runnable2 | runnable3
```

Example:

```python
chain = prompt | model | parser
```

Read it as:

> Output of `prompt` goes to `model`, and model output goes to `parser`.

---

## 4. LCEL With Prompt + Model + Parser

```python
chain = prompt | model | StrOutputParser()

response = chain.invoke({
    "topic": "AI"
})
```

Flow:

```text
{"topic": "AI"}
       ↓
PromptTemplate
       ↓
formatted prompt
       ↓
Model
       ↓
model response
       ↓
StrOutputParser
       ↓
string
```

We don't need to manually call every component.

---

## 5. LCEL vs RunnableSequence

You previously used:

```python
chain = RunnableSequence(
    prompt,
    model,
    parser
)
```

LCEL provides a shorter expression for the same sequential composition:

```python
chain = prompt | model | parser
```

So think:

```text
RunnableSequence
    ↓
explicit sequence

LCEL |
    ↓
concise way to compose that sequence
```

---

## 6. LCEL + RunnableParallel

Runnables can also be composed into parallel workflows.

```python
parallel_chain = RunnableParallel({
    "tweet": tweet_chain,
    "linkedin": linkedin_chain
})
```

Conceptually:

```text
                 ┌── tweet chain ───→ tweet
Input ───────────┤
                 └── linkedin chain → linkedin
```

LCEL is therefore not limited to simple linear flows.

---

## 7. LCEL + RunnablePassthrough

You used `RunnablePassthrough()` to keep an intermediate value while also sending it to another chain.

```python
parallel_chain = RunnableParallel({
    "joke": RunnablePassthrough(),
    "explanation": prompt2 | model | parser
})
```

Flow:

```text
                 ┌── Passthrough ──→ joke
Generated joke ──┤
                 └── prompt2 → model → parser → explanation
```

---

## 8. LCEL + RunnableLambda

A normal Python function can participate in a chain using `RunnableLambda`.

```python
def word_counter(text):
    return len(text.split())

chain = joke_gen_chain | RunnableParallel({
    "joke": RunnablePassthrough(),
    "total_words": RunnableLambda(word_counter)
})
```

Flow:

```text
Generated joke
      ↓
     ┌──────────────────────┐
     ↓                      ↓
Passthrough           RunnableLambda
     ↓                      ↓
   joke                word_counter()
                              ↓
                         total_words
```

So custom Python logic can become part of the Runnable workflow.

---

## 9. LCEL + RunnableBranch

You can also use LCEL inside conditional branches.

```python
branch_chain = RunnableBranch(
    (
        lambda x: len(x.split()) > 500,
        prompt2 | model | parser
    ),
    RunnablePassthrough()
)
```

Flow:

```text
             input
               ↓
        length > 500?
          /          \
        YES           NO
         ↓             ↓
    summarize       return same
```

---

## 10. LCEL Is Not a Component

LCEL itself is not:

- an LLM
- a PromptTemplate
- an OutputParser
- a model

LCEL is the **expression syntax used to compose Runnables**.

Think:

```text
Components
    ↓
Runnables
    ↓
LCEL composition
    ↓
Chain / Workflow
    ↓
invoke()
```

---

## 11. Complete Example

```python
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

prompt = PromptTemplate(
    template="Tell me one interesting fact about {topic}",
    input_variables=["topic"]
)

chain = prompt | model | StrOutputParser()

result = chain.invoke({
    "topic": "Artificial Intelligence"
})

print(result)
```

The key LCEL part is:

```python
chain = prompt | model | StrOutputParser()
```

---

## 12. Mental Model

Think of LCEL as a **pipeline syntax**:

```text
Input
  ↓
Prompt
  ↓
Model
  ↓
Parser
  ↓
Output
```

The code:

```python
prompt | model | parser
```

is simply the compact representation of that pipeline.

---

## 13. Runnable Concepts You Have Learned

| Runnable | Purpose |
|---|---|
| `RunnableSequence` | Run components one after another |
| `RunnableParallel` | Run multiple branches |
| `RunnablePassthrough` | Pass input unchanged |
| `RunnableLambda` | Run custom Python function |
| `RunnableBranch` | Choose a branch using a condition |

LCEL gives you a concise way to **compose these building blocks**.

---

# Final Mental Model

```text
Runnables = Building blocks

LCEL = Syntax to connect those blocks

Chain = Resulting workflow

invoke() = Execute the workflow
```

### One-line definition

> **LCEL is LangChain's expression-style syntax for composing Runnables into readable and reusable chains/workflows.**

### Most important syntax

```python
chain = prompt | model | parser
```
