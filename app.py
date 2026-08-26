from chatbot import chat_model
from schemas import str_output_parser,pydantic_output_parser
from langchain.messages import SystemMessage,AIMessage,HumanMessage
from langchain_core.runnables import RunnableBranch,RunnableParallel
from prompts import programming_template,mathematical_template,general_template,summary_prompt,answer_prompt
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

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

    result=parallel_chain.invoke({
        "user_input":user_input,
        "input_type":input_type,
        "category_input":category_input,
        "chat_history":st.session_state.chat_history
    })

    with st.chat_message("ai"):
        st.write(f"""Summary:{result["summary"].summary}
        Result:{result["answer"].answer}""")

    st.session_state.chat_history.append(AIMessage(content=result["answer"].answer))