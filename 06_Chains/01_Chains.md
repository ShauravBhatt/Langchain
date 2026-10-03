# Chains in LangChain

## 1. What is a Chain?

A **Chain** is a way to connect multiple LangChain components into a single workflow.

Instead of manually doing:

```text
Input
  ↓
Prompt
  ↓
LLM
  ↓
Parser
  ↓
Output
```

we can package this workflow into a Chain.

### Simple definition

> **A Chain connects multiple components so that the output of one step can be used as the input of the next step.**

---

# 2. Why Do We Need Chains?

Suppose we have a PromptTemplate and an LLM.

Without a Chain, we manually write:

```python
prompt = template.format(topic="AI")

response = llm.predict(prompt)
```

Here, **we are writing the glue code** that connects the two components.

As workflows become bigger:

```text
Prompt
  ↓
LLM
  ↓
Parser
  ↓
Another Prompt
  ↓
Another LLM
  ↓
Final Output
```

managing all these connections manually becomes harder.

A Chain packages this workflow into one reusable object.

---

# 3. Basic Idea

Think of a Chain as a **pipeline**.

```text
Component 1
     ↓
Component 2
     ↓
Component 3
     ↓
Output
```

For example:

```text
PromptTemplate
      ↓
     LLM
      ↓
 OutputParser
```

The Chain manages the flow between these components.

So instead of calling every component separately, we can execute the workflow through the Chain.

---

# 4. Simple Example

Imagine we want to generate a joke.

We have:

```text
PromptTemplate
      ↓
      LLM
```

The PromptTemplate creates:

```text
"Write a joke about AI"
```

Then the LLM receives that prompt and generates:

```text
AI walked into a bar...
```

A Chain combines these steps:

```text
Input: topic = AI
        ↓
PromptTemplate
        ↓
"Write a joke about AI"
        ↓
LLM
        ↓
Joke
```

The developer does not need to manually connect every step.

---

# 5. Chain Hides the Glue Code

This is the main reason Chains were useful.

### Without Chain

```python
formatted_prompt = prompt.format({
    "topic": "AI"
})

result = llm.predict(formatted_prompt)

answer = result["response"]
```

We manually manage:

```text
format()
   ↓
predict()
   ↓
extract output
```

### With Chain

The Chain contains this workflow internally.

Conceptually:

```python
chain.run({
    "topic": "AI"
})
```

The Chain handles:

```text
Input
  ↓
Prompt formatting
  ↓
LLM
  ↓
Output
```

---

# 6. Chains Can Represent Complete Workflows

A Chain does not have to contain only two components.

It can represent a larger workflow:

```text
Input
  ↓
Prompt
  ↓
LLM
  ↓
Parser
  ↓
Another Prompt
  ↓
LLM
  ↓
Final Output
```

For example:

```text
Topic
  ↓
Generate Joke
  ↓
Explain Joke
  ↓
Final Explanation
```

This entire process can be treated as one workflow.

---

# 7. Chain of Chains

An important idea is that a larger workflow can be built from smaller chains.

Example:

```text
Chain 1
Generate Joke
     ↓
Chain 2
Explain Joke
     ↓
Final Result
```

So instead of thinking only in terms of individual components:

```text
Prompt → LLM → Parser
```

we can also think:

```text
Chain 1 → Chain 2 → Chain 3
```

This makes larger workflows easier to organize.

---

# 8. Common Chain Pattern

A very common LLM workflow is:

```text
Prompt
  ↓
LLM
  ↓
Output Parser
```

Conceptually:

```python
chain = Prompt + LLM + Parser
```

The exact API can differ depending on the LangChain version and the type of chain being used, but the core idea remains:

> **Combine multiple steps into one executable workflow.**

---

# 9. The Problem With Traditional Chains

Chains solved the problem of manually connecting components, but as LangChain grew, many different specialized Chain classes appeared.

For example, different workflows could require different Chain implementations.

This could make the API harder to learn and compose.

Conceptually, you might end up thinking:

```text
Which Chain class should I use?
How does this Chain accept input?
How does this Chain return output?
Can I connect it to another component?
```

Different components also historically had different interfaces.

For example:

```text
PromptTemplate → format()
LLM            → predict()
Chain          → run()
```

The interfaces were not fully standardized.

This became an important limitation.

---

# 10. This Leads to Runnables

This is the connection to the topic you studied next.

The evolution can be understood as:

```text
Individual Components
        ↓
      Chains
        ↓
Need for more flexible composition
        ↓
     Runnables
        ↓
       LCEL
```

### Chains

Focused on packaging common workflows.

### Runnables

Provide a more standardized way for components and workflows to be composed.

### LCEL

Provides concise syntax for composing those Runnables.

For example:

```python
prompt | model | parser
```

We will learn all these in next lecture till then focus on chains. 

### One-line definition

> **A Chain is a workflow that connects multiple LangChain components so their operations can be executed together as one process.**

### The key problem Chains solved

```text
Manual glue code
      ↓
      Chain
      ↓
Reusable workflow
```

### The key limitation that led to Runnables

```text
Many specialized Chains
+
Different interfaces
+
Need for flexible composition
      ↓
Runnables
```
