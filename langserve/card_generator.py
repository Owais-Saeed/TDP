# card_generator.py

# Gemini Integration
from langchain_google_genai import ChatGoogleGenerativeAI
# LangChain
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
# Pydantic
from pydantic import BaseModel, Field
# Arrays
from typing import Any, Dict, List

# [ Request Example ]
# Level: High-school
# Topic: Photosynthesis
# Unit: Introduction to Photosynthesis
# Concept: The Photosynthesis Equation

class CardRequest(BaseModel):
    level: str
    topic: str
    unit: str
    concept: str

# create the model
model = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    temperature=0.3,
    max_tokens=5000,
)

# Create a number of flashcards ranging in difficulty based on a single concept in a unit

# ---- [ STEP 1 ] -- [ Create Flashcards ] ----

str_parser = StrOutputParser()

flashcards_prompt = PromptTemplate(
    template = r"""
You will create a set of 8-10 high-quality **concise** educational flashcards for a {level} level student. The course topic is {topic}, and this set is part of {unit}. Flashcards must focus on **active recall** by framing the front of the card as a **question** and providing a clear, concise answer on the back.

The flashcards should cover the following key concept:
{concept}
\n""",
    input_variables = ["level", "topic", "unit", "concept"],
)

flashcards_chain = flashcards_prompt | model

# ---- [ STEP 2 ] -- [ Output valid format ] ----

# define the data structure using pydantic
class Card(BaseModel):
    difficulty: str = Field(description="beginner/intermediate/advanced")
    front: str = Field(description="The flashcard prompt")
    back: str = Field(description="The flashcard response")
class Set(BaseModel):
    set: List[Card] = Field(description="A collection of flashcards")

json_parser = JsonOutputParser(pydantic_object=Set)

formatting_prompt = PromptTemplate(
    template = r"""
You will format the provided flashcards as outlined.

## LaTeX Formatting Instructions

    - Use LaTeX for **all** mathematical expressions, equations, and formulas.
    - Backslashes in LaTeX must be escaped as `\\` (double backslash). You must use `\\` double backslashes in your response.
    - For **standalone** equations, use display mode: $$ equation $$
    - For **inline** expressions, use inline mode: \\( equation \\)
    - For example, use `\\int` for integrals, `\\alpha` for the Greek letter alpha, and so on.
    - It is critical that you always use LaTeX where appropriate.

## JSON Formatting Instructions

{format_instructions}

## Flashcards
{flashcards}
\n""",
    input_variables = ["flashcards"],
    partial_variables = {"format_instructions": json_parser.get_format_instructions()},
)

formatting_chain = formatting_prompt | model | json_parser


# ------ [ Final Chain ] ------

final_chain = flashcards_chain | formatting_chain
