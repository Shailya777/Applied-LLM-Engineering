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

def extract_text(content):
    """
    Gradio 6+ wraps message content in a list of dictionaries for multimodal support:
    [{"type": "text", "text": "Hello"}]
    This function safely extracts the string.
    """
    if isinstance(content, list):
        # Extract text from all text blocks
        return " ".join([block["text"] for block in content if block.get("type") == "text"])
    return content

def chat(history):
    """
    Manages a single chat turn by extracting the latest user query, generating an AI response using retrieved context, and updating the conversation history.

    Args:
    history (list[dict]): A list of dictionaries representing the ongoing conversation.

    Returns:
    tuple[list[dict], str]: A tuple containing the updated history list with the new assistant response and a formatted HTML string of the retrieved source documents.
    """
    raw_last_content = history[-1]["content"]
    last_message = extract_text(raw_last_content)

    # Rebuild prior history so 'content' is strictly a string, which answer.py expects
    prior = []
    for msg in history[:-1]:
        prior.append({
            "role": msg["role"],
            "content": extract_text(msg["content"])
        })

    # Generate the response via Langchain
    answer, context = answer_question(last_message, prior)

    # Append the assistant's response.
    history.append({"role": "assistant", "content": answer})
    return history, format_context(context)

def main():
    def put_message_in_chatbot(message, history):
        # Append the user's input as a dictionary
        return "", history + [{"role": "user", "content": message}]

    theme = gr.themes.Soft(font=["Inter", "system-ui", "sans-serif"])

    with gr.Blocks(title="Insurellm Expert Assistant") as ui:
        gr.Markdown("# 🏢 Insurellm Expert Assistant\nAsk me anything about Insurellm!")

        with gr.Row():
            with gr.Column(scale=1):
                chatbot = gr.Chatbot(
                    label="💬 Conversation",
                    height=600
                )
                message = gr.Textbox(
                    label="Your Question",
                    placeholder="Ask anything about Insurellm...",
                    show_label=False,
                )

            with gr.Column(scale=1):
                context_markdown = gr.Markdown(
                    label="📚 Retrieved Context",
                    value="*Retrieved context will appear here*",
                    container=True,
                    height=600,
                )

        message.submit(
            put_message_in_chatbot, inputs=[message, chatbot], outputs=[message, chatbot]
        ).then(chat, inputs=chatbot, outputs=[chatbot, context_markdown])

    ui.launch(inbrowser=True, theme= theme)


if __name__ == '__main__':
    main()