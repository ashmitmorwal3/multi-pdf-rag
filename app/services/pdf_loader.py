from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader


def load_pdf(pdf_path: str):

    loader = PyPDFLoader(pdf_path)

    documents = loader.load()

    filename = Path(pdf_path).name

    for document in documents:
        document.metadata["source"] = filename

    return documents