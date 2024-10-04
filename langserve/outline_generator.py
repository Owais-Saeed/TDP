# Gemini Integration
from langchain_google_genai import ChatGoogleGenerativeAI
# LangChain Core
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel, Field
# Arrays
from typing import Any, Dict, List
# Prompts
from prompts import outline_instructions

# create the model
model = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    temperature=0.3,
    max_tokens=1000,
    timeout=None,
    max_retries=2,
    streaming=False,
)

# define the data structure

class Concept(BaseModel):
    concept : str = Field(description="A concept covered by the unit")
    # set : List[Card]

class Unit(BaseModel):
    id : int = Field(description="Unit number")
    title : str = Field(description="Title of the unit")
    outline : List[Concept]

class Course(BaseModel):
    topic : str = Field(description="The topic of the course")
    level : str = Field(description="The level of the course, e.g., High-school")
    units : List[Unit] = Field(description="List of the units in the course")


# set up a parser + inject instructions into the prompt template.
parser = JsonOutputParser(pydantic_object=Course)

prompt = PromptTemplate(
    template=outline_instructions,
    input_variables=["topic"],
    partial_variables={"format_instructions": parser.get_format_instructions()},
)

chain = prompt | model | parser