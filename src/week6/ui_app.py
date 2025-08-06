"""Gradio UI for the SmartEdu AI project."""

import gradio as gr
import requests
import time
from datetime import datetime

API_URL = "http://127.0.0.1:8000/chat"

CUSTOM_CSS = """
:root {
    --primary: #4f46e5;
    --primary-hover: #4338ca;
    --bg-dark: #0f172a;
    --bg-panel: #1e293b;
    --text-main: #f8fafc;
    --text-muted: #94a3b8;
}

body {
    background-color: var(--bg-dark);
    color: var(--text-main);
    font-family: 'Inter', sans-serif;
}

.gradio-container {
    background: transparent !important;
}

.main-container {
    max-width: 1200px;
    margin: 20px auto;
    border-radius: 16px;
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
    background: var(--bg-panel);
    border: 1px solid rgba(255, 255, 255, 0.1);
    overflow: hidden;
}

.header {
    padding: 24px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    background: linear-gradient(90deg, rgba(30,41,59,1) 0%, rgba(15,23,42,1) 100%);
}

.header h1 {
    color: var(--text-main);
    margin: 0;
    font-weight: 700;
    letter-spacing: -0.5px;
}

.header p {
    color: var(--text-muted);
    margin-top: 4px;
}

.sidebar {
    background-color: #111827;
    padding: 20px;
    border-right: 1px solid rgba(255,255,255,0.05);
    height: 100%;
}

.chat-area {
    padding: 20px;
}

/* Chat bubble styling */
.message.user {
    background: #312e81 !important;
    border: 1px solid rgba(79, 70, 229, 0.3) !important;
    border-radius: 12px 12px 0 12px !important;
}

.message.bot {
    background: #1e293b !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    border-radius: 12px 12px 12px 0 !important;
}

button.primary {
    background: var(--primary) !important;
    border-color: var(--primary) !important;
    transition: all 0.2s ease;
}

button.primary:hover {
    background: var(--primary-hover) !important;
    transform: translateY(-1px);
}

.activity-log {
    font-family: monospace;
    font-size: 0.85em;
    color: #64748b;
    background: #0f172a;
    padding: 10px;
    border-radius: 8px;
    max-height: 200px;
    overflow-y: auto;
}
"""

def chat_fn(message, history, filters, difficulty):
    # Simulate a tiny delay for loading skeleton effect
    time.sleep(0.5)
    
    # Notify user (Toast notification)
    gr.Info(f"Processing query: {message[:20]}...")
    
    try:
        # In a real scenario, you'd pass filters to the backend
        response = requests.post(API_URL, json={"message": message, "difficulty": difficulty}, timeout=90)
        response.raise_for_status()
        bot_response = response.json()["answer"]
        
        # Log activity
        log_entry = f"[{datetime.now().strftime('%H:%M:%S')}] User queried backend.\n"
        
        return bot_response, log_entry
        
    except requests.RequestException as exc:
        gr.Warning("Backend unreachable!")
        return f"Error connecting to backend: {exc}", f"[{datetime.now().strftime('%H:%M:%S')}] API Error.\n"

with gr.Blocks(css=CUSTOM_CSS, theme=gr.themes.Base()) as demo:
    
    # State for activity log
    activity_state = gr.State("System initialized.\n")
    
    with gr.Column(elem_classes=["main-container"]):
        with gr.Row(elem_classes=["header"]):
            with gr.Column():
                gr.Markdown("# 🧠 SmartEdu AI")
                gr.Markdown("Your intelligent learning assistant for Math & Programming.")
                
        with gr.Row():
            # Left Sidebar
            with gr.Column(scale=1, elem_classes=["sidebar"]):
                gr.Markdown("### ⚙️ Settings & Filters")
                
                subject_filter = gr.Dropdown(
                    choices=["All", "Mathematics", "Programming", "General Data"],
                    value="All",
                    label="Knowledge Domain",
                    interactive=True
                )
                
                difficulty_filter = gr.Radio(
                    choices=["Beginner", "Intermediate", "Advanced"],
                    value="Beginner",
                    label="Response Complexity"
                )
                
                gr.Markdown("### 📝 Activity Log")
                log_box = gr.Markdown("System initialized.", elem_classes=["activity-log"])
                
            # Right Chat Area
            with gr.Column(scale=3, elem_classes=["chat-area"]):
                chatbot = gr.Chatbot(height=500, avatar_images=(None, "🧠"))
                
                with gr.Row():
                    msg = gr.Textbox(
                        show_label=False,
                        placeholder="Ask me anything about Python or Math...",
                        scale=8,
                        container=False
                    )
                    submit_btn = gr.Button("Send", variant="primary", scale=1)
                
                gr.Examples(
                    examples=[
                        "What is a Python dictionary?",
                        "Can you explain the Pythagorean theorem?",
                        "How do I write a recursive function?"
                    ],
                    inputs=msg
                )
                
        def update_chat(user_msg, chat_history, subj_filter):
            chat_history.append({"role": "user", "content": user_msg})
            return "", chat_history
            
        def generate_response(chat_history, subj_filter, diff_filter, act_state):
            print(f"DEBUG chat_history[-1]: {repr(chat_history[-1])}")
            if isinstance(chat_history[-1], dict):
                user_msg = chat_history[-1]["content"]
            else:
                # In case it's an object like ChatMessage
                user_msg = getattr(chat_history[-1], "content", str(chat_history[-1]))
            
            print(f"DEBUG extracted user_msg: {repr(user_msg)} of type {type(user_msg)}")
            bot_msg, new_log = chat_fn(str(user_msg), chat_history, subj_filter, diff_filter)
            chat_history.append({"role": "assistant", "content": bot_msg})
            updated_log = new_log + act_state
            return chat_history, updated_log, updated_log
            
        submit_event = msg.submit(
            update_chat, [msg, chatbot, subject_filter], [msg, chatbot], queue=False
        ).then(
            generate_response, [chatbot, subject_filter, difficulty_filter, activity_state], [chatbot, activity_state, log_box]
        )
        
        submit_btn.click(
            update_chat, [msg, chatbot, subject_filter], [msg, chatbot], queue=False
        ).then(
            generate_response, [chatbot, subject_filter, difficulty_filter, activity_state], [chatbot, activity_state, log_box]
        )

if __name__ == "__main__":
    demo.launch()
