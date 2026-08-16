from app.services.vector_store import load_vector_store


def get_retriever(
    embeddings,
    session_id: str | None = None,
    documents: list[str] | None = None,
):

    vector_store = load_vector_store(
        embeddings
    )

    search_kwargs = {
        "k": 4
    }

    # ==========================================
    # FILTER BY SESSION
    # ==========================================

    if session_id:

        search_kwargs["filter"] = {
            "session_id": session_id
        }

    # ==========================================
    # FILTER BY DOCUMENTS
    # ==========================================

    if documents:

        document_filter = {
            "source": {
                "$in": documents
            }
        }

        if session_id:

            search_kwargs["filter"] = {
                "$and": [
                    {
                        "session_id": session_id
                    },
                    document_filter
                ]
            }

        else:

            search_kwargs["filter"] = (
                document_filter
            )

    # ==========================================
    # CREATE RETRIEVER
    # ==========================================

    retriever = vector_store.as_retriever(
        search_kwargs=search_kwargs
    )

    return retriever