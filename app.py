import streamlit as st
import google.generativeai as gemini

st.set_page_config(page_title="conversationai", layout="wide")

# Define available languages and their corresponding models
list_languages = ['Artificial Intelligence', 'English', 'Data Science', 'Deep Learning', 'Mathematics', 'Machine learning']
language = st.selectbox("Select a Topic ", list_languages)

st.title(f"{language}")

# Load API key from file
with open('key.txt') as f:
    api_key = f.read().strip()

gemini.configure(api_key=api_key)

# Get the corresponding model for the selected language
model = gemini.GenerativeModel(model_name="gemini-1.5-pro-latest",
                               system_instruction=f"You are AI Assistant to {language}. Queries of the user.")

if "messages" not in st.session_state.keys() or st.session_state.language != language:
    st.session_state.messages = [
        {"role": "assistant", "content": f"Hello, this is Friendly AI. How can I help you with {language} today?"}
    ]
    st.session_state.language = language
    st.title(f"Want to Learn about {language}. Great Choice...!!!")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

user_input = st.chat_input()

if user_input is not None:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Loading..."):
            try:
                ai_response = model.generate_content(user_input)
                if ai_response.text:
                    st.write(ai_response.text)
                else:
                    st.write("Sorry, no response from the AI model.")
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
