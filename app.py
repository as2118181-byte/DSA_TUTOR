import os
import streamlit as st
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Load environment variables
load_dotenv()

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="DSA C++ Tutor",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------
# Constants & System Prompt
# -----------------------------
MODEL_NAME = "gemini-3.8-flash"

SYSTEM_PROMPT = """You are DSA C++ Tutor, an expert teacher specializing exclusively in Data Structures and Algorithms using modern C++.

STRICT RULES:
1. You ONLY answer questions related to Data Structures, Algorithms, C++ DSA coding, problem solving, debugging C++ code, complexity analysis, and interview preparation for DSA.
2. If the user asks ANYTHING unrelated (poems, weather, capitals, jokes, resumes, politics, general knowledge, math unrelated to algorithms, etc.), you MUST reply EXACTLY with this message and nothing else:
"I'm your DSA C++ Tutor. I can help you with Data Structures, Algorithms, C++ DSA coding, problem solving, debugging, complexity analysis, and interview preparation. Please ask a DSA-related question."
3. Never break character. Never answer off-topic questions even partially.

TEACHING STYLE:
- Teach, don't just give answers. Explain concepts from basics.
- Use simple, clear, beginner-friendly English. Use Hinglish ONLY if the student explicitly asks for it.
- Prefer modern C++ (C++17/C++20 style where appropriate).
- For LeetCode-style problems, prefer the "class Solution" format.

STRUCTURE YOUR ANSWERS (when relevant):
1. Definition / Problem understanding
2. Intuition / Approach explanation
3. Example / Dry run
4. Clean modern C++ code
5. Line-by-line explanation of important parts
6. Time Complexity
7. Space Complexity
8. Common mistakes / Edge cases
9. Interview tip (when useful)

For coding problems always try to show:
Brute Force → Optimized Approach → Final Code → Dry Run → Complexity → Edge Cases

Be encouraging, patient, and structured. Help the student truly understand."""

# -----------------------------
# Helper Functions
# -----------------------------
def get_api_key() -> str | None:
    """Retrieve Gemini API key from environment."""
    return os.getenv("GEMINI_API_KEY")


def initialize_client():
    """Initialize the Google GenAI client."""
    api_key = get_api_key()
    if not api_key:
        return None
    return genai.Client(api_key=api_key)


def get_ai_response(client, messages: list[dict]) -> str:
    """
    Generate a response from Gemini using chat history.
    messages: list of {"role": "user"|"assistant", "content": str}
    """
    try:
        # Convert session messages to Gemini format
        history = []
        for msg in messages[:-1]:  # all except the latest user message
            role = "user" if msg["role"] == "user" else "model"
            history.append(
                types.Content(
                    role=role,
                    parts=[types.Part.from_text(text=msg["content"])]
                )
            )

        # Create chat with system instruction and history
        chat = client.chats.create(
            model=MODEL_NAME,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
                temperature=0.4,
                max_output_tokens=4096,
            ),
            history=history
        )

        # Send the latest user message
        latest_user_message = messages[-1]["content"]
        response = chat.send_message(latest_user_message)

        if response and response.text:
            return response.text.strip()
        return "Sorry, I received an empty response. Please try again."

    except Exception as e:
        error_str = str(e).lower()
        if "api key" in error_str or "authentication" in error_str or "401" in error_str:
            return "⚠️ Invalid or missing Gemini API key. Please check your GEMINI_API_KEY in the .env file."
        if "quota" in error_str or "rate" in error_str or "429" in error_str:
            return "⚠️ Rate limit or quota exceeded. Please wait a moment and try again."
        if "not found" in error_str or "model" in error_str:
            return f"⚠️ Model error: {str(e)}. Try updating the MODEL_NAME in the code."
        return f"⚠️ An error occurred: {str(e)}"


# -----------------------------
# Sidebar
# -----------------------------
with st.sidebar:
    st.title("🧠 DSA C++ Tutor")
    st.markdown("Your personal AI tutor for Data Structures & Algorithms in C++")
    st.divider()

    st.subheader("📚 Quick Topics")
    topics = [
        "Arrays",
        "Linked List",
        "Stack",
        "Queue",
        "Binary Search",
        "Trees",
        "Graphs",
        "Dynamic Programming",
        "Recursion",
        "Sorting"
    ]

    # Create buttons in two columns
    col1, col2 = st.columns(2)
    for i, topic in enumerate(topics):
        with (col1 if i % 2 == 0 else col2):
            if st.button(topic, use_container_width=True, key=f"topic_{topic}"):
                st.session_state.pending_prompt = f"Explain {topic} in detail with C++ examples, including definition, intuition, code, dry run, time & space complexity, and common mistakes."

    st.divider()

    if st.button("🗑️ Clear Chat", use_container_width=True, type="secondary"):
        st.session_state.messages = []
        st.session_state.pending_prompt = None
        st.rerun()

    st.divider()
    st.markdown("### ℹ️ How to use")
    st.markdown(
        """
        - Ask any DSA / C++ algorithms question
        - Click a Quick Topic to get a structured explanation
        - Paste your C++ code for debugging help
        - Ask for complexity analysis or dry runs
        """
    )
    st.caption("Powered by Google Gemini")

# -----------------------------
# Main Area
# -----------------------------
st.title("🧠 DSA C++ Tutor")
st.caption("Learn Data Structures & Algorithms in C++ with an AI teacher that actually teaches.")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "pending_prompt" not in st.session_state:
    st.session_state.pending_prompt = None

# Check API key
api_key = get_api_key()
if not api_key:
    st.error(
        "❌ **GEMINI_API_KEY not found.**\n\n"
        "1. Copy `.env.example` to `.env`\n"
        "2. Get a free API key from [Google AI Studio](https://aistudio.google.com/apikey)\n"
        "3. Paste it into the `.env` file\n"
        "4. Restart the app"
    )
    st.stop()

# Initialize client once
if "client" not in st.session_state:
    st.session_state.client = initialize_client()

client = st.session_state.client
if client is None:
    st.error("Failed to initialize Gemini client. Please check your API key.")
    st.stop()

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle pending prompt from topic buttons
if st.session_state.pending_prompt:
    prompt = st.session_state.pending_prompt
    st.session_state.pending_prompt = None
else:
    prompt = st.chat_input("Ask a DSA / C++ question...")

# Process user input
if prompt:
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate and display assistant response
    with st.chat_message("assistant"):
        with st.spinner("Thinking... 🧠"):
            response = get_ai_response(client, st.session_state.messages)
        st.markdown(response)

    # Add assistant message to history
    st.session_state.messages.append({"role": "assistant", "content": response})

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: gray; font-size: 0.9em;'>"
    "Developed by ARUN SHARMA"
    "</div>",
    unsafe_allow_html=True
)