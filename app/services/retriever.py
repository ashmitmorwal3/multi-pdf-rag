from app.services.vector_store import load_vector_store


def get_retriever(
    embeddings,
    documents: list[str] | None = None
):

    vector_store = load_vector_store(embeddings)

    search_kwargs = {
        "k": 4
    }

    # Filter by selected PDFs
    if documents:

        search_kwargs["filter"] = {
            "source": {
                "$in": documents
            }
        }

    retriever = vector_store.as_retriever(
        search_kwargs=search_kwargs
    )

    return retriever