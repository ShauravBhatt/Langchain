# Output Parsers in LangChain

## What is an Output Parser?

An **Output Parser** is a component that takes the raw response from an
LLM and converts it into a **specific, usable format** for our
application.

The important point is:

> An LLM is mainly designed to generate human-readable text, but our
> application often needs machine-friendly data.

For example, suppose we ask an LLM:

``` text
Give me the name and age of a student.
```

The model might return:

``` text
Sure! The student's name is Rahul and he is 21 years old.
```

This is easy for a human to understand, but difficult for a program to
reliably use.

Our Python code may actually need something like:

``` python
{
    "name": "Rahul",
    "age": 21
}
```

This is where **Output Parsers** become useful.

------------------------------------------------------------------------

# Why Do We Need Output Parsers?

## 1. LLMs naturally generate unstructured text

LLMs are very good at generating natural language.

For example:

``` text
The product is excellent and offers great value for money.
```

But suppose our application needs only:

``` text
positive
```

We don't want to manually process the complete sentence every time.

An output parser can convert the model's response into the format we
need.

------------------------------------------------------------------------

## 2. Applications need predictable output

Imagine we are building a sentiment-analysis application.

We ask the LLM:

``` text
Classify this review as positive or negative.
```

The model might return:

``` text
I would classify this review as positive because the customer
is very happy with the product.
```

But our application may need:

``` text
positive
```

A predictable output makes it much easier to use the result in our
program.

For example:

``` text
LLM
 ↓
Output Parser
 ↓
"positive"
 ↓
Python application
```

------------------------------------------------------------------------

## 3. We often need structured data

Many applications don't just need one piece of text.

For example, we may ask the LLM to extract:

-   Name
-   Age
-   Email
-   Skills

Instead of receiving a paragraph, we want something structured:

``` json
{
    "name": "Rahul",
    "age": 21,
    "email": "rahul@example.com",
    "skills": ["Python", "ML"]
}
```

Structured output is much easier for Python code to work with.

For example:

``` python
result["name"]
result["age"]
result["skills"]
```

------------------------------------------------------------------------

## 4. Output parsers reduce manual processing

Without an output parser, we may have to manually:

1.  Receive the LLM response
2.  Extract the required information
3.  Clean the text
4.  Convert it into the required format
5.  Validate whether the result is correct

Output parsers provide a standard way to handle this conversion.

So instead of:

``` text
LLM → messy text → manual processing → usable data
```

we can have:

``` text
LLM → Output Parser → usable data
```

------------------------------------------------------------------------

# Important Idea

An Output Parser **does not make the LLM generate better knowledge**.

Its main job is to handle the **format of the output**.

Think of it like this:

``` text
LLM
 ↓
Generates the answer
 ↓
Output Parser
 ↓
Converts the answer into the format our application needs
```

So:

**LLM = generates**

**Output Parser = formats / converts / validates the generated output**

------------------------------------------------------------------------

# Output Parser Types

We will study these step by step:

## 1. Without StrOutputParser

First, we will see what the raw output of the LLM looks like when we
don't use a string output parser.

This helps us understand the problem that parsers solve.

------------------------------------------------------------------------

## 2. StrOutputParser

Converts the model's response into a **plain Python string**.

``` text
LLM → StrOutputParser → String
```

Useful when we simply want the final text response.

------------------------------------------------------------------------

## 3. JsonOutputParser

Converts the LLM response into **JSON-style structured data**.

``` text
LLM → JsonOutputParser → JSON
```

Useful when our application needs multiple fields in a machine-readable
format.

------------------------------------------------------------------------

## 4. StructuredOutputParser

Allows us to define the fields we expect from the LLM using response
schemas.

``` text
LLM → StructuredOutputParser → Structured output
```

Useful when we want the model to follow a predefined output structure.

------------------------------------------------------------------------

## 5. PydanticOutputParser

Uses a **Pydantic model** to define and validate the expected output.

For example:

``` python
class Student(BaseModel):
    name: str
    age: int
```

The parser expects the LLM output to follow this structure.

``` text
LLM
 ↓
PydanticOutputParser
 ↓
Validated Pydantic object
```

This gives us both **structure and validation**.

------------------------------------------------------------------------

# Overall Picture

Different parsers solve different output requirements:

  Parser                   Main Purpose
  ------------------------ ----------------------------------------
  No parser                Raw model response
  StrOutputParser          Plain string
  JsonOutputParser         JSON data
  StructuredOutputParser   Predefined structured fields
  PydanticOutputParser     Structured + validated Pydantic object

The main problem we are solving is:

``` text
LLM gives us a response
        ↓
But our application needs a predictable format
        ↓
Output Parser converts the response
        ↓
Our application can easily use the result
```

**Core idea:**

> Output Parsers act as a bridge between the LLM's generated response
> and the format our application expects.
