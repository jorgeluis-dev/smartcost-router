"""
Core logic for difficulty classification and model selection.
"""

from models_config import MODELS
import tiktoken


def classify_difficulty(text: str) -> str:
    """
    Classifies the task as: easy | medium | hard
    MVP version based on rules + text length.
    """
    text_lower = text.lower().strip()
    words = text_lower.split()

    # Indicators of hard tasks
    hard_keywords = [
        "analyze deeply", "deep analysis", "reason step by step",
        "architecture", "optimize", "debug", "complex", "strategy",
        "explain in detail", "compare in depth",
        "create a robust solution", "design an architecture",
        "critically evaluate", "propose deep improvements"
    ]

    # Indicators of easy tasks
    easy_keywords = [
        "summarize", "translate", "list", "classify", "extract",
        "what is", "define", "correct", "rewrite simply",
        "tell me", "explain simply"
    ]

    # Decision rules
    if any(keyword in text_lower for keyword in hard_keywords):
        return "hard"

    if any(keyword in text_lower for keyword in easy_keywords) or len(words) < 12:
        return "easy"

    return "medium"


def estimate_tokens(text: str) -> int:
    """Counts tokens using OpenAI tokenizer (good approximation)."""
    try:
        encoding = tiktoken.get_encoding("o200k_base")
        return len(encoding.encode(text))
    except Exception:
        # Simple fallback
        return max(1, int(len(text.split()) * 1.3))


def calculate_cost(input_tokens: int, output_tokens: int, level: str) -> dict:
    """Calculates estimated input + output cost."""
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
    Main router function.
    Receives the text and returns the complete decision.
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
    reasons = {
        "easy": "Simple task detected → using the cheapest available model.",
        "medium": "Medium complexity task → selected a balanced cost/quality model.",
        "hard": "Complex task detected → using the highest capability model."
    }
    return reasons.get(level, "Default model selected.")