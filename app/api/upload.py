from pathlib import Path

from fastapi import APIRouter, UploadFile, File, HTTPException

from app.core import state

from app.services.pdf_loader import load_pdf
from app.services.text_splitter import split_documents
from app.services.vector_store import add_documents


router = APIRouter()


UPLOAD_DIR = Path("data/uploads")

UPLOAD_DIR.mkdir(
    parents=True,
    exist_ok=True
)


@router.post("/upload")
async def upload_pdf(
    file: UploadFile = File(...)
):

    if file.content_type != "application/pdf":

        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed."
        )


    file_path = UPLOAD_DIR / file.filename


    contents = await file.read()


    with open(file_path, "wb") as f:

        f.write(contents)


    # Load PDF
    documents = load_pdf(
        str(file_path)
    )


    # Split into chunks
    chunks = split_documents(
        documents
    )


    # Add chunks to Chroma
    add_documents(
        chunks=chunks,
        embeddings=state.embeddings
    )


    return {

        "filename": file.filename,

        "chunks": len(chunks),

        "message":
            "PDF uploaded and indexed successfully."

    }


@router.get("/documents")
def get_documents():

    files = []

    for file in UPLOAD_DIR.iterdir():

        if file.is_file() and file.suffix.lower() == ".pdf":

            files.append(file.name)


    return {
        "documents": files
    }