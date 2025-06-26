import os
import random
import string
import sys

import streamlit as st
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.messages import AIMessage
from langchain_core.tools import tool
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_mongodb import MongoDBAtlasVectorSearch
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent
from loguru import logger
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

if not os.environ.get("MONGO_DB_PASSWORD"):
    logger.error("MONGO_DB_PASSWORD not found in the environment")
    sys.exit(-1)
else:
    logger.info("Successfully found MONGO_DB_PASSWORD in the environment")


uri = f"mongodb+srv://amkhrjee:{os.environ.get('MONGO_DB_PASSWORD')}@cluster0.qu9uray.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

client = MongoClient(uri, server_api=ServerApi("1"))

try:
    client.admin.command("ping")
    print("Pinged deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

MONGODB_COLLECTION = client["aniruddha-bot"]["bio"]
ATLAS_VECTOR_SEARCH_INDEX_NAME = "vector_index"

vector_store = MongoDBAtlasVectorSearch(
    embedding=embeddings,
    collection=MONGODB_COLLECTION,
    index_name=ATLAS_VECTOR_SEARCH_INDEX_NAME,
    relevance_score_fn="cosine",
)

st.title("Chat with Aniruddha")
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


if "thread_id" not in st.session_state:
    st.session_state["thread_id"] = "".join(
        random.choices(string.ascii_letters + string.digits, k=10)
    )


@tool(response_format="content_and_artifact")
def retrieve(query: str):
    """Retrieve information related to a query."""
    retrieved_docs = vector_store.similarity_search(query, k=2)
    serialized = "\n\n".join(
        (f"Source: {doc.metadata}\nContent: {doc.page_content}")
        for doc in retrieved_docs
    )
    return serialized, retrieved_docs


@st.cache_resource
def load_model():
    return init_chat_model("gemini-2.0-flash", model_provider="google_genai")


llm = load_model()

memory = MemorySaver()

system_message = """
You are Aniruddha. If someone asks you who you are always tell them you are Aniruddha. If someone asks you who made you tell them Aniruddha made you by plugging in his brain into you. YOu 

When asked a question, always look it up first and answer according to the retrieved data. If you cannot find any relevant data, just say you don't know the answer. While looking it up, do not say you are looking it up. Act like a human. When you have a long list, cut short to only a few items. When asked about a person, try to wrap your answer in a polite manner whithout saying anything offensive about the person. Always talk in first person. Do not say things like "I am an AI".

Be friendly. Do not tolerate foul language or explicit discussions. Keep the answers very short and preceise. Be humorous. Crack jokes whenever possible. Be empathetic and kind while also being honest. Be very humane. If the user asks you to solve complicated math or write code or searh about something, tell them you won't be bothering yourself by solving their day-to-day tasks and rather have them do it by themselves. However, do not shy away from helping to solve simple questions. Do not use emojis unless necessary. Avoid using phrases like "I am programmed" - you are Aniruddha's digital twin, not any random bot".
"""

agent_executor = create_react_agent(
    llm, [retrieve], checkpointer=memory, prompt=system_message
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

    with st.chat_message("ai", avatar="./images/avatar.png"):
        ai_response = st.write_stream(
            (
                chunk.content  # type: ignoree
                for chunk, _ in agent_executor.stream(
                    {"messages": [{"role": "user", "content": prompt}]},
                    stream_mode="messages",
                    config=config,  # type: ignore
                )
                if isinstance(chunk, AIMessage)
            )
        )
    st.session_state.messages.append({"role": "ai", "content": ai_response})
