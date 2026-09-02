from fastapi import FastAPI, UploadFile, File, HTTPException
from app.chat.service import answer_question
from pydantic import BaseModel
from app.chat.storage import (create_session,
                              save_message,
                              get_history,
                              session_exists,
                              document_exists)
from app.rag.pipeline import ingest_document
from pathlib import Path

app = FastAPI()

UPLOAD_DIR = Path("data/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


class Source(BaseModel):
    file_name: str
    page_number: int


class ChatRequest(BaseModel):
    session_id: str
    question: str
    document_id: int


class ChatResponse(BaseModel):
    answer: str
    sources: list[Source]


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/sessions")
def new_session():
    session_id = create_session()

    return {
        "session_id": session_id
    }


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):

    if not session_exists(request.session_id):
        raise HTTPException(
            status_code=404,
            detail="Session not found.",
        )
    if not document_exists(request.document_id):
        raise HTTPException(
            status_code=404,
            detail="Document not found."
        )

    history = get_history(request.session_id)

    response = answer_question(
        user_input=request.question,
        history=history,
        document_id=request.document_id,
    )

    save_message(
        session_id=request.session_id,
        role="user",
        content=request.question,
    )

    save_message(
        session_id=request.session_id,
        role="assistant",
        content=response["answer"],
    )

    return response


@app.post("/documents/upload")
def upload_document(file: UploadFile = File(...)):

    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="Only pdf files are allowed."
        )
    file_path = UPLOAD_DIR / file.filename
    with open(file_path, "wb") as buffer:
        buffer.write(file.file.read())
    try:
        document_id = ingest_document(file_path)

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail="Failed to process the document.",
        ) from error

    return {
        "document_id": document_id,
        "file_name": file.filename,
    }
