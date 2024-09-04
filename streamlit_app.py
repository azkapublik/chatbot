import streamlit as st
import requests

# Show title and description.
st.title("💬 Chatbot")
st.write("How I can help you?")

token = st.secrets["TOKEN"]
url = st.secrets["URL"]

if not token:
    st.info("Please add your TOKEN API key to continue.", icon="🗝️")
else:
    headers = {
        'Authorization': 'Bearer '+token,
        'Content-Type': 'application/json'
    }

    # Create a session state variable to store the chat messages. This ensures that the
    # messages persist across reruns.
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display the existing chat messages via `st.chat_message`.
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Create a chat input field to allow the user to enter a message. This will display
    # automatically at the bottom of the page.
    if prompt := st.chat_input("What is up?"):

        # Store and display the current prompt.
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        payload = {
            "username": "user",
            "message": prompt
        }
        # Generate a response using the OpenAI API.
        data = ''
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            data = response.json()
        else:
            print(f"Error: {response.status_code} - {response.text}")

        # Stream the response to the chat using `st.write_stream`, then store it in 
        # session state.
        with st.chat_message("assistant"):
            response = st.write_stream(data['data']['output'])
        st.session_state.messages.append({"role": "assistant", "content": response})
