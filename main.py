import textbase
from textbase.message import Message
from textbase import models
import os
from typing import List

# Load your OpenAI API key
models.OpenAI.api_key = "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"
# or from environment variable:
# models.OpenAI.api_key = os.getenv("OPENAI_API_KEY")

# Prompt for GPT-3.5 Turbo
SYSTEM_PROMPT = """You are a career counselor speaking with a client who is seeking advice on their career path."""

@textbase.chatbot("talking-bot")
def on_message(message_history: List[Message], state: dict = None):
    """Your chatbot logic here
    message_history: List of user messages
    state: A dictionary to store any stateful information

    Return a string with the bot_response or a tuple of (bot_response: str, new_state: dict)
    """
    if not state or "counter" not in state:
        state = {"counter": 0, "conversation": []}

    # Generate GPT-3.5 Turbo response
    if state["counter"] < 15:
        # Ask a question
        prompt = f"{SYSTEM_PROMPT}\n{''.join(state['conversation'])}\nWhat is the next question you ask?"
        bot_response = models.OpenAI.generate(
            system_prompt=prompt,
            message_history=message_history,
            model="gpt-3.5-turbo",
        )
        state["conversation"].append(f"Counselor: {bot_response}\n")
    else:
        # Give career advice
        prompt = f"{SYSTEM_PROMPT}\n{''.join(state['conversation'])}\nWhat career advice do you give?"
        bot_response = models.OpenAI.generate(
            system_prompt=prompt,
            message_history=message_history,
            model="gpt-3.5-turbo",
        )
        state["conversation"].append(f"Counselor: {bot_response}\n")

    state["counter"] += 1

    return bot_response, state
