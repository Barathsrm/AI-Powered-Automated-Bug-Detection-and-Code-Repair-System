"""
Wraps calls to the Anthropic API to generate a patch for a given error +
code context. Kept separate from patch_service.py so the loop-control
logic (attempts, token budget) stays independent of the prompt/response
handling.
"""
import os
import anthropic

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

SYSTEM_PROMPT = (
    "You are a careful code-repair assistant. Given a failing test's error "
    "and the relevant source files, propose the smallest possible fix. "
    "Respond only with a unified diff and a one-paragraph explanation."
)


def generate_patch(error: dict, file_contents: dict[str, str]) -> dict:
    context = "\n\n".join(
        f"--- {path} ---\n{content}" for path, content in file_contents.items()
    )
    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=2000,
        system=SYSTEM_PROMPT,
        messages=[
            {
                "role": "user",
                "content": f"Error:\n{error['raw']}\n\nRelevant files:\n{context}",
            }
        ],
    )
    text = "".join(block.text for block in message.content if block.type == "text")
    tokens_used = message.usage.input_tokens + message.usage.output_tokens

    return {"raw_response": text, "tokens_used": tokens_used}
