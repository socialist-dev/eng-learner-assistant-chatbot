# Inspo Chatbot for Public: Can not storage chat history

import os
from dotenv import dotenv_values
import streamlit as st
import streamlit.components.v1 as components
from groq import Groq

# Function resolves response thread from Groq
def parse_groq_stream(stream):
    for chunk in stream:
        if chunk.choices:
            if chunk.choices[0].delta.content is not None:
                yield chunk.choices[0].delta.content


# streamlit page configuration
st.set_page_config(
    page_title="English Learner Assistant",
    page_icon="https://img.icons8.com/?size=100&id=ftgzqv4ry3uF&format=png&color=000000",
    layout="wide"
)

try:
    secrets = dotenv_values(".env")  # for dev env
    GROQ_API_KEY = secrets["GROQ_API_KEY"]
except:
    secrets = st.secrets  # for streamlit deployment
    GROQ_API_KEY = secrets["GROQ_API_KEY"]

# save the api_key to environment variable
os.environ["GROQ_API_KEY"] = GROQ_API_KEY

INITIAL_RESPONSE = secrets["INITIAL_RESPONSE"]
INITIAL_MSG = secrets["INITIAL_MSG"]
CHAT_CONTEXT = secrets["CHAT_CONTEXT"]


client = Groq()

# initialize the chat history if present as streamlit session
if "chat_history" not in st.session_state:
    # print("message not in chat session")
    st.session_state.chat_history = [
        {"role": "assistant",
         "content": INITIAL_RESPONSE
         },
    ]

# Modify style
hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    button[title^=Exit]+div [data-testid=stImage]{
            text-align: center;
            display: block;
            margin-left: auto;
            margin-right: auto;
            width: 100%;
        }
    </style>
    """

# Hide components of Streamlit
st.markdown(hide_streamlit_style, unsafe_allow_html=True)


# Page title
col1, col2, col3 = st.columns(3)
with col2:
    gif1 = "https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExcmhyamNhNWdvY201MWh2YWI3M2ZkZ24xNjB4bWc2OXRhMmthMWFqMCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9cw/621nhiYcf5pWS8yfmT/giphy.webp"
    gif2 = "https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExZjlnYjJsMTk5MGJkeG9ydjRvbzNtaWM1am5lZHNvaDB3cHYyM3g4YiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9cw/KZwaIIz48b8w9Az3L5/giphy.webp"
    gif3 = "https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExem1sejhjMGN3bHRhZzZwdDhkbzRlMGhiNzUxdmUyNThpZTZ6YWk4dCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9cw/MCEneemI5TEZmzeiZk/giphy.webp"
    st.image(gif3, use_column_width="always", caption="Learn so Hard, Get so High")
st.title("Hello!")
st.write("📚Today is a good day to learn!")
st.caption("MeowGPT: Using for Word Dominion (Discord group) learning, practicing English")
# the messages in chat_history will be stored as {"role":"user/assistant", "content":"msg}
# display chat history
for message in st.session_state.chat_history:
    # print("message in chat session")
    with st.chat_message("role", avatar='https://img.icons8.com/?size=100&id=ftgzqv4ry3uF&format=png&color=000000'):
        st.markdown(message["content"])


# user input field
user_prompt = st.chat_input("Write something...")

if user_prompt:
    # st.chat_message("user").markdown
    with st.chat_message("user", avatar="🗨️"):
        st.markdown(user_prompt)
    st.session_state.chat_history.append(
        {"role": "user", "content": user_prompt})

    # get a response from the LLM
    messages = [
        {"role": "system", "content": CHAT_CONTEXT
         },
        {"role": "assistant", "content": INITIAL_MSG},
        *st.session_state.chat_history
    ]

    # Display assistant response in chat message container
    with st.chat_message("assistant", avatar='https://img.icons8.com/?size=100&id=ftgzqv4ry3uF&format=png&color=000000'):
        stream = client.chat.completions.create(
            model="llama-3.1-70b-versatile",
            messages=messages,
            stream=True  # for streaming the message
        )
        response = st.write_stream(parse_groq_stream(stream))
    st.session_state.chat_history.append(
        {"role": "assistant", "content": response})

