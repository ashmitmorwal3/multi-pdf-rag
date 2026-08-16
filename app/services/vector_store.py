from langchain_chroma import Chroma

PERSIST_DIRECTORY = "data/chroma"


def create_vector_store(chunks, embeddings):

    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=PERSIST_DIRECTORY
    )

    return vector_store


def load_vector_store(embeddings):

    return Chroma(
        persist_directory=PERSIST_DIRECTORY,
        embedding_function=embeddings
    )


def add_documents(chunks, embeddings):

    vector_store = load_vector_store(embeddings)

    vector_store.add_documents(chunks)

    return vector_store