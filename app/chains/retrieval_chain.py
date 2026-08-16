from langchain_classic.chains.retrieval import create_retrieval_chain


def create_chain(
    retriever,
    document_chain,
):
    chain = create_retrieval_chain(
        retriever=retriever,
        combine_docs_chain=document_chain,
    )

    return chain