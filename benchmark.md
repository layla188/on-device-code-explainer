# Benchmark — On-Device Code Explainer

## 1. Experiment Goal

The goal of this experiment was to test the idea of running a coding LLM **locally on my laptop** using Ollama.

This benchmark was mainly conducted to verify that:

* The model can run successfully on-device.
* A Python application can communicate with the local model.
* The local inference speed is practical for experimentation.
* The local model can produce meaningful code explanations.

> **Important:** This is not intended to be a detailed model-quality benchmark or a comparison for production use. The main objective is to understand and demonstrate the local-inference workflow.

---

## 2. Setup

| Item            | Value                       |
| --------------- | --------------------------- |
| Local model     | Qwen2.5-Coder 0.5B          |
| Runtime         | Ollama                      |
| Inference       | Local / On-device           |
| API interface   | OpenAI-compatible API       |
| Local endpoint  | `http://localhost:11434/v1` |
| Target hardware | Laptop with 16 GB RAM       |

The model was selected because it is small enough for local experimentation and is intended for coding-related tasks.

---

## 3. Application Flow

The local benchmark used the following setup:

```text
Python Application
        ↓
OpenAI Python Client
        ↓
localhost:11434
        ↓
Ollama
        ↓
Qwen2.5-Coder 0.5B
        ↓
Generated Explanation
```

This demonstrates that the OpenAI Python client can be used with a local OpenAI-compatible endpoint by changing the `base_url`.

---

## 4. Test Cases

Five simple Python examples were used:

### Test 1 — Basic Function

```python
def add(a, b):
    return a + b
```

### Test 2 — Loop

```python
for i in range(5):
    print(i)
```

### Test 3 — Recursion

```python
def factorial(n):
    if n == 0:
        return 1
    return n * factorial(n - 1)
```

### Test 4 — Buggy Code

```python
numbers = [1, 2, 3]
print(numbers[3])
```

### Test 5 — Counting Vowels

```python
def count_vowels(text):
    vowels = "aeiou"
    return sum(1 for char in text.lower() if char in vowels)
```

---

## 5. Performance Results

| Test           | Response Time | Output Tokens | Tokens/sec |
| -------------- | ------------: | ------------: | ---------: |
| Basic function |       12.62 s |           220 |      17.43 |
| Loop           |       12.82 s |           396 |      30.90 |
| Recursion      |       18.80 s |           591 |      31.43 |
| Buggy code     |        7.20 s |           222 |      30.83 |
| Count vowels   |        9.56 s |           295 |      30.85 |

### Average generation speed

**28.29 tokens/sec**

The generation speed varied between test cases because the model produced different amounts of output.

---

## 6. Basic Quality Observation

The model was able to explain basic concepts such as:

* Function definitions
* Arithmetic operations
* Loops
* Recursion
* Generator expressions
* String processing

However, several outputs contained unsupported assumptions.

For example, the model sometimes described example function calls or execution scenarios that were not actually included in the input code.

The buggy-code test was particularly useful because the model did not correctly identify the indexing problem in:

```python
numbers[3]
```

for a list containing only three elements.

These observations show that the selected 0.5B model has limitations in explanation reliability.

---

## 7. Interpretation

The results demonstrate that the local model is capable of running successfully on the laptop and generating responses at an average measured speed of **28.29 tokens/sec**.

However, the experiment does **not** claim that the model is highly accurate or production-ready.

The main purpose was to answer a practical question:

> Can I run a small coding LLM locally and integrate it into a working Python application?

The answer from this experiment is **yes**.

---

## 8. Local Inference vs Hosted Inference

The application also supports a hosted OpenRouter backend.

The two modes use the same application structure:

```text
Local:
Python
 ↓
OpenAI Client
 ↓
Ollama
 ↓
Local Model
```

and:

```text
Hosted:
Python
 ↓
OpenAI Client
 ↓
OpenRouter
 ↓
Hosted Model
```

The main change is the configured endpoint and model backend.

The hosted and local tests in this project are **not a controlled same-model comparison**, because the hosted configuration uses a hosted model endpoint while the local benchmark uses Qwen2.5-Coder 0.5B.

Therefore, the benchmark should not be interpreted as a direct measurement of "local vs hosted performance for the same model."

---

## 9. Final Observation

The experiment successfully demonstrated local LLM inference using:

```text
Qwen2.5-Coder 0.5B
+
Ollama
+
OpenAI-compatible Python client
```

The measured average generation speed was:

```text
28.29 tokens/sec
```

The response-quality tests also showed that a small local model can have noticeable limitations, especially when it needs to stay strictly grounded in the provided code.

For this project, that limitation is acceptable because the primary goal was to **experiment with and understand local inference**, not to build a production-grade code-explanation system.

A larger or more capable model could be evaluated later if response quality becomes the primary requirement.
