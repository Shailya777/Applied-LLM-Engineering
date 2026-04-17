import gradio as gr
from dotenv import load_dotenv
from rag_implementation_simplified.answer import answer_question
load_dotenv()

def format_context(context):
    """
    Converts a list of retrieved documents into a formatted HTML string for display, highlighting the source metadata and page content.

    Args:
    context (list): A list of Document objects containing metadata and text content.

    Returns:
    str: An HTML-formatted string featuring styled headers and source labels for each context fragment.
    """

    result = "<h2 style='color: #ff7800;'>Relevant Context</h2>\n\n"

    for doc in context:
        result += f"<span style='color: #ff7800;'>Source: {doc.metadata['source']}</span>\n\n"
        result += doc.page_content + "\n\n"
    return result

def chat(history):
    """
    Manages a single chat turn by extracting the latest user query, generating an AI response using retrieved context, and updating the conversation history.

    Args:
    history (list[dict]): A list of dictionaries representing the ongoing conversation.

    Returns:
    tuple[list[dict], str]: A tuple containing the updated history list with the new assistant response and a formatted HTML string of the retrieved source documents.
    """
    last_message = history[-1]['content']
    prior = history[:-1]
    answer, context = answer_question(last_message, prior)
    history.append({'role': 'assistant', 'content': answer})
    return history, format_context(context)

def main():

    def put_message_in_chatbot(message, history):
        return "", history + [{'role': 'user', 'content': message}]

    theme= gr.themes.Ocean(font=["Inter", "system-ui", "sans-serif"])

    with gr.Blocks(title= "Insurellm Expert Assistant") as ui:
        gr.Markdown("# 🏢 Insurellm Expert Assistant\nAsk me anything about Insurellm!")

        with gr.Row():
            with gr.Column(scale= 1):
                chatbot = gr.Chatbot(
                    label= "💬 Conversation", height=600, show_copy_button=True
                )
                message = gr.Textbox(
                    label= 'Your Question',
                    placeholder= 'Ask anything about Insurellm...',
                    show_label= False
                )

            with gr.Column(scale= 1):
                context_markdown = gr.Markdown(
                    label= '📚 Retrieved Context',
                    value= '*Retrieved context will appear here*',
                    container= True,
                    height= 600
                )

        message.submit(
            put_message_in_chatbot, inputs= [message, chatbot], outputs= [message, chatbot]
        ).then(chat, inputs= chatbot, outputs= [chatbot, context_markdown])

    ui.launch(theme= theme, inbrowser= True)