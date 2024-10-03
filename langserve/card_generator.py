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

generation_instructions = r'''
You will create a set of 8-10 high-quality **concise** educational flashcards for a {level} level student. The course topic is {topic}, and this set is part of {unit}. Flashcards must focus on **active recall** by framing the front of the card as a **question** and providing a clear, concise answer on the back.

The flashcards will range between beginner, intermediate, and advanced levels.

Use LaTeX to represent **all** mathematical expressions, equations, and formulas.

The flashcards should cover the following key concept:
{concept}
\n'''

refinement_instructions = r'''
You must edit the following flashcards to use concise language.

All cards must span a single line, new lines are not allowed.

All cards must retain a front (prompt) and back (response) format.

## The Flashcards
{content}
\n'''

formatting_instructions = r'''
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
{content}
\n'''

# [ Request Example ]
# Level: High-school
# Topic: Photosynthesis
# Unit: Introduction to Photosynthesis
# Concept: The Photosynthesis Equation

# create the model
model = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    temperature=0.3,
    max_tokens=5000,
)

# function to extract the content from the AIMessage object
def extract_content(ai_message):
    return {"content": ai_message.content}

# define the data structure using pydantic
class Card(BaseModel):
    difficulty: str = Field(description="beginner/intermediate/advanced")
    front: str = Field(description="The flashcard prompt")
    back: str = Field(description="The flashcard response")
class Set(BaseModel):
    set: List[Card] = Field(description="A collection of flashcards")

# create the parsers
str_parser = StrOutputParser()
json_parser = JsonOutputParser(pydantic_object=Set)

# ---- [ STEP 1 ] -- [ Create Flashcards ] ----

generation_prompt = PromptTemplate(
    template = generation_instructions,
    input_variables = ["level", "topic", "unit", "concept"],
)

generation_chain = (generation_prompt | model | extract_content).with_config({"run_name": "Generation"})

# ---- [ STEP 2 ] -- [ Refine the cards ] ----

refinement_prompt = PromptTemplate(
    template = refinement_instructions,
    input_variables = ["content"],
)

refinement_chain = (refinement_prompt | model | extract_content).with_config({"run_name": "Refinement"})

# ---- [ STEP 3 ] -- [ Output valid format ] ----

formatting_prompt = PromptTemplate(
    template = formatting_instructions,
    input_variables = ["content"],
    partial_variables = {"format_instructions": json_parser.get_format_instructions()},
)

formatting_chain = (formatting_prompt | model | json_parser).with_config({"run_name": "Formatting"})


# ------ [ Final Chain ] ------

final_chain = (generation_chain | refinement_chain | formatting_chain).with_config({"run_name": "Full flashcard generation"})
