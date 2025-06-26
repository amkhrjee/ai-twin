import streamlit as st

st.title("About")
st.sidebar.markdown("""
Learn more about the project.
                    
[View source code](https://github.com/amkhrjee/ai-twin)
                    
[Learn more about me](https://amkhrjee.in)
""")

st.markdown("""
This is an experimental RAG project built with LangChain. The AI here is a [ReAct agent](https://arxiv.org/abs/2210.03629) connected to a MongoDB vector database.
            
The agent retrieves data from a text file stored and indexed in the database as necessary. 
            
The agent gets its behaviour from a straight-forward system prompt.
            
This project is not perfect, and might hallucinate and reveal the identity of the foundation model used, which, by the way, is Gemini 2.0-flash.

Thus, this is still under active development and I intent to add more features in the future.
            
Till then, have fun!            
""")
