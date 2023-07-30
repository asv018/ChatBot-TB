import textbase
from textbase.message import Message
from textbase import models
import os
from typing import List

# Load your OpenAI API key
models.OpenAI.api_key = "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"
# or from environment variable:
# models.OpenAI.api_key = os.getenv("OPENAI_API_KEY")

# Initial prompt for GPT-3.5 Turbo to start the conversation
INITIAL_PROMPT = """Hello! I am your mental health support chatbot. How are you feeling today? Please share your thoughts and emotions with me, and I'll do my best to provide guidance and support.
"""

@textbase.chatbot("talking-bot")
def on_message(message_history: List[Message], state: dict = None):
    """Your chatbot logic here
    message_history: List of user messages
    state: A dictionary to store any stateful information

    Return a string with the bot_response or a tuple of (bot_response: str, new_state: dict)
    """

    if state is None or "counter" not in state:
        state = {"counter": 0}
    else:
        state["counter"] += 1

    # If this is the first interaction, use the initial prompt
    if len(message_history) == 0:
        bot_response = INITIAL_PROMPT
    else:
        # Generate GPT-3.5 Turbo response based on the user's message
        response_object = models.OpenAI.generate(
            system_prompt=message_history[-1].content,  # Use the last user message as the prompt
            message_history=message_history,
            model="gpt-3.5-turbo",
        )
        # Extract the actual text from the response object
        bot_response = response_object['choices'][0]['message']['content']

    # Add a question at the end of the response
    bot_response += "\n\nHow can I assist you further?"

    return bot_response, state
