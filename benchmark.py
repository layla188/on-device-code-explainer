import time

from openai import OpenAI

from config import LOCAL_BASE_URL, LOCAL_MODEL


# ---------------------------------
# Local Ollama client
# ---------------------------------

client = OpenAI(
    base_url=LOCAL_BASE_URL,
    api_key="ollama",
)


SYSTEM_PROMPT = """
You are a code explanation assistant.

Explain the provided code clearly and accurately.

Focus on:
1. What the code does.
2. Important parts of the code.
3. How the code executes.
4. Important programming concepts.

Do not invent behavior that is not present in the code.
"""


TEST_CASES = {
    "basic_function": """
def add(a, b):
    return a + b
""",

    "loop": """
for i in range(5):
    print(i)
""",

    "recursion": """
def factorial(n):
    if n == 0:
        return 1
    return n * factorial(n - 1)
""",

    "buggy_code": """
numbers = [1, 2, 3]
print(numbers[3])
""",

    "count_vowels": """
def count_vowels(text):
    vowels = "aeiou"
    return sum(1 for char in text.lower() if char in vowels)
""",
}


def run_test(test_name: str, code: str):
    print("=" * 70)
    print(f"TEST: {test_name}")
    print("=" * 70)

    start_time = time.perf_counter()

    response = client.chat.completions.create(
        model=LOCAL_MODEL,
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

    end_time = time.perf_counter()

    elapsed_time = end_time - start_time
    explanation = response.choices[0].message.content or ""

    print(explanation)
    print("\nTime:", round(elapsed_time, 2), "seconds")

    # OpenAI-compatible servers may provide usage information.
    completion_tokens = None

    if getattr(response, "usage", None):
        completion_tokens = getattr(
            response.usage,
            "completion_tokens",
            None,
        )

    if completion_tokens:
        tokens_per_second = completion_tokens / elapsed_time

        print("Output tokens:", completion_tokens)
        print("Tokens/sec:", round(tokens_per_second, 2))

    else:
        print("Output tokens: not provided by this endpoint")
        print("Tokens/sec: not available from usage data")

    print()

    return {
        "test": test_name,
        "time": elapsed_time,
        "completion_tokens": completion_tokens,
        "tokens_per_second": (
            completion_tokens / elapsed_time
            if completion_tokens
            else None
        ),
        "explanation": explanation,
    }


def main():
    print("=" * 70)
    print("QWEN 2.5 CODER - LOCAL BENCHMARK")
    print("=" * 70)
    print("Model:", LOCAL_MODEL)
    print()

    results = []

    for test_name, code in TEST_CASES.items():
        result = run_test(test_name, code)
        results.append(result)

    print("\n" + "=" * 70)
    print("BENCHMARK SUMMARY")
    print("=" * 70)

    valid_speeds = [
        r["tokens_per_second"]
        for r in results
        if r["tokens_per_second"] is not None
    ]

    for result in results:
        print(
            f'{result["test"]}: '
            f'{result["time"]:.2f}s'
        )

    if valid_speeds:
        average_speed = sum(valid_speeds) / len(valid_speeds)

        print(
            "\nAverage generation speed:",
            round(average_speed, 2),
            "tokens/sec",
        )
    else:
        print(
            "\nAverage generation speed: "
            "not available from response usage"
        )


if __name__ == "__main__":
    main()