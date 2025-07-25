from typing import List # from mcp we will have a list of questions then we will store them in the list
from pydantic import BaseModel, Field, validator
## BaseModel is a class from pydantic that allows us to create data models with validation
## Field is used to define the fields of the model (default values) with additional metadata
## validator is used to define validation rules for the fields

class MCQQuestion(BaseModel):
    question: str= Field(description="The question text")
    options: list[str]= Field(description="list of 4 options")
    correct_answer: str= Field(description="The correct answer from the options list")

    @validator('question', pre=True)
    def clean_question(cls, value):
        if isinstance(value, dict):
            return value.get("description", str(value))
        return str(value)


class FillBlankQuestion(BaseModel):
    question: str = Field(description="The question text with the '___' for the blank")
    correct_answer: str = Field(description="The correct word or phase for the blank")
    

    @validator('question', pre=True)
    def clean_question(cls, value):
        if isinstance(value, dict):
            return value.get("description", str(value)) # convert to string if a dict
        return str(value) # convert to string if not a dict

'''

Great, Shubhansh! Let’s break down the code from your screenshot step by step. This is a Pydantic model named MCQQuestion, and it’s being used to define and validate the structure of a multiple choice question object.

⸻

📌 Code Breakdown:

from typing import List
from pydantic import BaseModel, Field, validator

	•	List: To define a list of strings (i.e. multiple options).
	•	BaseModel: Base class for Pydantic models.
	•	Field: Used for adding metadata (like description) and constraints.
	•	validator: Decorator for custom field validation.

⸻

🎯 Model Definition:

class MCQQuestion(BaseModel):

This defines a data model for an MCQ (Multiple Choice Question). It extends BaseModel, so Pydantic can handle validation and parsing.

⸻

🧩 Fields:

question: str = Field(description="The question text")
options: List[str] = Field(description="List of 4 options")
correct_answer: str = Field(description="The correct answer from the options")

	•	question: A string that holds the question.
	•	options: A list of strings (4 options for the MCQ).
	•	correct_answer: A string that must match one of the options.

All three fields use Field(...) to provide helpful descriptions for documentation, validation, or auto-generating forms (e.g. in FastAPI).

⸻

🔍 Custom Validator:

@validator('question', pre=True)
def clean_question(cls, v):
    if isinstance(v, dict):
        return v.get('description', str(v))
    return str(v)

✅ What it does:

This validator runs before the built-in validation (pre=True) and cleans up the question field:
	•	If the input for question is a dictionary, it tries to extract the value from the 'description' key.
	•	If it’s not a dictionary, it just converts the input to a string.

✅ Use Case:

This is useful if the incoming data might have a nested structure like:

{
  "question": { "description": "What is Python?" }
}

This validator ensures only the text "What is Python?" gets stored in the final model.

⸻

🧪 Example Input

data = {
    "question": {"description": "What is the capital of India?"},
    "options": ["Delhi", "Mumbai", "Kolkata", "Chennai"],
    "correct_answer": "Delhi"
}
q = MCQQuestion(**data)
print(q.question)  # "What is the capital of India?"


⸻

✅ Summary:

Component	Purpose
BaseModel	Defines a Pydantic model
Field(...)	Adds description and constraints
List[str]	Defines a list of string options
@validator	Cleans or validates specific fields
pre=True	Runs the validator before default validation


⸻

Let me know if you’d like to extend this with:
	•	Option count validation (exactly 4 options)
	•	Checking if correct_answer is one of the options
	•	Integration with FastAPI or MongoDB schemas

Would you like that?



'''