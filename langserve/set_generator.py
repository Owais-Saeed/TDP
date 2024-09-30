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
    front: str = Field(description="The flashcard prompt")
    back: str = Field(description="The flashcard response")
class CardSet(BaseModel):
    set: List[Card] = Field(description="A collection of flashcards")

# set up a parser + inject instructions into the prompt template.
parser = JsonOutputParser(pydantic_object=CardSet)

prompt = PromptTemplate(
    template = r"""
You will create a set of 8-10 high-quality **concise** educational flashcards for a {level} level student. The course topic is {topic}, and this set is part of {unit}. Flashcards must focus on **active recall** by framing the front of the card as a **question** and providing a clear, concise answer on the back.

The flashcards should cover the following key concepts:
{concepts}

### Key Rules for Creating Flashcards that Encourage Active Recall

#### I. Content Rules

1. **One Concept Per Card**
    - Each flashcard must focus on a **single concept**. Do not include multiple related ideas on one card.
    - If you need to explore more than one aspect of a concept (e.g., a formula and its application), create **separate flashcards** for each aspect.

2. **Focus on Key Concepts**
    - Prioritize essential information, like definitions, concepts, formulas, or important principles.
    - Each card must have **one question** on the front, and the **concise answer** on the back.

3. **Frame Questions to Require Active Recall**
    - Use clear, direct questions that prompt the learner to retrieve one key piece of information or understanding per card.
    - Avoid yes/no questions. Instead, ask for explanations, definitions, or formulas.

4. **Keep Answers Concise and Direct**
    - Limit responses to **1-2 sentences** to ensure clarity and simplicity.
    - Avoid over-explaining; focus on the key information necessary to answer the question.

5. **Accuracy is Critical**
    - Verify the accuracy of all facts, definitions, and explanations provided on the flashcards.

#### II. Formatting Rules

1. **Consistent and Simple Formatting**
    - Ensure that the formatting is clean and minimal, without unnecessary elaboration.

2. **Markdown Formatting**
    - Use **bold** markdown formatting to emphasize key terms.
    - The only markdown-specific formatting you are allowed to use is **bold**, eg. do not create lists.

3. **Clarity and Precision**
    - Both the question and answer must be easily understandable at a glance.
    - Avoid vague or overly complex wording.

4. **Code blocks**
    - Use triple backticks (```) to create a fenced code block.
    - Use single backticks (`) for inline code when referring to specific functions, variables, or code snippets within text.

5. **Mathematical and Scientific Notation**
    - Use LaTeX for **all** mathematical expressions, equations, and formulas.
    - Backslashes in LaTeX must be escaped as `\\` (double backslash). You must use `\\` double backslashes in your response.
    - For **standalone** equations, use display mode: $$ equation $$
    - For **inline** expressions, use inline mode: \\( equation \\)
    - For example, use `\\int` for integrals, `\\alpha` for the Greek letter alpha, and so on.
    - It is critical that you always use LaTeX where appropriate.

#### III. Cognitive Engagement Rules

1. **Promote Active Recall**
    - Frame the content in a question-and-answer format to encourage active recall.
    - Use prompts that require the learner to retrieve information rather than just recognize it.

2. **Include Varied Question Types**
    - Incorporate a mix of question types, including factual, conceptual, and application-based questions.
    - Ensure that some questions challenge the learner to explain “why” or “how” a concept works, promoting deeper understanding.

3. **Promote Engagement and Motivation**
    - Create flashcards that are engaging and encourage repeated use, such as by using varied question formats and including interesting facts or examples.
    - Avoid monotonous repetition of similar questions; aim to keep the learner motivated and interested.

#### Example Flashcards:

- **Front**: "What is the formula for the area of a circle?"
- **Back**: "$$ A = \\pi r^2 $$"

- **Front**: "What is the goal when balancing a chemical equation?"
- **Back**: "Equal atoms on both sides."

#### Use LaTeX for:

- Mathematical symbols
- Scientific formulas
- Any specialized symbols or notation

---

Ensure that each flashcard is clear, concise, and encourages active recall. Cover the following concepts: {concepts}.

Ensure that each flashcard covers one concept at a time. If a topic requires explaining more than one concept, prefer creating multiple flashcards rather than combining them into one.

{format_instructions}
\n""",
    input_variables = ["level", "topic", "unit", "concepts"],
    partial_variables = {"format_instructions": parser.get_format_instructions()},
)


chain = prompt | model | parser