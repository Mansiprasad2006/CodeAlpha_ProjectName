"""
Stylish Rule-Based Chatbot — Streamlit App
============================================
A visually polished, rule-based chatbot built with Streamlit.

Color Palette:
    - Deep Classic Blue   : Primary background / headers
    - Vibrant Turquoise   : Accent buttons, active states, user bubbles
    - Warm Elegant Gold   : Borders, highlights, bot bubble accents

Run with:
    streamlit run app.py
"""

import streamlit as st
import random
import re
from datetime import datetime

# ----------------------------------------------------------------------------
# 1. PAGE CONFIGURATION
# ----------------------------------------------------------------------------
st.set_page_config(
    page_title="Aurora Chat — Rule-Based Bot",
    page_icon="💬",
    layout="centered",
    initial_sidebar_state="expanded",
)

# ----------------------------------------------------------------------------
# 2. COLOR PALETTE CONSTANTS (kept centralized for easy theming)
# ----------------------------------------------------------------------------
DEEP_BLUE = "#0B1F3A"
DEEP_BLUE_LIGHT = "#12294F"
TURQUOISE = "#2DD4BF"
TURQUOISE_DARK = "#14B8A6"
GOLD = "#E8B94B"
GOLD_SOFT = "#F3D98B"
LIGHT_BG = "#F5F7FA"
TEXT_LIGHT = "#F1F5F9"

