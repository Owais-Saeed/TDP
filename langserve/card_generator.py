# Gemini Integration
from langchain_google_genai import ChatGoogleGenerativeAI
# LangChain Core
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
from pydantic import BaseModel, Field
# Arrays
from typing import Any, Dict, List

# Define your desired data structure.
class Card(BaseModel):
    difficulty: str = Field(description="beginner/intermediate/advanced")
    prompt: str = Field(description="The flashcard prompt")
    response: str = Field(description="The flashcard response")
class CardSet(BaseModel):
    set: List[Card] = Field(description="A collection of flashcards")

# create the model
model = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    temperature=0.4,
    max_tokens=500,
    timeout=None,
    max_retries=2,
    streaming=False,
    # other params...
)

# Set up a parser + inject instructions into the prompt template.
parser = JsonOutputParser(pydantic_object=CardSet)

prompt = PromptTemplate(
    template="Create a set of flashcards based on the provided topic.\n{format_instructions}\n{query}\n",
    input_variables=["query"],
    partial_variables={"format_instructions": parser.get_format_instructions()},
)

chain = prompt | model | parser