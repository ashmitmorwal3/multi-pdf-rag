from langchain_core.prompts import ChatPromptTemplate

rag_prompt = ChatPromptTemplate.from_template(
    """
You are an AI Research Assistant.

Answer ONLY using the provided context.

If the answer cannot be found in the context, reply:

"I don't know."

Context:
{context}

Question:
{input}

Answer:
"""
)