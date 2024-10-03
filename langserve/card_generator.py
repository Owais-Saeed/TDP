# card_generator.py

# Gemini Integration
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
# LangChain
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain_core.runnables import RunnableLambda
# Pydantic
from pydantic import BaseModel, Field
# Arrays
from typing import Any, Dict, List

# [ Request Example ]
# Level: High-school
# Topic: Photosynthesis
# Unit: Introduction to Photosynthesis
# Concept: The Photosynthesis Equation

class UserInput(BaseModel):
    type: str = "UserInput"
    level: str
    topic: str
    unit: str
    concept: str
    concepts_to_avoid: str

# memory
memory = {}

generation_instructions = r'''
You are an educational content creator. Generate a set of 8–10 concise flashcards for a {level} level student. The course topic is "{topic}", and this set is part of "{unit}".

Each flashcard should focus on active recall by presenting a question on the front (the prompt) and a clear, concise answer on the back (the response).

**Key concept to cover**: {concept}

**Do not** cover the following concepts, as they will be addressed elsewhere in the unit: {concepts_to_avoid}


**Guidelines**:

- **One Concept Per Card**: Each flashcard must address a single concept.
- **Focus on Key Concepts**: Prioritize essential information like definitions, concepts, formulas, or important principles.
- **Active Recall**: Frame questions to prompt retrieval of information, avoiding yes/no questions.
- **Concise Answers**: Limit answers to 1-2 sentences.
- **Accuracy**: Ensure all information is factually correct.
- **Australian English**: Responses should be provided using proper Australian English.


**Formatting Guidelines**:

- **Bold (`**text**`) key terms and concepts**:
	- **Front Questions**: Bold key terms or phrases central to the question.
	- **Back Answers**: Bold the primary term being defined or explained.
- **Use italics (`*text*`) for emphasis within explanations**:
	- Emphasise descriptive phrases or secondary information that supplements the key term.
	- Use italics sparingly to add subtle emphasis without overshadowing key terms.
- **Code Formatting (`\`code\``)**:
   - Enclose programming keywords or code snippets in backticks to distinguish them from regular text.
- **Mathematical Notation**:
   - Use LaTeX within double dollar signs (`$$`) for standalone equations to ensure proper formatting and readability.
- **Avoid Over-Formatting**:
   - Limit the use of bold and italics to prevent visual clutter and maintain focus on the most critical information.


**Example Flashcards**:

- **Example Flashcard 1**
	- **Front**: "What is the **powerhouse of the cell**?"
	- **Back**: "**Mitochondria** generate most of the cell's ATP, providing energy for cellular activities."

- **Example Flashcard 2**
	- **Front**: "Describe the process of **photosynthesis**."
	- **Back**: "**Photosynthesis** converts sunlight, carbon dioxide, and water into glucose and oxygen in plant cells."

- **Example Flashcard 3**
	- **Front**: "How does **mitosis** differ from **meiosis**?"
	- **Back**: "**Mitosis** produces two identical daughter cells for growth, while **meiosis** creates four genetically diverse gametes for reproduction."

- **Example Flashcard 4**
	- **Front**: "What does the `def` keyword do in Python?"
	- **Back**: "The `def` keyword defines a *new function* in Python."

- **Example Flashcard 5**
	- **Front**: "What is the formula for the **area of a circle**?"
	- **Back**: "$$ A = \\pi r^2 $$"


**Flashcards**:
\n'''

refinement_instructions = r'''

You are an educational editor, editing content for a {level} level student. The course topic is "{topic}", and this set is part of "{unit}".

Each flashcard should focus on active recall by presenting a question on the front (the prompt) and a clear, concise answer on the back (the response).

**Key concept to cover**: {concept}

**Do not** cover the following concepts, as they will be addressed elsewhere in the unit: {concepts_to_avoid}

You must edit the following flashcards to use concise language.

All cards must span a single line, new lines are not allowed.

All cards must retain a front (prompt) and back (response) format.

## The Flashcards
{generated_cards}
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
{refined_cards}
\n'''

# create the model
model = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    temperature=0.3,
    max_tokens=5000,
)

# function to extract the content from the AIMessage object
def extract_content(ai_message):
    return {"content": ai_message.content}

def store_input(input_data):
    memory.update(input_data)
    return input_data

def get_memory():
    return memory

def store_content(ai_message, descriptor: str):
    memory.update({descriptor: ai_message.content})
    return memory


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
    input_variables = ["level", "topic", "unit", "concept", "concepts_to_avoid"],
)

generation_chain = (
        #store_input | generation_prompt | model | extract_content | pass_content_and_memory
        store_input | generation_prompt | model | RunnableLambda(lambda x: store_content(x, "generated_cards"))
    ).with_config({"run_name": "Generation"})

# ---- [ STEP 2 ] -- [ Refine the cards ] ----

refinement_prompt = PromptTemplate(
    template = refinement_instructions,
    input_variables = ["generated_cards", "level", "topic", "unit", "concept", "concepts_to_avoid"],
)

refinement_chain = (
        refinement_prompt | model | RunnableLambda(lambda x: store_content(x, "refined_cards"))
    ).with_config({"run_name": "Refinement"})

# ---- [ STEP 3 ] -- [ Output valid format ] ----

formatting_prompt = PromptTemplate(
    template = formatting_instructions,
    input_variables = ["refined_cards"],
    partial_variables = {"format_instructions": json_parser.get_format_instructions()},
)

formatting_chain = (
        formatting_prompt | model | json_parser
    ).with_config({"run_name": "Formatting"})


# ------ [ Final Chain ] ------

final_chain = (
        generation_chain | refinement_chain | formatting_chain
    ).with_config({"run_name": "Full flashcard generation"})
