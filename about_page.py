import streamlit as st

st.title("RAG-powered personal AI clone")
st.sidebar.markdown("""
Learn more about the project.
                    
[View source code](https://github.com/amkhrjee/ai-twin)
                    
[Learn more about me](https://amkhrjee.in)
""")

st.markdown("""
This is an experimental project built with [LangChain](https://www.langchain.com/). The AI here is a [ReAct agent](https://arxiv.org/abs/2210.03629) connected to a MongoDB vector database. It uses [Retrieval-Augmented Generation (RAG)](https://arxiv.org/abs/2005.11401) to fetch relevant data from the database and frame an answer according to the system prompt.
            
The agent uses cosine similarity to find similar excerpts of text from the vector database. The database comprises of relevant text describing my personality and likings. 
            
The agent gets its quirky behaviour from its straight-forward system prompt (which is supposed to be mimicing me).
            
This project is not perfect, and might hallucinate and reveal the identity of the foundation model used, which, by the way, is `gemini-2.0-flash`.

Thus, this is still under active development and I intend to add more features in the future.
            
Till then, have fun!

P.S. I'd really appreciate it if you send me screenshots of conversations with this AI agent that you found amusing/interesting/infuriating. I'm available at [amkhrjee@gmail.com](amkhrjee@gmail.com).           
""")
