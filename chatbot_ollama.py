from ollama import Client
import streamlit as st

st.title("ChatGPT-like clone")

client = Client(host='http://localhost:11434')

if "ollama_model" not in st.session_state:
    st.session_state["ollama_model"] = "llama3.1"

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        stream = client.chat(
            model=st.session_state["ollama_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )
        response = st.write_stream(stream)
        
    # Store the full assistant response
    st.session_state.messages.append({"role": "assistant", "content": response})