# On-Device Code Explainer

A lightweight local LLM application for explaining Python code.

This project was built as part of **Week 4 — Local LLMs & Open-Source Tooling** in the Helwan Career Center AI Engineering Roadmap.

The main purpose of this project is to experiment with **running an open-source LLM locally on a laptop** using Ollama and connecting to it from Python through an OpenAI-compatible API.

> **Project focus:** This project is primarily a local-inference experiment. The goal is to understand how a local LLM can be integrated into an application, rather than to achieve production-level code explanation quality.

---

## Project Idea

The application takes Python code as input and asks a language model to explain what the code does in a beginner-friendly way.

For example:

```python
def factorial(n):
    if n == 0:
        return 1
    return n * factorial(n - 1)
```

The model generates a natural-language explanation of the code.

---

## Main Features

* Run a coding LLM locally with **Ollama**
* Explain Python code through a simple application
* Use the **OpenAI Python client** with an OpenAI-compatible local endpoint
* Switch between local and hosted inference using one configuration flag
* Run the application through a **Gradio interface**
* Measure local generation speed
* Document the limitations of the selected small model

---

## Architecture

### Local Mode

```text
User
 ↓
Gradio / Python App
 ↓
OpenAI Python Client
 ↓
http://localhost:11434/v1
 ↓
Ollama
 ↓
Qwen2.5-Coder 0.5B
 ↓
Code Explanation
```

### Hosted Mode

```text
User
 ↓
Gradio / Python App
 ↓
OpenAI Python Client
 ↓
OpenRouter API
 ↓
Hosted Model
 ↓
Code Explanation
```

The application uses the same Python-side interface in both modes. The backend is selected through `config.py`.

---

## Local vs Hosted

| Mode   | Backend    | Model Location  | Internet Required   |
| ------ | ---------- | --------------- | ------------------- |
| Local  | Ollama     | My laptop       | No during inference |
| Hosted | OpenRouter | Remote provider | Yes                 |

The main configuration switch is:

```python
USE_LOCAL = True
```

Use:

```python
USE_LOCAL = True
```

to run the application locally with Ollama.

Use:

```python
USE_LOCAL = False
```

to use the hosted OpenRouter backend.

---

## Model

### Qwen2.5-Coder 0.5B

The local model used in this project is:

```text
Model: Qwen2.5-Coder 0.5B
Runtime: Ollama
Inference: Local / On-device
```

The model was selected because it is small enough for local experimentation and is designed for coding-related tasks.

The project intentionally stays with the 0.5B model rather than downloading a larger model, because the main objective is to explore the local-LLM workflow on the available laptop hardware.

---

## Project Structure

```text
on-device-code-explainer/
│
├── app.py
├── gradio_app.py
├── config.py
├── benchmark.py
├── benchmark.md
├── README.md
├── requirements.txt
├── .gitignore
└── .env
```

### `app.py`

Contains the main code-explanation logic and handles the selected local or hosted backend.

### `gradio_app.py`

Provides a simple browser-based interface for entering Python code and viewing the generated explanation.

### `config.py`

Stores the local and hosted configuration, including:

* local model
* local endpoint
* hosted model
* hosted API endpoint
* API key
* `USE_LOCAL` switch

### `benchmark.py`

Runs a small local benchmark using several code examples and records response time and generation speed.

### `benchmark.md`

Contains the benchmark results, observations, and limitations.

---

## Installation

### 1. Install Ollama

Verify that Ollama is installed:

```powershell
ollama --version
```

### 2. Pull the local model

```powershell
ollama pull qwen2.5-coder:0.5b
```

Verify the model:

```powershell
ollama list
```

### 3. Install Python dependencies

```powershell
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file in the project directory:

```text
OPENROUTER_API_KEY=your_api_key_here
MODEL_NAME=openrouter/free
```

The `.env` file contains secrets and should **not** be committed to GitHub.

---

## Run the CLI Application

Set:

```python
USE_LOCAL = True
```

in `config.py`.

Then run:

```powershell
python app.py
```

The application accepts Python code from the terminal and uses the selected model to generate an explanation.

---

## Run the Gradio Interface

For the browser-based interface:

```powershell
python gradio_app.py
```

Gradio will provide a local URL that can be opened in a browser.

---

## Benchmark

A local benchmark was performed using five simple test cases:

1. Basic function
2. Loop
3. Recursion
4. Buggy code
5. Counting vowels

### Result

```text
Model: Qwen2.5-Coder 0.5B
Runtime: Ollama
Average generation speed: 28.29 tokens/sec
```

The detailed results are available in [`benchmark.md`](benchmark.md).

---

## Quality Observation

The model was able to produce meaningful explanations for several basic programming concepts.

However, the test outputs also showed limitations. In some cases, the model introduced assumptions that were not present in the input code. It also failed to correctly identify an indexing error in one of the test cases.

For this reason, the response-quality results should not be interpreted as a production-quality evaluation.

The main goal of this experiment was to verify and understand **local inference**, not to optimize the quality of the generated explanations.

---

## What I Learned

Through this project, I practiced:

* Running an open-source LLM locally with Ollama
* Calling a local model through an OpenAI-compatible API
* Understanding the role of `base_url` when switching between hosted and local inference
* Separating configuration from application logic
* Switching between local and hosted backends with a configuration flag
* Measuring local model generation speed
* Evaluating practical limitations of a small local model
* Building a simple Gradio interface around an LLM application

---

## Key Takeaway

The main outcome of this project was understanding that an LLM application does not have to depend entirely on a remote API.

A small open-source model can run directly on a laptop, and an existing Python application can communicate with it through a local OpenAI-compatible endpoint.

The project also demonstrates the trade-off between **local accessibility and model capability**: local inference provides control and offline operation, while a small model may have noticeable limitations in response quality.

---

## Future Improvements

Possible future improvements include:

* Testing a larger coding model
* Improving the prompt to reduce unsupported assumptions
* Adding more detailed code-error detection
* Adding additional benchmark cases
* Comparing local and hosted models using the same fixed model
* Adding a more polished Gradio interface

---

## Week 4 Project

This project corresponds to the Week 4 **Offline-First AI Tool** idea from the roadmap: a small application that runs using a local model via Ollama with an optional hosted backend, together with a benchmark and model-choice discussion.
