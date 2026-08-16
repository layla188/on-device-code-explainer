import gradio as gr

from app import explain_code
from config import LOCAL_MODEL, HOSTED_MODEL


# ---------------------------------
# Explain code from UI
# ---------------------------------

def explain_from_ui(code: str, mode: str):

    if not code or not code.strip():
        return "Please enter some Python code."

    use_local = mode == "Local"

    try:

        explanation = explain_code(
            code,
            use_local=use_local,
        )

        return explanation

    except Exception as e:

        return f"Error while calling the model:\n\n{e}"


# ---------------------------------
# Update model information
# ---------------------------------

def update_model_info(mode: str):

    if mode == "Local":

        return (
            f"### Current Configuration\n"
            f"**Mode:** Local / On-Device  \n"
            f"**Model:** `{LOCAL_MODEL}`  \n"
            f"**Privacy:** Code stays on your device."
        )

    else:

        return (
            f"### Current Configuration\n"
            f"**Mode:** Hosted / OpenRouter  \n"
            f"**Model:** `{HOSTED_MODEL}`  \n"
            f"**Privacy:** Requires an internet connection."
        )


# ---------------------------------
# Gradio Application
# ---------------------------------

with gr.Blocks(
    title="On-Device Code Explainer"
) as demo:

    gr.Markdown(
        """
        # 💻 Code Explainer

        Paste Python code below and choose whether you want
        to explain it using the **local on-device model**
        or a **hosted model**.
        """
    )

    mode_selector = gr.Radio(
        choices=[
            "Local",
            "Hosted",
        ],
        value="Local",
        label="Choose Model Mode",
    )

    model_info = gr.Markdown(
        update_model_info("Local")
    )

    code_input = gr.Code(
        label="Python Code",
        language="python",
        lines=15,
    )

    explain_button = gr.Button(
        "Explain Code",
        variant="primary",
    )

    explanation_output = gr.Markdown(
        label="Explanation"
    )


    # When mode changes
    mode_selector.change(
        fn=update_model_info,
        inputs=mode_selector,
        outputs=model_info,
    )


    # When Explain Code is clicked
    explain_button.click(
        fn=explain_from_ui,
        inputs=[
            code_input,
            mode_selector,
        ],
        outputs=explanation_output,
    )


if __name__ == "__main__":
    demo.launch()