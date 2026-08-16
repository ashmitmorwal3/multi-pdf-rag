from langchain_classic.chains.history_aware_retriever import (
    create_history_aware_retriever,
)

from app.prompts.history_prompt import history_prompt


def create_history_chain(
    llm,
    retriever,
):
    return create_history_aware_retriever(
        llm,
        retriever,
        history_prompt,
    )