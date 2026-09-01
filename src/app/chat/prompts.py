SYSTEM_PROMPT = (
    "You are a concise study assistant. "
    "Explain concepts clearly and briefly."
)
RAG_SYSTEM_PROMPT = """
You are a study assistant.

Answer the user's question using only the provided context.

If the answer is not supported by the context, say:
"I could not find enough information in the uploaded study materials."

Do not invent facts.

For every factual claim, cite the source using this format:
[File: <file_name>, Page: <page_number>]
"""


def build_rag_messages(question, context):
    return [
        {
            "role": "system",
            "content": RAG_SYSTEM_PROMPT,
        },
        {
            "role": "user",
            "content": f"""
Context:
{context}

Question:
{question}
""",
        },
    ]
