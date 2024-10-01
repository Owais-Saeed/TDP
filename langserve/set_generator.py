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
    max_tokens=10000,
    timeout=None,
    max_retries=2,
    streaming=False,
)

# define the data structure.
class Card(BaseModel):
    difficulty: str = Field(description="beginner/intermediate/advanced")
    concept: str = Field(description="The concept the flashcard covers")
    prompt: str = Field(description="The flashcard prompt")
    response: str = Field(description="The flashcard response")
class CardSet(BaseModel):
    set: List[Card] = Field(description="A collection of flashcards")

# set up a parser + inject instructions into the prompt template.
parser = JsonOutputParser(pydantic_object=CardSet)

prompt = PromptTemplate(
    template="""
You will create a set of 8-10 high-quality educational flashcards for a {level} level. The course is about {topic}, and this unit is part of {unit}.
    
The flashcard set should specifically cover each of the following concepts:
{concepts}
    
Your flashcards will range between beginner, intermediate, and advanced levels, with the aim of testing the student's comprehensive knowledge of the topic.
    
### Rules for Creating High-Quality Flashcards
    
I. Content Rules
    
1. Focus on Key Concepts

    - Prioritise the most critical information, including essential definitions, concepts, dates, formulas, and vocabulary.

    - Each flashcard should focus on one concept or question to avoid overloading information.

    - Ensure each flashcard uses concise language.

2. Ensure Clarity

    - Write questions and answers clearly and concisely. Avoid ambiguous language.

    - Use straightforward language that is easy to understand but precise enough to convey the correct meaning.

3. Accuracy is Critical

    - Verify the accuracy of all facts, definitions, and explanations provided on the flashcards.

II. Formatting Rules

1. Consistent Formatting

    - Maintain a consistent format across all flashcards, with the question or prompt on one side and the answer on the other.

2. Markdown Formatting

    - Use **bold** to emphasise key terms.

3. Code blocks

    - Use triple backticks ``` to create a fenced code block.

    - Use single backticks ` for inline code when referring to specific functions, variables, or code snippets within text.

4. Mathematical and Scientific Notation

    - Use LaTeX for **all** mathematical expressions, equations, and formulas.
    
    - Backslashes in LaTeX must be escaped as `\\\\` (double backslash). From here on you will see `\\` single backslashes, but you must use `\\\\` double backslashes in your response.

    - For **standalone** equations, use display mode:
    $$ equation $$
    
    - For **inline** expressions, use inline mode: \\( equation \\)

    - For example, use `\\int` for integrals, `\\alpha` for the Greek letter alpha, and so on.

    - It is critical that you always use LaTeX where appropriate.

III. Cognitive Engagement Rules

1. Promote Active Recall

    - Frame the content in a question-and-answer format to encourage active recall.

    - Use prompts that require the learner to retrieve information rather than just recognize it.

2. Include Varied Question Types

    - Incorporate a mix of question types, including factual, conceptual, and application-based questions.

    - Ensure that some questions challenge the learner to explain “why” or “how” a concept works, promoting deeper understanding.

3. Promote Engagement and Motivation

    - Create flashcards that are engaging and encourage repeated use, such as by using varied question formats and including interesting facts or examples.

    - Avoid monotonous repetition of similar questions; aim to keep the learner motivated and interested.

### Example Flashcards with LaTeX Formatting:

Flashcard 1
- **Question**: What is the formula for the area of a circle?
- **Answer**: $$ A = \\pi r^2 $$

Flashcard 2
- **Question**: How do you find the derivative of \\( f(x) = x^2 \\)?
- **Answer**: $$ f'(x) = 2x $$

Flashcard 3
- **Question**: What is the formula for gravitational force between two masses?
- **Answer**: $$ F = \\frac{G m_1 m_2}{r^2} $$

### Use LaTeX for:

- Mathematical symbols
- Scientific formulas
- Any specialized symbols or notation

### JSON Formatting Instructions

{format_instructions}
\n""",
    input_variables=["level", "topic", "unit", "concepts"],
    partial_variables={"format_instructions": parser.get_format_instructions()},
)

chain = prompt | model | parser