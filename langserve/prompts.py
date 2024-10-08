# prompts.py

# ====================================================================================================
# OUTLINE INSTRUCTIONS

outline_instructions = r"""
Provide a unit outline based on {topic}.
Aim for a high-school level, between 4-6 units.

{format_instructions}
\n"""

# ====================================================================================================
# FLASHCARD INSTRUCTIONS

# ----------------------------------------------------------------------------------------------------
# GENERATION INSTRUCTIONS

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
- **Varying Difficulty**: The cards should cover beginner, intermediate, and advanced concepts.
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
    - **Difficulty**: "beginner"
	- **Front**: "What is the **powerhouse of the cell**?"
	- **Back**: "**Mitochondria** generate most of the cell's ATP, providing energy for cellular activities."

- **Example Flashcard 2**
    - **Difficulty**: "beginner"
	- **Front**: "Describe the process of **photosynthesis**."
	- **Back**: "**Photosynthesis** converts sunlight, carbon dioxide, and water into glucose and oxygen in plant cells."

- **Example Flashcard 3**
    - **Difficulty**: "intermediate"
	- **Front**: "How does **mitosis** differ from **meiosis**?"
	- **Back**: "**Mitosis** produces two identical daughter cells for growth, while **meiosis** creates four genetically diverse gametes for reproduction."

- **Example Flashcard 4**
    - **Difficulty**: "beginner"
	- **Front**: "What does the `def` keyword do in Python?"
	- **Back**: "The `def` keyword defines a *new function* in Python."

- **Example Flashcard 5**
    - **Difficulty**: "beginner"
	- **Front**: "What is the formula for the **area of a circle**?"
	- **Back**: "$$ A = \\pi r^2 $$"


**Flashcards**:
\n'''

# ----------------------------------------------------------------------------------------------------
# EDITING INSTRUCTIONS

editing_instructions = r'''
You are an educational content reviewer tasked with evaluating a set of flashcards created for a {level} level student studying "{topic}" in the "{unit}" unit. Your objective is to ensure that each flashcard adheres to the established guidelines for quality, accuracy, and educational effectiveness.

**Key Concept to Cover**:
{concept}

**Avoid** the following concepts as they will be covered elsewhere in the unit:
{concepts_to_avoid}


**Flashcard Review Guidelines**:
Rewrite the flashcards where you see fit, ensuring the following:
	- **One Concept Per Card**: Where a single card explores too many concepts, split it into separate cards exploring each concept individually.
	- **Active Recall**: Where a card does not encourage active recall (as a simple yes/no question) rewrite the card to promote the active retrieval of information using 'who', 'what', 'where', 'when', and 'how' based questions.
	- **Conciseness**: Where a card is too wordy, reword the card to use concise language. Be careful to ensure the flashcards continue to use the front (prompt) and back (response) format.
	- **Keep key terms on the front**: Key terms should be located on the front of the card, and definitions on the back.


**Original Flashcards**
{generated_cards}


**Updated Flashcards**
\n'''

# ----------------------------------------------------------------------------------------------------
# FORMATTING INSTRUCTIONS

formatting_instructions = r'''
You are a formatting specialist tasked with refining a set of educational flashcards for a {level} level student studying "{topic}" in the "{unit}" unit. Your objective is to ensure that each flashcard adheres to the established formatting guidelines to enhance readability and effectiveness.

**Flashcards to Format**:
{edited_cards}

**Formatting Rules**:

1. **Markdown Formatting**:
   - **Bold (`**text**`)** for key terms and concepts.
   - **Italics (`*text*`)** for emphasis within explanations.
   - **Avoid Lists**: Each flashcard should have a clear **Front** and **Back** without additional list formatting.
   - **Avoid New Lines**: Flashcards should have a clear **Front** and **Back** that spans a single line each, the only exception is for code blocks and LaTeX equations.

2. **Code Formatting**:
   - Use backticks (\`) for inline code snippets (e.g., `def`).
   - Use triple backticks (\`\`\`) for fenced code blocks if including larger code segments.

3. **Mathematical and Scientific Notation**:
   - **Standalone Equations**: Enclose LaTeX expressions within double dollar signs (`$$`) for proper rendering.
     - Example: "$$ A = \\pi r^2 $$"
   - **Inline Expressions**: For smaller mathematical expressions within text, use single dollar signs (`$`).
     - Example: "The formula for area is $A = \\pi r^2$."

4. **Clarity and Precision**:
   - Ensure that questions and answers are concise and easily understandable.
   - Avoid overly complex wording or jargon unless necessary for the concept.

5. **Consistency**:
   - Maintain uniform formatting across all flashcards.
   - Ensure that similar concepts are formatted in the same manner to aid recognition and learning.

6. **Avoid Over-Formatting**:
   - Limit the use of bold and italics to prevent visual clutter.
   - Only emphasize the most critical information to guide the student's focus effectively.

**Example Formatting**:

```markdown
1. **Front**: "What is the **powerhouse of the cell**?"
   **Back**: "**Mitochondria** generate most of the cell's ATP, providing energy for cellular activities."

2. **Front**: "Describe the process of **photosynthesis**."
   **Back**: "**Photosynthesis** converts *sunlight*, carbon dioxide, and water into glucose and oxygen in plant cells."

3. **Front**: "How does **mitosis** differ from **meiosis**?"
   **Back**: "**Mitosis** produces two identical daughter cells for growth, while **meiosis** creates four genetically diverse gametes for reproduction."

4. **Front**: "What does the `def` keyword do in Python?"
   **Back**: "The `def` keyword defines a *new function* in Python."

5. **Front**: "What is the **area of a circle** formula?"
   **Back**: "$$ A = \\pi r^2 $$"
```

{format_instructions}

**Task**:
- Apply the above formatting rules to each flashcard.
- Ensure that all flashcards are uniformly formatted and free of errors.
- Maintain the integrity and clarity of the content while enhancing its presentation.

Provide the formatted flashcards below.
\n'''