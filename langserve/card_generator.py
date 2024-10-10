# card_generator.py

# Gemini Integration
from langchain_google_genai import GoogleGenerativeAI
# LangChain
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain_core.runnables import RunnableLambda
# Pydantic
from pydantic import BaseModel, Field
# Arrays
from typing import Any, Dict, List
# Prompts
from prompts import generation_instructions, editing_instructions, formatting_instructions

# [ Request Example ]
# Level: High-school
# Topic: Photosynthesis
# Unit: Introduction to Photosynthesis
# Concept: The Photosynthesis Equation

# create the model
model = GoogleGenerativeAI(
    model="gemini-1.5-flash-8b",
    temperature=0.3,
    max_tokens=5000,
)

# memory variable
memory = {}

# functions to access and manipulate memory
def store_input(input_data):
    memory.update(input_data)
    return input_data

def get_memory():
    return memory

def store_content(ai_message, descriptor: str):
    memory.update({descriptor: ai_message})
    return memory


# define the data structure using pydantic
class Card(BaseModel):
    difficulty: str = Field(description="beginner/intermediate/advanced")
    front: str = Field(description="The flashcard prompt")
    back: str = Field(description="The flashcard response")
class Cards(BaseModel):
    cards: List[Card] = Field(description="A collection of flashcards")

# create the parsers
str_parser = StrOutputParser()
json_parser = JsonOutputParser(pydantic_object=Cards)

# ---- [ STEP 1 ] -- [ Create Flashcards ] ----

generation_prompt = PromptTemplate(
    template = generation_instructions,
    input_variables = ["level", "topic", "unit", "concept", "concepts_to_avoid"],
)

generation_store = RunnableLambda(lambda x: store_content(x, "generated_cards"))

generation_chain = (
        store_input | generation_prompt | model | generation_store
    ).with_config({"run_name": "Generation"})

# ---- [ STEP 2 ] -- [ Edit the Flashcards ] ----

editing_prompt = PromptTemplate(
    template = editing_instructions,
    input_variables = ["generated_cards", "level", "topic", "unit", "concept", "concepts_to_avoid"],
)

editing_store = RunnableLambda(lambda x: store_content(x, "edited_cards"))

editing_chain = (
        editing_prompt | model | editing_store
    ).with_config({"run_name": "Editing"})

# ---- [ STEP 4 ] -- [ Output valid format ] ----

formatting_prompt = PromptTemplate(
    template = formatting_instructions,
    input_variables = ["edited_cards"],
    partial_variables = {"format_instructions": json_parser.get_format_instructions()},
)

formatting_chain = (
        formatting_prompt | model | json_parser
    ).with_config({"run_name": "Formatting"})


# ------ [ Final Chain ] ------

final_chain = (
        generation_chain | editing_chain | formatting_chain
    ).with_config({"run_name": "Full flashcard generation"})
