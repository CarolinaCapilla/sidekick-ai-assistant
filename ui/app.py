import gradio as gr
import os
from sidekick import Sidekick
from sidekick.utils.output_saver import save_conversation_to_markdown


async def setup():
    sidekick = Sidekick()
    await sidekick.setup()
    return sidekick


async def process_message(sidekick, message, success_criteria, history):
    # Initialize sidekick if it's None
    if sidekick is None:
        sidekick = Sidekick()
        await sidekick.setup()
    
    results = await sidekick.run_superstep(message, success_criteria, history)
    
    # Save the conversation to a markdown file
    output_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "outputs")
    saved_file = save_conversation_to_markdown(message, success_criteria, results, output_dir)
    
    # Add a notification about the saved file
    if saved_file:
        # Create a notification message
        notification = {
            "role": "system", 
            "content": f"📝 Conversation saved to: {os.path.basename(saved_file)}"
        }
        results.append(notification)
    
    return results, sidekick


async def reset():
    new_sidekick = Sidekick()
    await new_sidekick.setup()
    return "", "", None, new_sidekick


def free_resources(sidekick):
    print("Cleaning up")
    try:
        if sidekick:
            sidekick.cleanup()
    except Exception as e:
        print(f"Exception during cleanup: {e}")


with gr.Blocks(title="Sidekick", theme=gr.themes.Default(primary_hue="emerald")) as ui:
    gr.Markdown("## Sidekick Personal Co-Worker")
    sidekick = gr.State(delete_callback=free_resources)

    with gr.Row():
        chatbot = gr.Chatbot(label="Sidekick", height=300, type="messages")
    with gr.Group():
        with gr.Row():
            message = gr.Textbox(show_label=False, placeholder="Your request to the Sidekick")
        with gr.Row():
            success_criteria = gr.Textbox(
                show_label=False, placeholder="What are your success critiera?"
            )
    with gr.Row():
        reset_button = gr.Button("Reset", variant="stop")
        go_button = gr.Button("Go!", variant="primary")

    # Make sure to initialize the sidekick when the UI loads
    ui.load(setup, [], [sidekick])
    message.submit(
        process_message, [sidekick, message, success_criteria, chatbot], [chatbot, sidekick]
    )
    success_criteria.submit(
        process_message, [sidekick, message, success_criteria, chatbot], [chatbot, sidekick]
    )
    go_button.click(
        process_message, [sidekick, message, success_criteria, chatbot], [chatbot, sidekick]
    )
    reset_button.click(reset, [], [message, success_criteria, chatbot, sidekick])
