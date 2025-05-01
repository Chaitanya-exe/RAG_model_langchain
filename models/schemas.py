from pydantic import BaseModel

class AnswerResponse(BaseModel):
    answer: str

class QuestionRequest(BaseModel):
    question: str