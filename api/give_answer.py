from fastapi import APIRouter, HTTPException
from rag.get_answer import prepare_answer
from models.schemas import AnswerResponse, QuestionRequest

router = APIRouter()

@router.post("/get_answer", response_model=AnswerResponse)
async def generate_answer(request: QuestionRequest):
    if request.question == None:
        HTTPException(status_code=404, detail="user question not in body")
    
    user_question = request.question
    answer = prepare_answer(user_question)

    if answer:
        return AnswerResponse(
            answer=answer
        )
    else: 
        return HTTPException(status_code=500, detail="error generating answer")