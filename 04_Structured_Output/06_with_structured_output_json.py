from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

model = ChatGroq(
    model="openai/gpt-oss-20b"
)


# ---------------------------------------------------------
# JSON SCHEMA
#
# A schema is basically a "blueprint" for the output.
#
# We are telling the LLM:
# "Your answer should have these fields,
#  and each field should contain this type of data."
# ---------------------------------------------------------

json_schema = {

    # Name of our schema
    "title": "Review",

    # The final output should be a JSON object/dictionary.
    "type": "object",

    # Define the fields inside that object.
    "properties": {

        # key_themes should be a list of strings.
        "key_themes": {
            "type": "array",
            "items": {
                "type": "string"
            },
            "description": "Write down all the key themes discussed in the review in a list"
        },

        # summary should be a string.
        "summary": {
            "type": "string",
            "description": "A brief summary of the review"
        },

        # sentiment must be one of the allowed values.
        "sentiment": {
            "type": "string",
            "enum": ["pos", "neg", "neutral"],
            "description": "Return sentiment of the review either negative, positive or neutral"
        },

        # pros can either be a list of strings OR null.
        "pros": {
            "type": ["array", "null"],
            "items": {
                "type": "string"
            },
            "description": "Write down all the pros inside a list"
        },

        # cons can either be a list of strings OR null.
        "cons": {
            "type": ["array", "null"],
            "items": {
                "type": "string"
            },
            "description": "Write down all the cons inside a list"
        },

        # name can be a string OR null.
        "name": {
            "type": ["string", "null"],
            "description": "Write the name of the reviewer"
        }
    },

    # These fields MUST be present in the final output.
    "required": ["key_themes", "summary", "sentiment"]
}


# Give this schema to LangChain.
# Now the model knows what structure its output should follow.
structured_model = model.with_structured_output(json_schema)


result = structured_model.invoke(
    """
I recently upgraded to the Samsung Galaxy S24 Ultra, and I must say, it’s an absolute powerhouse! The Snapdragon 8 Gen 3 processor makes everything lightning fast—whether I’m gaming, multitasking, or editing photos. The 5000mAh battery easily lasts a full day even with heavy use, and the 45W fast charging is a lifesaver.

The S-Pen integration is a great touch for note-taking and quick sketches, though I don’t use it often. What really blew me away is the 200MP camera—the night mode is stunning, capturing crisp, vibrant images even in low light. Zooming up to 100x actually works well for distant objects, but anything beyond 30x loses quality.

However, the weight and size make it a bit uncomfortable for one-handed use. Also, Samsung’s One UI still comes with bloatware. The $1,300 price tag is also a hard pill to swallow.

Pros:
Insanely powerful processor
Stunning 200MP camera
Long battery life with fast charging
S-Pen support

Cons:
Bulky and heavy
Bloatware
Expensive

by Shaurav Bhatt
"""
)

print(result)


"""
SCHEMA BASICS:

Think of JSON Schema as a blueprint.

"type": "object"
    → Output should be a dictionary/object.

"properties"
    → Defines what fields the object can have.

"required"
    → Defines which fields MUST be present.

"type": "string"
    → Normal text.

"type": "array"
    → A list.

"items": {"type": "string"}
    → The list must contain strings.

"enum": ["pos", "neg"]
    → Only these values are allowed.

"type": ["array", "null"]
    → The value can be a list OR None.

"description"
    → Gives the LLM instructions about what that field means.


EXPECTED OUTPUT:

{
    "key_themes": ["performance", "camera", "battery"],
    "summary": "The phone has strong performance...",
    "sentiment": "pos",
    "pros": ["powerful processor", "great camera"],
    "cons": ["heavy", "expensive"],
    "name": "Shaurav Bhatt"
}


IMPORTANT:

Pydantic:
    Python class → schema

JSON Schema:
    Dictionary → schema

Both describe the SAME basic idea:

    "Here is the structure I want from the LLM."
"""