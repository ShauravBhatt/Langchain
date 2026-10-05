# Introduction to Runnables in LangChain

## 1. The Bigger Picture: Why Runnables Exist

Before understanding **Runnables**, understand the problem LangChain was trying to solve.

When LLM applications started becoming common, developers were not only calling an LLM. A real application could involve many steps:

- Load a document
- Split it into smaller chunks
- Generate embeddings
- Store them in a vector database
- Retrieve relevant information
- Build a prompt
- Send the prompt to an LLM
- Parse and display the output

So, **calling an LLM was only one small part of an entire LLM application**.

LangChain gradually introduced reusable components for these different jobs:

- Document Loaders
- Text Splitters
- Embedding Models
- Vector Stores
- Retrievers
- Prompt Templates
- Output Parsers
- Memory
- LLM/Model interfaces

The idea was simple:

> Instead of rebuilding every piece from scratch, developers could pick components and connect them to create applications.

---

## 2. From Components → Chains

Once these components existed, another pattern became obvious.

Many LLM applications repeatedly performed the same combinations of operations.

For example, a basic application might do:

```text
User Topic
   ↓
Prompt Template
   ↓
LLM
   ↓
Response
```

Traditionally, the developer had to manually write the glue code connecting these components.

LangChain introduced **Chains** to package such repeated workflows.

### Example: LLM Chain

Instead of manually doing:

```text
Prompt Template → format prompt → LLM → get response
```

an **LLMChain** could handle the whole flow.

You provide:

- an LLM
- a prompt template

and the chain handles the intermediate work.

So a Chain is essentially:

> **A predefined workflow that connects multiple components to perform a particular task.**

---

## 3. Chains Became Powerful... and Then Created a Problem

As more use cases appeared, more specialized chains were created.

Some examples:

| Chain | Purpose |
|---|---|
| **LLMChain** | Connects a prompt with an LLM |
| **SequentialChain** | Runs multiple chains in sequence |
| **SimpleSequentialChain** | Simpler sequential workflow |
| **ConversationalRetrievalChain** | Conversational Q&A with retrieval and memory |
| **RetrievalQA** | Retrieves relevant documents and uses an LLM to answer |
| **RouterChain** | Routes a request to different chains based on intent |
| **MultiPromptChain** | Selects different prompts dynamically |
| **HydeChain** | Uses hypothetical documents to improve retrieval |
| **AgentExecutorChain** | Coordinates tools/actions through an agent |
| **SQLDatabaseChain** | Converts natural-language questions into database-related operations |

This list is **not exhaustive**. The important idea is that chains were being created for many recurring workflows.

### The problem?

Too many specialized chains created two major issues:

**1. Large codebase**

More chains meant more custom implementation and maintenance.

**2. Steep learning curve**

A new developer had to remember:

> "For this use case, which chain should I use?"

So the abstraction that was supposed to make LangChain easier was itself becoming difficult to learn.

---

# 4. The Root Cause: Components Were Not Standardized

This is the key idea behind Runnables.

Different LangChain components originally behaved differently.

For example:

```text
LLM              → predict(...)
Prompt Template  → format(...)
Retriever        → get_relevant_documents(...)
Output Parser    → parse(...)
```

Notice the problem?

Each component had its **own interface**.

Because their interfaces were different, they could not simply be plugged together.

Developers therefore needed custom glue code:

```text
Prompt Template
      ↓
   custom code
      ↓
     LLM
```

And for retrieval:

```text
Retriever
    ↓
custom code
    ↓
Prompt
    ↓
custom code
    ↓
LLM
```

As more combinations appeared, more custom chains had to be created.

### The ideal solution

What if all these components followed a **common standard interface**?

Then instead of writing custom code for every combination, components could directly connect with one another.

That is the fundamental motivation behind **Runnables**.

---

# 5. What Exactly Is a Runnable?

A **Runnable** can be thought of as a **unit of work**.

It:

```text
Input
  ↓
Runnable
  ↓
Output
```

Every Runnable has some specific purpose.

For example:

