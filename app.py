from openai import OpenAI

from config import (
    USE_LOCAL,
    LOCAL_MODEL,
    LOCAL_BASE_URL,
    HOSTED_MODEL,
    HOSTED_API_KEY,
    HOSTED_BASE_URL,
)


# ---------------------------------
# System prompt
# ---------------------------------

SYSTEM_PROMPT = """
You are a code explanation assistant.

IMPORTANT RULES:
- Explain ONLY the code provided by the user.
- Do NOT create example inputs or outputs.
- Do NOT assume the code is called or executed unless the call is present.
- Do NOT invent function names, variables, or program behavior.
- If the code contains an error, explicitly identify the error.
- If execution cannot be determined from the provided code alone, say so.
- Quote the relevant line when identifying a problem.

Structure your answer as:
1. What the code does
2. Important lines
3. Execution flow
4. Errors or limitations
"""


# ---------------------------------
# Get client and model
# ---------------------------------

def get_model_config(use_local: bool):

    if use_local:

        client = OpenAI(
            base_url=LOCAL_BASE_URL,
            api_key="ollama",
        )

        model_name = LOCAL_MODEL
        mode = "LOCAL"

    else:

        if not HOSTED_API_KEY:
            raise ValueError(
                "OPENROUTER_API_KEY is missing from the .env file."
            )

        client = OpenAI(
            api_key=HOSTED_API_KEY,
            base_url=HOSTED_BASE_URL,
        )

        model_name = HOSTED_MODEL
        mode = "HOSTED"

    return client, model_name, mode


# ---------------------------------
# Code explanation function
# ---------------------------------

def explain_code(code: str, use_local: bool = True) -> str:

    client, model_name, mode = get_model_config(use_local)

    response = client.chat.completions.create(
        model=model_name,
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": f"Explain this code:\n\n{code}",
            },
        ],
        temperature=0.2,
    )

    return response.choices[0].message.content


# ---------------------------------
# Main application
# ---------------------------------

def main():

    print("=" * 60)
    print("       ON-DEVICE CODE EXPLAINER")
    print("=" * 60)

    client, model_name, mode = get_model_config(USE_LOCAL)

    print(f"\nMode: {mode}")
    print(f"Model: {model_name}")

    print("\nPaste your Python code below.")
    print("When you finish, type END on a new line.\n")

    lines = []

    while True:

        line = input()

        if line.strip() == "END":
            break

        lines.append(line)

    code = "\n".join(lines).strip()

    if not code:
        print("\nNo code was provided.")
        return

    print("\nGenerating explanation...\n")

    try:

        explanation = explain_code(
            code,
            use_local=USE_LOCAL,
        )

        print("-" * 60)
        print("EXPLANATION")
        print("-" * 60)
        print(explanation)
        print("-" * 60)

    except Exception as e:

        print("\nError while calling the model:")
        print(e)


if __name__ == "__main__":
    main()