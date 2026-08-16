# Benchmark — On-Device Code Explainer

## 1. Purpose

This benchmark was conducted as part of the Week 4 **Offline-First AI Tool** project.

The main goal of this project is to test the idea of running an LLM **locally on my laptop** using Ollama, rather than relying entirely on a hosted API.

The benchmark is therefore primarily focused on:

* Verifying that local inference works successfully.
* Measuring the local model's generation speed.
* Understanding the practical experience of running an LLM on-device.
* Confirming that the application can communicate with a locally hosted model through an OpenAI-compatible API.

**The quality evaluation in this benchmark is only a basic sanity check. It is not intended to prove that the selected model provides high-quality or production-ready code explanations.**

The project is mainly demonstrating the **local-LLM concept and deployment approach**.

---

## 2. Model and Runtime

| Item            | Value                       |
| --------------- | --------------------------- |
| Model           | Qwen2.5-Coder 0.5B          |
| Runtime         | Ollama                      |
| Inference       | Local / On-device           |
| API interface   | OpenAI-compatible API       |
| Local endpoint  | `http://localhost:11434/v1` |
| Target hardware | Laptop with 16 GB RAM       |

The model was selected because it is small enough for local experimentation and is specifically designed for coding-related tasks.

---

## 3. Benchmark Setup

The application sends code to the local model through the OpenAI Python client.

The flow is:

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
Code Explanation
```

Five simple test cases were used:

1. Basic function
2. Loop
3. Recursion
4. Buggy code
5. Counting vowels

The tests were selected to check whether the local model could handle different basic programming constructs.

---

## 4. Performance Results

| Test           | Response Time | Output Tokens | Tokens/sec |
| -------------- | ------------: | ------------: | ---------: |
| Basic function |       12.62 s |           220 |      17.43 |
| Loop           |       12.82 s |           396 |      30.90 |
| Recursion      |       18.80 s |           591 |      31.43 |
| Buggy code     |        7.20 s |           222 |      30.83 |
| Count vowels   |        9.56 s |           295 |      30.85 |

### Average generation speed

**28.29 tokens/sec**

The results show that the model can perform local inference at a usable speed on the tested laptop.

Response time varies between inputs because the model generates different numbers of output tokens for different explanations.

---

## 5. Basic Quality Observation

The generated explanations were reviewed only as a basic sanity check to confirm that the model was producing meaningful responses.

The model was able to explain several basic programming concepts, including:

* Functions
* Loops
* Recursion
* Generator expressions
* Basic list operations

However, some outputs contained incorrect assumptions or invented execution examples. For example, the model sometimes described function calls that were not actually present in the input code, and it failed to correctly identify the error in the `numbers[3]` test case.

These observations show that the model has limitations in code-explanation reliability.

**These limitations are documented for transparency, but improving response quality is not the primary objective of this experiment.**

---

## 6. Conclusion

The experiment successfully demonstrated the main objective of the project:

> A small open-source coding model can be downloaded and executed locally on a laptop using Ollama, and a Python application can interact with it through an OpenAI-compatible API.

The measured average generation speed was **28.29 tokens/sec** for the selected test cases.

The experiment also demonstrated an important Week 4 concept: the application can use a local model without sending the code to a remote inference provider.

For this project, the primary focus is therefore **proving and understanding local inference**, rather than achieving the highest possible model quality.

The model's response-quality limitations are acknowledged, and a larger or more capable model could be considered in a future experiment if higher explanation accuracy becomes a requirement.