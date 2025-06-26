import streamlit as st

# Meta text
st.markdown("## Chat with Aniruddha")
st.sidebar.markdown("# Chat")
st.sidebar.markdown("""
Hi! I'm Aniruddha, or rather, his digital twin. He has plugged in his brain into me, giving me full access to his thoughts, memory and deepest desires and fears. I'm his digital doppleganger.


P.S. He's a simple guy who enjoys food, beaches,  mild cool breezes and bright sunny days. He tries really hard to be funny and relatable. He's a nerd.
""")


with st.chat_message("ai", avatar="./images/avatar.png"):
    st.text("Hello! This is a fake response!")

    
with st.chat_message("user", avatar="🧑🏻"):
    st.text("Hello! How are you?")

prompt = st.chat_input("Say something")
if prompt:
    st.write(f"User has sent the following prompt: {prompt}")