from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.core import state
from app.core.config import APP_NAME, APP_VERSION

from app.services.embedding import get_embedding_model
from app.services.retriever import get_retriever
from app.services.llm import get_llm

from app.chains.rag_chain import create_rag_chain
from app.chains.history_chain import create_history_chain
from app.chains.retrieval_chain import create_chain

from app.api.upload import router as upload_router
from app.api.routes import router

from app.database.init_db import init_db

from app.database.database import Base
from app.database.database import engine

# Import models so SQLAlchemy knows about them
from app.database import models



from fastapi.middleware.cors import CORSMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):

    print("Creating Database...")
    init_db()


    print("Loading Embedding Model...")
    state.embeddings = get_embedding_model()

    print("Loading Retriever...")
    state.retriever = get_retriever(state.embeddings)

    print("Loading LLM...")
    state.llm = get_llm()

    print("Building Document Chain...")
    document_chain = create_rag_chain(
        state.llm
    )

    print("Building History Aware Retriever...")
    history_retriever = create_history_chain(
        state.llm,
        state.retriever
    )

    print("Building Retrieval Chain...")
    state.rag_chain = create_chain(
        history_retriever,
        document_chain
    )

    print("Application Ready!")

    yield

    print("Server Stopped")


app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION,
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://multi-pdf-rag-two.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload_router)
app.include_router(router)


@app.get("/")
def home():
    return {
        "message": "Welcome to the Multi-Document AI Research Assistant!"
    }


@app.get("/health")
def health():
    return {
        "status": "ok"
    }


@app.get("/version")
def version():
    return {
        "version": APP_VERSION
    }