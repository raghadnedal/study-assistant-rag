from app.rag.retrieval import retrieve_chunks


questions = [
    "What scholarships are available for master's students?",
    "Which scholarships are fully funded?",
    "What opportunities are available in the UK?",
    "Which scholarship provides €34,000?",
    "What scholarships are available for undergraduate students?",
]


for question in questions:
    print("\nQUESTION:", question)

    results = retrieve_chunks(
        question=question,
        top_k=5,
    )

    for result in results:
        print("Distance:", result["distance"])
        print("Page:", result["page_number"])
        print("Text:", result["text"][:250])
        print("-" * 40)