- A prompt Runnable transforms input into a prompt.
- A model Runnable generates a response.
- A parser Runnable converts model output into a desired format.
- A retriever Runnable finds relevant information.

The important part is not what the Runnable does internally.

The important part is:

> **How you interact with it.**

---

# 6. The Common Interface

LangChain Runnables follow a **common interface**.

That means different Runnables expose common operations.

### `invoke()`

Used when you want to provide one input and get one output.

```text
Input → invoke() → Output
```

### `batch()`

Used when multiple inputs need to be processed together.

```text
Input 1 ─┐
Input 2 ─┼→ batch() → Outputs
Input 3 ─┘
```

### `stream()`

Used when you want output progressively instead of waiting for the complete result.

```text
Input
  ↓
stream()
  ↓
chunk → chunk → chunk → ...
```

So instead of learning a completely different execution method for every component, you get a common way of interacting with them.

**That standardization is the real power.**

---

# 7. Runnables Can Be Connected

Because Runnables share a common interface, they can be composed.

Suppose:

```text
R1 → R2 → R3
```

Then:

- R1 receives the original input.
- R1 produces an output.
- That output automatically becomes R2's input.
- R2's output becomes R3's input.

So you can build workflows like:

```text
Input
  ↓
Prompt
  ↓
Model
  ↓
Parser
  ↓
Final Output
```

No need to manually write glue code between every step.

---

# 8. The Powerful Part: A Workflow Is Also a Runnable

This is where the concept becomes interesting.

Suppose you create:

```text
R1 → R2 → R3
```

That entire pipeline can itself behave like **one Runnable**.

So now you can treat:

```text
(R1 → R2 → R3)
```

as a single unit and connect it to another Runnable:

```text
(R1 → R2 → R3) → R4 → R5
```

This gives you **composition**.

You can build small pieces, combine them into larger workflows, and then combine those workflows again.

Think:

```text
Small Runnable
      ↓
Small Workflow
      ↓
Larger Workflow
      ↓
Complete Application
```

Yahi concept makes the architecture scalable.

---

# 9. The LEGO Analogy

The easiest mental model for Runnables is **LEGO blocks**.

### 1. Each block has a purpose

Different LEGO pieces have different shapes and purposes.

Similarly:

> Every Runnable performs some unit of work.

### 2. Blocks follow a common connection system

LEGO pieces may look different, but their connection mechanism is standardized.

Similarly:

> Runnables may perform completely different tasks, but they expose a common interface.

### 3. Blocks can be connected

```text
Block A → Block B → Block C
```

Similarly:

```text
Runnable A → Runnable B → Runnable C
```

### 4. A completed structure becomes a larger building block

A collection of LEGO pieces can form a larger structure, which can conceptually become part of an even bigger structure.

Same with Runnables:

```text
R1 → R2 → R3
```

can be treated as one composable unit.

Then:

```text
Workflow A → Workflow B → Workflow C
```

can form an even larger workflow.

---

# 10. Why This Changes LangChain

The original Chain-heavy approach was roughly:

```text
Different Components
        ↓
Different Interfaces
        ↓
Custom Glue Code
        ↓
Many Specialized Chains
```

The Runnable approach moves toward:

```text
Different Components
        ↓
Common Interface
        ↓
Composable Runnables
        ↓
Flexible Workflows
```

So the key shift is:

> **Instead of creating a new Chain for every possible combination, make components composable through a common interface.**

That is the real "why" behind Runnables.

---

# 11. The Mental Model to Keep

Don't memorize Runnables as just another LangChain class.

Think of them as an **architecture for composition**.

```text
             Runnables
                 │
        ┌────────┼────────┐
        ↓        ↓        ↓
      Input    Process   Output
                 │
        Common Interface
                 │
        ┌────────┼────────┐
        ↓        ↓        ↓
      invoke   batch    stream
                 │
                 ↓
          Composition
                 │
                 ↓
       Complex Workflows
```

### One-line definition

> **A Runnable is a standardized, composable unit of work in LangChain that takes an input, performs a task, and produces an output.**

The magic is not merely that it "runs something."

The magic is that **different kinds of work can speak the same interface**, allowing them to be connected like LEGO blocks.
