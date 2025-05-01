from fastapi import FastAPI, UploadFile, File, HTTPException, Form, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from api.upload_and_prepare import router as handler
from api.give_answer import router as answer_handler

app = FastAPI(title="RAG backend API" , description="API for rag application to communicate with the frontend", version="1.0.0")

class userRequest(BaseModel):
    username: str
    password: str

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)
app.include_router(handler, tags=["handler"])
app.include_router(answer_handler, tags=["answers"])

@app.post("/info")
async def handleData(userData: userRequest):
    print("Info recieved")
    print(f"username: {userData.username}\npassword: {userData.password}")
    return {"message": "data recieved"}

@app.get("/")
async def root():   
    return {"message":"RAG_AI pdf is running"}

def main():
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000,)


if __name__ == "__main__":
    main()