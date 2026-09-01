import os

from dotenv import load_dotenv
from groq import Groq


load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def generate_response(messages):
    try:
        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=messages,
            temperature=0.3,
            max_tokens=500,
            reasoning_effort="low",
            include_reasoning=False,
        )

        return response.choices[0].message.content

    except Exception as error:
        print("LLM error:", error)
        return "Sorry, I could not generate a response."
