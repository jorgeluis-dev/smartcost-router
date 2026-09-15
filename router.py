"""
router.py
---------
This file contains the main logic of SmartCost Router.

It does 3 important things:
1. Classifies the difficulty of the user request (easy, medium, hard)
2. Estimates the number of tokens
3. Selects the best model and calculates the cost
"""

from models_config import MODELS
import tiktoken


def classify_difficulty(text: str) -> str:
    """
    Classifies the task difficulty.
    Returns: "easy", "medium" or "hard"
    """
    text_lower = text.lower().strip()
    words = text_lower.split()

    # Words that usually mean a hard task
    hard_keywords = [
        "analyze deeply", "deep analysis", "reason step by step",
        "architecture", "optimize", "debug", "complex", "strategy",
        "explain in detail", "compare in depth",
        "create a robust solution", "design an architecture",
        "critically evaluate", "propose deep improvements"
    ]

    # Words that usually mean an easy task
    easy_keywords = [
        "summarize", "translate", "list", "classify", "extract",
        "what is", "define", "correct", "rewrite simply",
        "tell me", "explain simply", "in one sentence", "in a few words"
    ]

    # Decision rules
    if any(keyword in text_lower for keyword in hard_keywords):
        return "hard"

    if any(keyword in text_lower for keyword in easy_keywords) or len(words) < 10:
        return "easy"

    return "medium"


def estimate_tokens(text: str) -> int:
    """
    Counts how many tokens the text has.
    Uses the OpenAI tokenizer (good approximation).
    """
    try:
        encoding = tiktoken.get_encoding("o200k_base")
        return len(encoding.encode(text))
    except Exception:
        # Simple fallback if tiktoken fails
        return max(1, int(len(text.split()) * 1.3))


def calculate_cost(input_tokens: int, output_tokens: int, level: str) -> dict:
    """
    Calculates the estimated cost in US dollars.
    """
    model = MODELS[level]
    input_cost = (input_tokens / 1_000_000) * model["input_price"]
    output_cost = (output_tokens / 1_000_000) * model["output_price"]
    total = input_cost + output_cost

    return {
        "input_cost": round(input_cost, 6),
        "output_cost": round(output_cost, 6),
        "total_cost": round(total, 6)
    }


def route(text: str, estimated_output_tokens: int = 400) -> dict:
    """
    Main function of the router.
    Receives the user text and returns the full decision.
    """
    level = classify_difficulty(text)
    model = MODELS[level]
    input_tokens = estimate_tokens(text)
    costs = calculate_cost(input_tokens, estimated_output_tokens, level)

    return {
        "level": level,
        "selected_model": model["name"],
        "provider": model["provider"],
        "model_description": model["description"],
        "reason": generate_reason(level),
        "input_tokens": input_tokens,
        "estimated_output_tokens": estimated_output_tokens,
        "input_cost_usd": costs["input_cost"],
        "output_cost_usd": costs["output_cost"],
        "total_cost_usd": costs["total_cost"]
    }


def generate_reason(level: str) -> str:
    """
    Returns a simple explanation of why the model was chosen.
    """
    reasons = {
        "easy": "Simple task detected → using the cheapest available model.",
        "medium": "Medium complexity task → selected a balanced cost/quality model.",
        "hard": "Complex task detected → using the highest capability model."
    }
    return reasons.get(level, "Default model selected.")