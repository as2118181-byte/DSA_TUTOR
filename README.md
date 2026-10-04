# 🧠 DSA C++ Tutor

An AI-powered educational Streamlit web application that acts as a specialized tutor for **Data Structures and Algorithms in C++**.

It is **not** a general chatbot. It only answers DSA / C++ / algorithms related questions and politely refuses everything else.

---

## ✨ Features

- Clean chat interface (`st.chat_message` + `st.chat_input`)
- Full conversation history (session state)
- Strong system prompt that keeps the AI focused only on DSA & C++
- Beginner-friendly explanations
- Modern C++ code examples (class Solution style preferred for problems)
- Dry runs, time & space complexity analysis
- C++ DSA code debugging help
- Quick topic buttons in the sidebar
- Clear Chat button
- Loading spinner while the AI is thinking
- Proper error handling for missing API key, rate limits, etc.
- Footer: **Developed by ARUN SHARMA**

---

## 🛠 Tech Stack

- Python 3.9+
- Streamlit
- Google Gemini API via official modern SDK: `google-genai`
- `python-dotenv` for secure API key management

---

## 📁 Project Structure
