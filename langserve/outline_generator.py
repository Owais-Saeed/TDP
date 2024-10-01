# Gemini Integration
from langchain_google_genai import ChatGoogleGenerativeAI
# LangChain Core
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
from pydantic import BaseModel, Field
# Arrays
from typing import Any, Dict, List

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
class Unit(BaseModel):
    title: str = Field(description="Title of the unit")
    concepts: List[str] = Field(description="Outline of the topics covered in the unit")

class Topic(BaseModel):
    topic: str = Field(description="The topic of the course")
    level: str = Field(description="The level of the course, e.g., High-school")
    units: Dict[str, Unit] = Field(description="Dictionary of unit numbers mapped to Unit objects")

class Course(BaseModel):
    course: Topic = Field(description="A course, containing units about a given topic")

# set up a parser + inject instructions into the prompt template.
parser = JsonOutputParser(pydantic_object=Course)

prompt = PromptTemplate(
    template="""
Provide a unit outline based on {topic}.
Aim for a high-school level, between 4-6 units.

{format_instructions}
\n""",
    input_variables=["topic"],
    partial_variables={"format_instructions": parser.get_format_instructions()},
)

chain = prompt | model | parser