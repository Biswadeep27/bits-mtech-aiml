from fastapi import FastAPI
import gradio as gr
import os
from gradio.themes.utils import sizes
from databricks.sdk import WorkspaceClient
from databricks.sdk.service.serving import ChatMessage, ChatMessageRole

app = FastAPI()

# your endpoint will directly be setup with proper permissions when you deploy your app
w = WorkspaceClient()
available_endpoints = [x.name for x in w.serving_endpoints.list()]


def respond(message, history, dropdown):
    if len(message.strip()) == 0:
        return "ERROR the question should not be empty"
    try:
        messages = []
        if history:
            for human, assistant in history:
                messages.append(ChatMessage(content=human, role=ChatMessageRole.USER))
                messages.append(
                    ChatMessage(content=assistant, role=ChatMessageRole.ASSISTANT)
                )
        messages.append(ChatMessage(content=message, role=ChatMessageRole.USER))
        response = w.serving_endpoints.query(
            name=dropdown,
            messages=messages,
            temperature=1.0,
            stream=False,
        )
    except Exception as error:
        return f"ERROR requesting endpoint {dropdown}: {error}"
    return response.choices[0].message.content


theme = gr.themes.Soft(
    text_size=sizes.text_sm,
    radius_size=sizes.radius_sm,
    spacing_size=sizes.spacing_sm,
)

demo = gr.ChatInterface(
    respond,
    chatbot=gr.Chatbot(
        show_label=False, container=False, show_copy_button=True, bubble_full_width=True
    ),
    textbox=gr.Textbox(placeholder="What is Snowflake SQL?", container=False, scale=7),
    title="QueryMorph App - Chat with your SQL Generator assistant",
    description="This chatbot is used to create source SQLs that are fed to QueryMorph Validation Framework. <br>It answers with the help of All the EDW Source Documentation saved in a Knowledge database.<br/>It is using Meta llma 3.3. Model Eveluation is enabled for this App.",
    examples=[
        ["Give me 5 Snowflake queries with date functions."],
        ["Give me 5 Redshift queris with with clause."],
        ["Give me 10 Snowflake queries that have complex joins in them."],
    ],
    cache_examples=False,
    theme=theme,
    retry_btn=None,
    undo_btn=None,
    clear_btn="Clear",
    additional_inputs=gr.Dropdown(
        choices=available_endpoints,
        value=os.environ["MODEL_SERVING_ENDPOINT"],
        label="Serving Endpoint",
    ),
    additional_inputs_accordion="Settings",
)

demo.queue(default_concurrency_limit=100)
app = gr.mount_gradio_app(app, demo, path="/")
