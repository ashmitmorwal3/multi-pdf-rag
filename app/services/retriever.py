from app.services.vector_store import load_vector_store


def get_retriever(
    embeddings,
    session_id: str | None = None,
    documents: list[str] | None = None,
):

    # ==========================================
    # LOAD CHROMA VECTOR STORE
    # ==========================================

    vector_store = load_vector_store(
        embeddings
    )


    # ==========================================
    # BASE SEARCH SETTINGS
    # ==========================================

    search_kwargs = {
        "k": 4
    }


    # ==========================================
    # BUILD FILTER
    # ==========================================

    filters = []


    # ------------------------------------------
    # SESSION FILTER
    # ------------------------------------------

    if session_id:

        filters.append(
            {
                "session_id": session_id
            }
        )


    # ------------------------------------------
    # DOCUMENT FILTER
    # ------------------------------------------

    if documents:

        filters.append(
            {
                "source": {
                    "$in": documents
                }
            }
        )


    # ==========================================
    # APPLY FILTER
    # ==========================================

    if len(filters) == 1:

        search_kwargs["filter"] = filters[0]

    elif len(filters) > 1:

        search_kwargs["filter"] = {
            "$and": filters
        }


    # ==========================================
    # CREATE RETRIEVER
    # ==========================================

    retriever = vector_store.as_retriever(
        search_kwargs=search_kwargs
    )


    return retriever