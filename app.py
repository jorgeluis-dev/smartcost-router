"""
SmartCost Router - Main Interface
Portfolio MVP
"""

import gradio as gr
from router import route


def process_request(text, output_tokens):
    if not text or not text.strip():
        return "Please enter a request.", "", "", "", "", ""

    result = route(text, int(output_tokens))

    summary = f"""
### System Decision

**Selected Model:** {result['selected_model']}  
**Provider:** {result['provider']}  
**Difficulty Level:** {result['level'].upper()}

**Reason:** {result['reason']}

---

**Input Tokens:** {result['input_tokens']}  
**Estimated Output Tokens:** {result['estimated_output_tokens']}

**Estimated Cost:**
- Input: US$ {result['input_cost_usd']:.6f}
- Output: US$ {result['output_cost_usd']:.6f}
- **Total: US$ {result['total_cost_usd']:.6f}**
"""

    return (
        summary,
        result["selected_model"],
        result["level"].upper(),
        str(result["input_tokens"]),
        f"US$ {result['total_cost_usd']:.6f}",
        result["reason"]
    )


# ===== Gradio Interface =====
with gr.Blocks(
    title="SmartCost Router",
    theme=gr.themes.Soft()
) as demo:

    gr.Markdown(
        """
        # SmartCost Router
        ### Intelligent LLM selection system focused on cost-efficiency
        
        Type what you need. The system analyzes complexity and automatically selects 
        the most suitable model (cheap × balanced × powerful).
        """
    )

    with gr.Row():
        with gr.Column(scale=2):
            user_input = gr.Textbox(
                label="What do you need?",
                placeholder="Example: Summarize this text... or Analyze deeply the architecture of this system...",
                lines=5
            )
            output_tokens = gr.Slider(
                minimum=100,
                maximum=2000,
                value=400,
                step=50,
                label="Estimated output tokens (expected response length)"
            )
            submit_btn = gr.Button("Analyze and Select Model", variant="primary")

        with gr.Column(scale=1):
            selected_model = gr.Textbox(label="Selected Model")
            difficulty = gr.Textbox(label="Difficulty Level")
            tokens = gr.Textbox(label="Input Tokens")
            total_cost = gr.Textbox(label="Estimated Total Cost")

    reason = gr.Textbox(label="Decision Reason", lines=2)
    full_result = gr.Markdown(label="Details")

    submit_btn.click(
        fn=process_request,
        inputs=[user_input, output_tokens],
        outputs=[full_result, selected_model, difficulty, tokens, total_cost, reason]
    )

    gr.Markdown(
        """
        ---
        **SmartCost Router** · Portfolio MVP  
        Demonstrates intelligent model routing focused on cost optimization.
        """
    )


if __name__ == "__main__":
    demo.launch()