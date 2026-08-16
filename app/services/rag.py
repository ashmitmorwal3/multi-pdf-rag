from app.services.embedding import get_embedding_model
from app.services.retriever import get_retriever
from app.services.llm import get_llm
from app.chains.rag_chain import create_rag_chain
from app.core import state

def ask_question(question: str):

    docs = state.retriever.invoke(question)

    context = "\n\n".join(
        [doc.page_content for doc in docs]
    )

    answer = state.rag_chain.invoke(
        {
            "context": context,
            "question": question
        }
    )

    return answer