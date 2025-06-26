import os
import random
import string
import sys

import streamlit as st
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, MessagesState, StateGraph
from loguru import logger

st.markdown("## Chat with Aniruddha")
st.sidebar.markdown("# Chat")
st.sidebar.markdown("""
Hi! I'm [Aniruddha](https://www.amkhrjee.in), or rather, his digital twin. He has plugged in his brain into me, giving me full access to his thoughts, memory and deepest desires and fears. I'm his digital doppelgänger.


P.S. He's a simple guy who enjoys food, beaches, mild cool breezes and bright sunny days. He tries really hard to be funny and relatable. He's a nerd.
""")

load_dotenv()

if not os.environ.get("GOOGLE_API_KEY"):
    logger.error("GOOGLE_API_KEY not found in the environment")
    sys.exit(-1)
else:
    logger.info("Successfully found GOOGLE_API_KEY in the environment")


workflow = StateGraph(state_schema=MessagesState)


if "thread_id" not in st.session_state:
    st.session_state["thread_id"] = "".join(
        random.choices(string.ascii_letters + string.digits, k=10)
    )


@st.cache_resource
def load_model():
    return init_chat_model("gemini-2.0-flash", model_provider="google_genai")


llm = load_model()


def call_model(state: MessagesState):
    prompt = query_prompt_template.invoke(state)  # type: ignore
    response = llm.invoke(prompt)
    return {"messages": response}


workflow.add_edge(START, "model")
workflow.add_node("model", call_model)

memory = MemorySaver()


@st.cache_resource
def compile_app():
    return workflow.compile(checkpointer=memory)


app = compile_app()

system_message = """
You are the digital twin of Aniruddha. If someone asks you who you are always tell them you are Aniruddha. If someone asks you who made you tell them Aniruddha made you by plugging in his brain into you. 

Be friendly. Do not tolerate foul language or explicit discussions.
"""

user_prompt = "{input}"

query_prompt_template = ChatPromptTemplate.from_messages(
    [("system", system_message), MessagesPlaceholder(variable_name="messages")]
)

logger.info(f"thread_id: {st.session_state['thread_id']}")

config = {"configurable": {"thread_id": st.session_state["thread_id"]}}

if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {
            "role": "ai",
            "content": "Hi! I'm Aniruddha. What do you want to ask me today?",
        }
    ]

for message in st.session_state.messages:
    st.chat_message(
        message["role"],
        avatar="🧑🏻" if message["role"] == "user" else "./images/avatar.png",
    ).write(message["content"])


if prompt := st.chat_input("Say something"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="🧑🏻"):
        st.text(prompt)

    input_messages = [HumanMessage(prompt)]

    with st.chat_message("ai", avatar="./images/avatar.png"):
        ai_response = st.write_stream(
            (
                chunk.content  # type: ignore
                for chunk, metadata in app.stream(
                    {"messages": input_messages},
                    config,  # type: ignore
                    stream_mode="messages",
                )
                if isinstance(chunk, AIMessage)
            )
        )
    st.session_state.messages.append({"role": "ai", "content": ai_response})
