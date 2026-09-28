import streamlit as st
import ollama

st.title("AI Chatbot")
st.subheader("Welcome to the AI Chatbot! Please enter your message below.")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

with st.form("ask_ai_form"):
    user_input = st.text_input("Your message", placeholder="Ask any question")
    ask_ai = st.form_submit_button("Ask AI")

if ask_ai:
    if not user_input.strip():
        st.warning("Please enter a message first.")
    else:
        user_message = user_input.strip()
        st.session_state.messages.append(
            {"role": "user", "content": user_message}
        )

        with st.chat_message("user"):
            st.write(user_message)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    response = ollama.chat(
                        model="llama3.2:3b",
                        messages=st.session_state.messages,
                    )
                    ai_response = response["message"]["content"]
                except Exception as error:
                    st.error(f"Unable to get a response: {error}")
                else:
                    st.session_state.messages.append(
                        {"role": "assistant", "content": ai_response}
                    )
                    st.write(ai_response)