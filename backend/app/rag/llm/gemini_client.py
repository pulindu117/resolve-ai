import os
from google import genai
from dotenv import load_dotenv

load_dotenv()


def get_client() -> genai.Client:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not set in environment")
    return genai.Client(api_key=api_key)


def generate_response(
    query: str,
    context: str,
    model: str = "gemini-3.1-flash-lite",
    max_tokens: int = 1024,
) -> str:
    """
    Send a query and retrieved context to Gemini and return the answer.

    We use gemini-3.1-flash-lite for speed and cost during development.
    The model is a parameter so you can swap it without changing this file —
    that's the pluggable LLM provider pattern.
    """
    from app.rag.prompts.prompt_templates import SYSTEM_PROMPT, build_user_prompt

    client = get_client()

    response = client.models.generate_content(
        model=model,
        contents=build_user_prompt(query=query, context=context),
        config=genai.types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            max_output_tokens=max_tokens,
        ),
    )

    return response.text