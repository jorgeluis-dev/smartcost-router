# SmartCost Router

**Intelligent LLM Routing System focused on Cost-Efficiency**

SmartCost Router analyzes a user request, detects the complexity of the task, and automatically selects the most suitable language model.  
The goal is simple: use the cheapest model that can still deliver good quality.

---

## Problem

Companies often use expensive AI models for simple tasks.  
This creates unnecessary costs.

SmartCost Router solves this by choosing the right model for each request.

---

## How It Works

1. The user types a request
2. The system classifies the difficulty (Easy / Medium / Hard)
3. It selects the best model:
   - **Easy** → Cheap models (fast and low cost)
   - **Medium** → Balanced models (good quality and reasonable cost)
   - **Hard** → Strong models (high quality for complex tasks)
4. The system shows:
   - Selected model
   - Reason for the choice
   - Estimated tokens
   - Estimated cost

---

## Features (MVP)

- Automatic task complexity detection
- Intelligent model routing
- Token counting
- Cost estimation
- Clean web interface (Gradio)
- Easy configuration of models and prices
- Ready for deployment on Hugging Face Spaces

---

## Project Structure

```text
project/
├── app.py              # Web interface
├── router.py           # Core logic (classification + routing)
├── models_config.py    # Models and pricing
├── requirements.txt    # Dependencies
├── .gitignore
└── README.md
```

## Tech Stack

- Python 3.10+
- Gradio
- Tiktoken
- Custom routing logic

## How to Run

```bash
pip install -r requirements.txt
python app.py
```

## Why This Project Matters

- How tokens and AI costs work
- How to design a practical AI product
- How to optimize cost without losing quality
- How to deliver a clean and usable MVP

## Future Improvements

- Connect real APIs (OpenAI, Anthropic, Hugging Face)
- Use a small model to classify difficulty more accurately
- Add history of decisions and cost savings
- Create a simple dashboard for companies

