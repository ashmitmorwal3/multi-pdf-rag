from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts import MessagesPlaceholder

history_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """Given the chat history and the latest user question,
rewrite the question so it can be understood without the chat history.

Do NOT answer the question.

Only rewrite it if necessary.

Otherwise return it unchanged."""
        ),

        MessagesPlaceholder("chat_history"),

        (
            "human",
            "{input}"
        )
    ]
)