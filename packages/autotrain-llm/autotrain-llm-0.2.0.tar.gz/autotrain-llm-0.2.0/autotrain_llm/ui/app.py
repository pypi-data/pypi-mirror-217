import gradio as gr
from autotrain_llm.utils import SUPPORTED_MODELS


def main():
    with gr.Blocks() as demo:
        with gr.Row():
            hub_model = gr.Dropdown(
                label="Model",
                value=SUPPORTED_MODELS[0],
                choices=SUPPORTED_MODELS,
                interactive=True,
            )
            _ = gr.Markdown("")
            _ = gr.Markdown("")
    return demo
