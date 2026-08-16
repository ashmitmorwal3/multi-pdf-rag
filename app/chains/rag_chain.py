from langchain_classic.chains.combine_documents import (
    create_stuff_documents_chain,
)

from app.prompts.rag_prompt import rag_prompt


def create_rag_chain(llm):

    chain = create_stuff_documents_chain(
        llm,
        rag_prompt,
    )

    return chain