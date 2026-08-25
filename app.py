from chatbot import chat_model
from schemas import str_output_parser,pydantic_output_parser
from langchain.messages import SystemMessage,AIMessage,HumanMessage
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

if "chat_history" not in st.session_state:
    st.session_state.chat_history=[SystemMessage(content="You are a helpful assistant.Always answer useful things,try to avoid unnecessary things.And if possible then give a short paragraph(if it is wanted)")]

st.header("Simple ChatBot")

user_input=st.chat_input()

category_input=st.selectbox(
    "Response Category",
    ["General Intuition","Programming Intuition","Mathematical Intuition"]
)
input_type=st.selectbox(
    "Explanation Level",
    ["Beginner-Friendly","Intermediate","Deep Intuition"]
)

with st.sidebar:
    st.subheader("Chat History")

    if not st.session_state.chat_history:
        st.write("Empty")
    else:
        for msg in st.session_state.chat_history:
            if isinstance(msg,SystemMessage):
                continue
            elif isinstance(msg,AIMessage):
                role="AI"
            else:
                role="Human"

            st.write(f"{role}:{msg.content}")

if user_input:
    st.session_state.chat_history.append(HumanMessage(content=user_input))

    with st.chat_message("human"):
        st.write(user_input)

    result=chat_model.invoke(st.session_state.chat_history)

    with st.chat_message("ai"):
        st.write(result.content)

    st.session_state.chat_history.append(AIMessage(content=result.content))