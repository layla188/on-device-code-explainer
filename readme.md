# On-Device Code Explainer

A small AI application that explains Python code using a locally running open-source language model.

This project was built as part of **Week 4 — Local LLMs & Open-Source Tooling** of the Helwan Career Center AI Engineering Roadmap.

The main purpose of this project is to explore and demonstrate **local LLM inference** using Ollama and an OpenAI-compatible API.

> **Note:** The project focuses primarily on understanding and demonstrating the local-inference workflow. The selected small model is not intended to provide production-level code explanation quality.

---

## Project Idea

The application accepts a piece of Python code and asks an LLM to explain it in a beginner-friendly way.

Example:

```python
def factorial(n):
    if n == 0:
        return 1
    return n * factorial(n - 1)
```

The model then generates a natural-language explanation of the code.

---

## Architecture

The project supports both local and hosted inference.

### Local mode

```text
User
 ↓
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
Explanation
```

### Hosted mode

```text
User
 ↓
Python Application
 ↓
OpenAI Python Client
 ↓
OpenRouter API
 ↓
Hosted Model
 ↓
Explanation
```

The same application can switch between the two modes using a single configuration flag.

---

## Project Structure

```text
on-device-code-explainer/
│
├── app.py
├── config.py
├── benchmark.py
├── benchmark.md
├── README.md
├── .env
└── .gitignore
```

### `app.py`

Main application.

It:

* accepts Python code from the user,
* sends the code to the selected model,
* and prints the generated explanation.

### `config.py`

Contains the model and connection configuration.

The main switch is:

```python
USE_LOCAL = True
```

Set it to:

```python
USE_LOCAL = True
```

to use Ollama locally.

Set it to:

```python
USE_LOCAL = False
```

to use the hosted OpenRouter backend.

### `benchmark.py`

Runs a small benchmark on the local model and measures response time and generation speed.

### `benchmark.md`

Contains the benchmark results, observations, model information, and limitations.

---

## Technologies Used

* Python
* Ollama
* Qwen2.5-Coder 0.5B
* OpenAI Python client
* OpenRouter
* python-dotenv

---

## Local Model

### Qwen2.5-Coder 0.5B

The local model used in this project is:

```text
Model: Qwen2.5-Coder 0.5B
Runtime: Ollama
Inference: Local / On-device
```

The model was selected because it is small enough for local experimentation on a laptop while being designed for coding-related tasks.

---

## Installation

### 1. Install Ollama

Install Ollama and verify that it is available from the terminal:

```powershell
ollama --version
```

### 2. Pull the model

```powershell
ollama pull qwen2.5-coder:0.5b
```

Verify that it is installed:

```powershell
ollama list
```

### 3. Install Python dependencies

```powershell
pip install openai python-dotenv
```

---

## Environment Variables

Create a `.env` file:

```text
OPENROUTER_API_KEY=your_api_key_here
MODEL_NAME=openrouter/free
```

The API key should not be committed to GitHub.

---

## Running the Application

### Local mode

In `config.py`:

```python
USE_LOCAL = True
```

Then run:

```powershell
python app.py
```

The application will use:

```text
localhost:11434 → Ollama → Qwen2.5-Coder 0.5B
```

### Hosted mode

In `config.py`:

```python
USE_LOCAL = False
```

Then run:

```powershell
python app.py
```

The application will use the OpenRouter hosted backend.

---

## Example

After starting the application:

```text
============================================================
       ON-DEVICE CODE EXPLAINER
============================================================

Mode: LOCAL
Model: qwen2.5-coder:0.5b
```

Paste Python code and finish with:

```text
END
```

The model then returns an explanation of the code.

---

## Benchmark

A small benchmark was performed using five test cases:

1. Basic function
2. Loop
3. Recursion
4. Buggy code
5. Counting vowels

### Local benchmark result

```text
Model: Qwen2.5-Coder 0.5B
Runtime: Ollama
Average generation speed: 28.29 tokens/sec
```

The detailed benchmark and observations are available in [`benchmark.md`](benchmark.md).

---

## Quality and Limitations

The quality evaluation in this project is intentionally limited.

The primary objective was to **test and understand local LLM inference**, not to prove that the selected 0.5B model provides production-ready code explanations.

During testing, the model was able to explain several basic programming concepts, but some outputs contained unsupported assumptions or incorrect interpretations.

For example, the model sometimes described example function calls that were not present in the input code and failed to correctly identify an indexing error in one of the test cases.

These observations are treated as model limitations rather than a failure of the local-inference setup.

A larger or more capable model could be evaluated in a future version if higher explanation quality becomes a requirement.

---

## What This Project Demonstrates

This project demonstrates several Week 4 concepts:

### Local inference

An open-source model can run directly on the user's machine through Ollama.

### OpenAI-compatible APIs

The same OpenAI Python client can communicate with different backends by changing the API endpoint.

### Local vs Hosted

The application can switch between:

```text
Local Ollama
```

and:

```text
Hosted OpenRouter
```

through a configuration flag.

### Model and hardware trade-offs

A small quantized model can be practical for local experimentation because it requires significantly fewer resources than larger models.

### Benchmarking

The project measures local generation speed and documents the observed limitations of the selected model.

---

## Key Takeaway

The main result of this project is not that the 0.5B model is the best code-explanation model.

The main result is demonstrating that an AI application can be designed to run **locally and privately**, while keeping the option to switch to a hosted backend when needed.

This is the core idea behind the Week 4 **Offline-First AI Tool** project.