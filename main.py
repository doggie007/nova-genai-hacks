from langchain_openai import ChatOpenAI
import streamlit as st

llm = ChatOpenAI(
    openai_api_key="sk-1-nnzryEbytTnAqTcIyH7Q", 
    openai_api_base="https://nova-litellm-proxy.onrender.com",
    model="gpt-4o"
)

template = """Generate a kids story based on this prompt: {query}"""

prompt = template.format(query='My sons dad was in jail. Write a story to make sure he doesnt end like him')

response = llm.invoke(prompt)

st.write("Roommate Matching")
st.write(response.content)
