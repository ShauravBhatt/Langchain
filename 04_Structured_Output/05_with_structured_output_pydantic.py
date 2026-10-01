from typing import Optional, Literal
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langchain_groq import ChatGroq

load_dotenv()

# Create the LLM.
model = ChatGroq(
    model="openai/gpt-oss-20b"
)


# Define the exact structure we want from the LLM.
class Review(BaseModel):
    key_themes: list[str] = Field(
        description="Write down all the key themes discussed in the review in a list"
    )

    summary: str = Field(
        description="A brief summary about the whole review."
    )

    # Literal restricts the output to only these 3 values.
    sentiment: Literal["pos", "neg", "neutral"] = Field(
        description="Sentiment of the review: pos, neg, or neutral."
    )

    pros: Optional[list[str]] = Field(
        default=None,
        description="Write down all the pros inside the list"
    )

    cons: Optional[list[str]] = Field(
        default=None,
        description="Write down all the cons inside the list"
    )

    name: Optional[str] = Field(
        default=None,
        description="Write the name of ref"
    )


# Connect the Pydantic schema with the LLM.
structured_model = model.with_structured_output(Review)


result = structured_model.invoke(
    """
I recently upgraded to the Samsung Galaxy S24 Ultra, and I must say, it’s an absolute powerhouse! The Snapdragon 8 Gen 3 processor makes everything lightning fast—whether I’m gaming, multitasking, or editing photos. The 5000mAh battery easily lasts a full day even with heavy use, and the 45W fast charging is a lifesaver.

The S-Pen integration is a great touch for note-taking and quick sketches, though I don’t use it often. What really blew me away is the 200MP camera—the night mode is stunning, capturing crisp, vibrant images even in low light. Zooming up to 100x actually works well for distant objects, but anything beyond 30x loses quality.

However, the weight and size make it a bit uncomfortable for one-handed use. Also, Samsung’s One UI still comes with bloatware—why do I need five different Samsung apps for things Google already provides? The $1,300 price tag is also a hard pill to swallow.

Pros:
Insanely powerful processor (great for gaming and productivity)
Stunning 200MP camera with incredible zoom capabilities
Long battery life with fast charging
S-Pen support is unique and useful

Cons:
Bulky and heavy—not great for one-handed use
Bloatware still exists in One UI
Expensive compared to competitors
"""
)

print(result)


"""
CONCEPT:

This time we use Pydantic instead of TypedDict.

Pydantic gives us:
- Field descriptions → help the LLM understand each field.
- Literal → restricts values to specific choices.
- Optional → field can be missing/None.
- Field(default=...) → sets a default value.

So the LLM reads the review and returns data
matching the `Review` schema.
"""