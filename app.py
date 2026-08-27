from random import SystemRandom
from chatbot import chat_model
from schemas import str_output_parser,pydantic_output_parser
from langchain.messages import SystemMessage,AIMessage,HumanMessage
from langchain_core.runnables import RunnableBranch,RunnableParallel
from prompts import programming_template,mathematical_template,general_template,summary_prompt,answer_prompt
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

def clear_text():
    st.session_state.chat_history=[SystemMessage(content="You are a helpful assistant.Always answer useful things,try to avoid unnecessary things.And if possible then give a short paragraph(if it is wanted)")]

general_chain=general_template|chat_model|str_output_parser
programming_chain=programming_template|chat_model|str_output_parser
mathematical_chain=mathematical_template|chat_model|str_output_parser

conditional_chain=RunnableBranch(
    (lambda x:"programming intuition" in x["category_input"].strip().lower(),programming_chain),
    (lambda x:"mathematical intuition" in x["category_input"].strip().lower(),mathematical_chain),
    general_chain
)

parallel_chain=RunnableParallel({
    "summary":conditional_chain|summary_prompt|chat_model|pydantic_output_parser,
    "answer":conditional_chain|answer_prompt|chat_model|pydantic_output_parser
})

if "chat_history" not in st.session_state:
    st.session_state.chat_history=[SystemMessage(content="You are a helpful assistant.Always answer useful things,try to avoid unnecessary things.And if possible then give a short paragraph(if it is wanted)")]

st.title("Simple AI Tutor")

for msg in st.session_state.chat_history:

    if isinstance(msg,SystemMessage):
        continue
    elif isinstance(msg,HumanMessage):
        st.write(msg.content,HumanMessage)
    elif isinstance(msg,AIMessage):
        st.write(msg.content,AIMessage)

user_input=st.chat_input("Ask me anything.......")

category_input=st.selectbox(
    "Response Category",
    ["General Intuition","Programming Intuition","Mathematical Intuition"]
)
input_type=st.selectbox(
    "Explanation Level",
    ["Beginner-Friendly","Intermediate","Deep Intuition"]
)

with st.sidebar:
    st.subheader("💬 Chat History")
    st.button("Clear",on_click=clear_text)
    st.divider()
    for msg in st.session_state.chat_history:
        if isinstance(msg, SystemMessage):
            continue

        if isinstance(msg, HumanMessage):
            st.markdown(f"**👤 You:** {msg.content}")
        elif isinstance(msg, AIMessage):
            st.markdown(f"**🤖 AI:** {msg.content}")

if user_input:
    st.session_state.chat_history.append(HumanMessage(content=user_input))

    with st.chat_message("human"):
        st.write(user_input)

    result=parallel_chain.invoke({
        "user_input":user_input,
        "input_type":input_type,
        "category_input":category_input,
        "chat_history":st.session_state.chat_history
    })

    with st.chat_message("ai"):
        st.markdown("### Summary")
        st.write(result["summary"].summary)

        st.markdown("### Answer")
        st.write(result["answer"].answer)

    st.session_state.chat_history.append(AIMessage(content=result["summary"].summary))