# ----------------------------------------------------------------------------
# 3. CUSTOM CSS — styles background, headers, chat bubbles, input box, buttons
# ----------------------------------------------------------------------------
st.markdown(
    f"""
    <style>
    /* ---------- Overall App Background ---------- */
    .stApp {{
        background: linear-gradient(180deg, {LIGHT_BG} 0%, #E9EDF3 100%);
    }}

    /* ---------- Sidebar Styling ---------- */
    section[data-testid="stSidebar"] {{
        background: linear-gradient(180deg, {DEEP_BLUE} 0%, {DEEP_BLUE_LIGHT} 100%);
        border-right: 2px solid {GOLD};
    }}
    section[data-testid="stSidebar"] * {{
        color: {TEXT_LIGHT} !important;
    }}

    /* ---------- Chat Header Banner ---------- */
    .chat-header {{
        background: linear-gradient(90deg, {DEEP_BLUE} 0%, {DEEP_BLUE_LIGHT} 100%);
        padding: 22px 28px;
        border-radius: 16px;
        border: 2px solid {GOLD};
        box-shadow: 0 6px 18px rgba(11, 31, 58, 0.35);
        margin-bottom: 20px;
        text-align: center;
    }}
    .chat-header h1 {{
        color: {GOLD} !important;
        margin: 0;
        font-size: 2rem;
        letter-spacing: 1px;
        font-weight: 800;
    }}
    .chat-header p {{
        color: {TURQUOISE} !important;
        margin: 4px 0 0 0;
        font-size: 0.95rem;
        font-weight: 500;
    }}

    /* ---------- Chat Bubble Container ---------- */
    .chat-container {{
        background-color: rgba(255, 255, 255, 0.6);
        border-radius: 18px;
        padding: 18px;
        border: 1px solid {GOLD_SOFT};
        margin-bottom: 16px;
    }}

    /* ---------- User Message Bubble (Turquoise) ---------- */
    .user-bubble {{
        background: linear-gradient(135deg, {TURQUOISE} 0%, {TURQUOISE_DARK} 100%);
        color: #062A28;
        padding: 12px 18px;
        border-radius: 18px 18px 4px 18px;
        max-width: 75%;
        margin: 8px 0 8px auto;
        box-shadow: 0 3px 10px rgba(45, 212, 191, 0.35);
        font-weight: 500;
        text-align: right;
    }}

    /* ---------- Bot Message Bubble (Gold-accented, Deep Blue) ---------- */
    .bot-bubble {{
        background: linear-gradient(135deg, {DEEP_BLUE} 0%, {DEEP_BLUE_LIGHT} 100%);
        color: {TEXT_LIGHT};
        padding: 12px 18px;
        border-radius: 18px 18px 18px 4px;
        max-width: 75%;
        margin: 8px auto 8px 0;
        border-left: 4px solid {GOLD};
        box-shadow: 0 3px 10px rgba(11, 31, 58, 0.3);
        font-weight: 500;
    }}

    .bubble-meta {{
        font-size: 0.7rem;
        opacity: 0.7;
        margin-top: 4px;
    }}

    /* ---------- Text Input Box ---------- */
    .stTextInput input {{
        border: 2px solid {GOLD} !important;
        border-radius: 12px !important;
        padding: 10px 14px !important;
        background-color: #FFFFFF !important;
        color: {DEEP_BLUE} !important;
        font-weight: 500 !important;
    }}
    .stTextInput input:focus {{
        border: 2px solid {TURQUOISE} !important;
        box-shadow: 0 0 0 3px rgba(45, 212, 191, 0.25) !important;
    }}

    /* ---------- Buttons ---------- */
    .stButton button {{
        background: linear-gradient(135deg, {TURQUOISE} 0%, {TURQUOISE_DARK} 100%);
        color: #062A28;
        border: 2px solid {GOLD};
        border-radius: 12px;
        font-weight: 700;
        padding: 8px 20px;
        transition: all 0.2s ease-in-out;
    }}
    .stButton button:hover {{
        background: linear-gradient(135deg, {GOLD_SOFT} 0%, {GOLD} 100%);
        color: {DEEP_BLUE};
        border: 2px solid {DEEP_BLUE};
        transform: translateY(-2px);
    }}

    /* ---------- Section Divider ---------- */
    hr {{
        border: none;
        border-top: 2px dashed {GOLD_SOFT};
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

# ----------------------------------------------------------------------------
# 4. RULE-BASED CHATBOT LOGIC (backend)
# ----------------------------------------------------------------------------
# Each rule is a tuple: (list of regex patterns, list of possible responses)
# Using regex allows flexible matching (e.g. "hello", "hello there", "Hello!")
CHAT_RULES = [
    (
        [r"\bhi\b", r"\bhello\b", r"\bhey\b", r"\byo\b"],
        ["Hi there! 👋", "Hello! Great to see you.", "Hey! How can I help you today?"],
    ),
    (
        [r"how are you", r"how're you", r"how you doing"],
        ["I'm fine, thanks for asking! 😊", "Doing great! And you?", "All systems running smoothly!"],
    ),
    (
        [r"\bbye\b", r"goodbye", r"see you", r"take care"],
        ["Goodbye! Have a wonderful day. 🌟", "See you soon!", "Take care! Come back anytime."],
    ),
    (
        [r"your name", r"who are you"],
        ["I'm Aurora, your friendly rule-based chatbot! ✨", "You can call me Aurora."],
    ),
    (
        [r"\bthanks\b", r"thank you", r"thx"],
        ["You're welcome! 🙌", "Anytime! Happy to help.", "No problem at all!"],
    ),
    (
        [r"\bhelp\b", r"what can you do"],
        [
            "I can chat about greetings, how you're doing, my name, and say goodbye. Try 'hello' or 'how are you'!",
        ],
    ),
    (
        [r"time", r"date"],
        [f"Right now it's {datetime.now().strftime('%I:%M %p on %B %d, %Y')}."],
    ),
    (
        [r"joke", r"funny"],
        [
            "Why don't programmers like nature? Too many bugs. 🐛",
            "I told my computer I needed a break, and it said 'no problem — I'll go to sleep.' 💤",
        ],
    ),
]

# Fallback responses when no rule matches
FALLBACK_RESPONSES = [
    "I'm not sure I understand. Could you rephrase that?",
    "Hmm, I don't have a rule for that yet. Try asking me something else!",
    "Sorry, I didn't quite catch that. Try 'help' to see what I can do.",
]


def get_bot_response(user_text: str) -> str:
    """
    Core rule-matching function.

    Loops through each rule's list of regex patterns and checks whether
    any pattern matches the (lower-cased) user input. If a match is found,
    a random response from that rule's response list is returned.
    If no rule matches, a random fallback response is returned.

    Parameters
    ----------
    user_text : str
        The raw text typed by the user.

    Returns
    -------
    str
        The chatbot's response text.
    """
    text = user_text.lower().strip()

    # Guard clause: empty input
    if not text:
        return "Please type something so I can respond! 🙂"

    # Iterate over every rule and its associated patterns
    for patterns, responses in CHAT_RULES:
        for pattern in patterns:
            if re.search(pattern, text):
                return random.choice(responses)

    # No pattern matched -> fallback
    return random.choice(FALLBACK_RESPONSES)


# ----------------------------------------------------------------------------
# 5. SESSION STATE INITIALIZATION (preserves chat history across reruns)
# ----------------------------------------------------------------------------
if "chat_history" not in st.session_state:
    # Each entry: {"role": "user"/"bot", "text": str, "time": str}
    st.session_state.chat_history = [
        {
            "role": "bot",
            "text": "Hello! I'm Aurora 🤖 — ask me anything (try 'hello', 'how are you', or 'bye').",
            "time": datetime.now().strftime("%H:%M"),
        }
    ]

if "input_counter" not in st.session_state:
    # Used to reset the text_input widget after each submission
    st.session_state.input_counter = 0


def handle_user_message():
    """
    Callback triggered when the user submits a message.
    Reads the current input, generates a bot reply, and appends both
    to the persistent chat history stored in session state.
    """
    key = f"user_input_{st.session_state.input_counter}"
    user_text = st.session_state.get(key, "")

    if user_text.strip():
        timestamp = datetime.now().strftime("%H:%M")

        # Append user message
        st.session_state.chat_history.append(
            {"role": "user", "text": user_text, "time": timestamp}
        )

        # Generate and append bot response
        bot_reply = get_bot_response(user_text)
        st.session_state.chat_history.append(
            {"role": "bot", "text": bot_reply, "time": timestamp}
        )

        # Increment counter to force a fresh (empty) input widget next render
        st.session_state.input_counter += 1


def clear_chat():
    """Resets the chat history back to the initial greeting."""
    st.session_state.chat_history = [
        {
            "role": "bot",
            "text": "Chat cleared! Let's start fresh. 😊",
            "time": datetime.now().strftime("%H:%M"),
        }
    ]
    st.session_state.input_counter += 1


# ----------------------------------------------------------------------------
# 6. SIDEBAR — info panel & controls
# ----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("## 💎 Aurora Chat")
    st.markdown("A rule-based chatbot demo built with **Streamlit**.")
    st.markdown("---")
    st.markdown("### 🧭 Try saying:")
    st.markdown(
        "- `hello`\n"
        "- `how are you`\n"
        "- `what's your name`\n"
        "- `tell me a joke`\n"
        "- `what time is it`\n"
        "- `bye`"
    )
    st.markdown("---")
    st.button("🗑️ Clear Chat", on_click=clear_chat, use_container_width=True)
    st.markdown("---")
    st.caption("Palette: Deep Blue · Turquoise · Gold")

# ----------------------------------------------------------------------------
# 7. MAIN HEADER
# ----------------------------------------------------------------------------
st.markdown(
    """
    <div class="chat-header">
        <h1>💬 Aurora — Rule-Based Chatbot</h1>
        <p>Deep Blue • Vibrant Turquoise • Elegant Gold</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ----------------------------------------------------------------------------
# 8. CHAT HISTORY DISPLAY
# ----------------------------------------------------------------------------
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

for message in st.session_state.chat_history:
    if message["role"] == "user":
        st.markdown(
            f"""
            <div class="user-bubble">
                {message['text']}
                <div class="bubble-meta">You · {message['time']}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f"""
            <div class="bot-bubble">
                {message['text']}
                <div class="bubble-meta" style="color:#E8B94B;">Aurora · {message['time']}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.markdown("</div>", unsafe_allow_html=True)

# ----------------------------------------------------------------------------
# 9. USER INPUT AREA
# ----------------------------------------------------------------------------
input_col, button_col = st.columns([5, 1])

current_key = f"user_input_{st.session_state.input_counter}"

with input_col:
    st.text_input(
        "Type your message",
        key=current_key,
        placeholder="Type a message... e.g. 'hello'",
        label_visibility="collapsed",
        on_change=handle_user_message,
    )

with button_col:
    st.button("Send 🚀", on_click=handle_user_message, use_container_width=True)

# ----------------------------------------------------------------------------
# 10. FOOTER
# ----------------------------------------------------------------------------
st.markdown(
    f"""
    <hr>
    <p style="text-align:center; color:{DEEP_BLUE}; font-size:0.8rem;">
        Built with ❤️ using Streamlit — Rule-Based Logic Engine
    </p>
    """,
    unsafe_allow_html=True,
)
