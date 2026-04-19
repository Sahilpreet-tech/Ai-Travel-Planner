import os

from dotenv import load_dotenv
from groq import Groq

load_dotenv()

SYSTEM_TRAVEL = (
    "You are WANDERLUX, a world-class travel planner. "
    "Reply with clear **markdown**: use ### for day titles, bullet lists for activities, "
    "and short notes on food and transport when helpful. Match the user's budget honestly."
)

SYSTEM_CONCIERGE = (
    "You are WANDERLUX, a friendly luxury travel concierge. "
    "Help with destinations, flights ideas, packing, etiquette, and itinerary tweaks. "
    "Use **markdown** with short sections. If the user has not said where they are going, ask one clarifying question."
)


def _client():
    key = os.getenv("GROQ_API_KEY")
    if not key:
        return None
    return Groq(api_key=key)


def generate_travel_plan(destination: str, days: int, budget: str) -> str:
    """Build a day-by-day itinerary from destination, duration, and budget tier."""
    client = _client()
    if client is None:
        return (
            "**Setup required:** add your Groq API key.\n\n"
            "1. Create a free key at [console.groq.com](https://console.groq.com/)\n"
            "2. In the project folder, create a `.env` file with:\n"
            "`GROQ_API_KEY=your_key_here`\n"
            "3. Restart Streamlit."
        )

    prompt = (
        f"Create a detailed **{days}-day** itinerary for **{destination}**.\n\n"
        f"**Budget level:** {budget}\n\n"
        "Requirements:\n"
        "- Day-by-day sections (Day 1, Day 2, …).\n"
        "- Suggest realistic hotels or areas (not necessarily specific brand names unless widely known).\n"
        "- Meals, sights, and one backup activity per day.\n"
        "- Keep transport practical for the budget.\n"
        "- End with **Packing & tips** (3–5 bullets).\n"
    )

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": SYSTEM_TRAVEL},
                {"role": "user", "content": prompt},
            ],
            temperature=0.7,
            max_tokens=4096,
        )
        return response.choices[0].message.content or "(No response text.)"
    except Exception as e:
        return f"**Error:** {e}"


def chat_with_concierge(messages: list[dict]) -> str:
    """Continue a concierge chat; `messages` is OpenAI-style role/content dicts (no system)."""
    client = _client()
    if client is None:
        return (
            "I need a **GROQ_API_KEY** in your `.env` file to chat. "
            "Get a key at console.groq.com and restart the app."
        )

    api_messages = [{"role": "system", "content": SYSTEM_CONCIERGE}] + messages

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=api_messages,
            temperature=0.7,
            max_tokens=2048,
        )
        return response.choices[0].message.content or "(No response text.)"
    except Exception as e:
        return f"**Error:** {e}"
