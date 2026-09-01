from app.chat.prompts import build_rag_messages
from app.llm.client import generate_response
from app.rag.retrieval import build_context, retrieve_chunks


def build_sources(results):
    sources = []
    seen = set()

    for result in results:
        source_key = (
            result["file_name"],
            result["page_number"]
        )
        if source_key in seen:
            continue
        seen.add(source_key)

        sources.append(
            {
                "file_name": result["file_name"],
                "page_number": result["page_number"],
            }
        )

    return sources


def build_retrieval_question(history, user_input):
    if not history:
        return user_input

    previous_user_message = None

    for message in reversed(history):
        if message["role"] == "user":
            previous_user_message = message["content"]
            break

    if previous_user_message is None:
        return user_input

    return f"{previous_user_message}\nFollow-up: {user_input}"


def run_chat():
    history = []
    while True:
        user_input = input("You: ")

        if user_input.lower() == "exit":
            break

        retrieval_question = build_retrieval_question(
            history=history,
            user_input=user_input,
        )

        results = retrieve_chunks(
            question=retrieval_question,
            top_k=3,
        )
        for result in results:
            print("Distance:", result["distance"])
            print("Page:", result["page_number"])
            print("Text:", result["text"])
            print("-" * 50)

        context = build_context(results)

        messages = build_rag_messages(
            question=user_input,
            context=context,
        )
        messages[1:1] = history

        assistant_reply = generate_response(messages)

        sources = build_sources(results)

        response = {
            "answer": assistant_reply,
            "sources": sources,
        }

        history.append(
            {
                "role": "user",
                "content": user_input,
            }
        )

        history.append(
            {
                "role": "assistant",
                "content": assistant_reply,
            }
        )
        print("Assistant:", response["answer"])
        print("Sources:", response["sources"])
