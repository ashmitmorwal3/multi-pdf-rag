from pathlib import Path

from fastapi import (
    APIRouter,
    UploadFile,
    File,
    HTTPException,
    Form,
)

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


# ==========================================
# UPLOAD PDF
# ==========================================

@router.post("/upload")
async def upload_pdf(
    session_id: str = Form(...),
    file: UploadFile = File(...),
):

    if not session_id:

        raise HTTPException(
            status_code=400,
            detail="Session ID is required."
        )


    if file.content_type != "application/pdf":

        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed."
        )


    # ==========================================
    # CREATE SESSION DIRECTORY
    # ==========================================

    session_dir = UPLOAD_DIR / session_id

    session_dir.mkdir(
        parents=True,
        exist_ok=True
    )


    # ==========================================
    # SAVE PDF
    # ==========================================

    file_path = session_dir / file.filename

    contents = await file.read()

    with open(file_path, "wb") as f:

        f.write(contents)


    # ==========================================
    # LOAD PDF
    # ==========================================

    documents = load_pdf(
        str(file_path)
    )


    # ==========================================
    # SPLIT INTO CHUNKS
    # ==========================================

    chunks = split_documents(
        documents
    )


    # ==========================================
    # ADD SESSION ID TO CHUNK METADATA
    # ==========================================

    for chunk in chunks:

        if chunk.metadata is None:
            chunk.metadata = {}

        chunk.metadata["session_id"] = session_id
        chunk.metadata["source"] = file.filename


    # ==========================================
    # ADD CHUNKS TO CHROMA
    # ==========================================

    add_documents(
        chunks=chunks,
        embeddings=state.embeddings
    )


    # ==========================================
    # RESPONSE
    # ==========================================

    return {

        "filename": file.filename,

        "chunks": len(chunks),

        "session_id": session_id,

        "message":
            "PDF uploaded and indexed successfully."

    }


# ==========================================
# GET DOCUMENTS FOR SESSION
# ==========================================

@router.get("/documents")
def get_documents(
    session_id: str
):

    if not session_id:

        raise HTTPException(
            status_code=400,
            detail="Session ID is required."
        )


    session_dir = UPLOAD_DIR / session_id


    if not session_dir.exists():

        return {
            "documents": []
        }


    files = []


    for file in session_dir.iterdir():

        if (
            file.is_file()
            and file.suffix.lower() == ".pdf"
        ):

            files.append(file.name)


    return {

        "documents": files

    }