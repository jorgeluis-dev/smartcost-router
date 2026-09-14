"""
Central configuration of models and pricing.
Easily control which models exist and how much they cost.
"""

# Approximate prices in US$ per 1 million tokens (input, output)

MODELS = {
    "easy": {
        "name": "GPT-5.6 Luna",
        "description": "Cheap and fast model for simple tasks",
        "input_price": 0.20,
        "output_price": 1.20,
        "provider": "OpenAI"
    },
    "medium": {
        "name": "Claude Sonnet 5",
        "description": "Good balance between quality and cost",
        "input_price": 3.00,
        "output_price": 15.00,
        "provider": "Anthropic"
    },
    "hard": {
        "name": "Claude Opus 5",
        "description": "Maximum quality for complex tasks",
        "input_price": 5.00,
        "output_price": 25.00,
        "provider": "Anthropic"
    }
}

# Future alternatives (Hugging Face open-source models)
ALTERNATIVE_MODELS = {
    "easy_hf": "mistralai/Mistral-7B-Instruct-v0.3",
    "medium_hf": "meta-llama/Meta-Llama-3-8B-Instruct",
}