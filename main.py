import streamlit as st
from time import time, sleep
from os import environ, listdir

from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_openai.chat_models import ChatOpenAI
from langchain_core.messages import HumanMessage

from voice import clone_voice, transcribe, speak

TEAM_API_KEY=environ.get('TEAM_API_KEY')
PROXY_ENDPOINT=environ.get('PROXY_ENDPOINT')
CARTESIA_KEY=environ.get('CARTESIA_KEY')


# Initialize session states
if 'messages' not in st.session_state:
    st.session_state.messages = ChatMessageHistory()
if 'button_triggered' not in st.session_state:
    st.session_state.button_triggered = False
if 'names' not in st.session_state:
    names = {}
    for file in listdir('dummy_data'):
        name = file[:-4]
        names[name] = {
            'embedding': clone_voice(file),
            'bio': transcribe(file)
        }
    st.session_state.names = names

llm = ChatOpenAI(
    openai_api_key=TEAM_API_KEY, 
    openai_api_base=PROXY_ENDPOINT,
    model="gpt-4o"
)

if not st.session_state.button_triggered:
    st.title("Roommate Matching")
    st.write("Looking for a roommate? Our platform helps match you with compatible living partners based on your bio, lifestyle preferences, and room photos.")
    
    st.markdown("<p class='custom-label'>Record a 20-30 second bio about yourself and attach it below</p>", unsafe_allow_html=True)
    uploaded_main_recording = st.audio_input('Start recording')

    st.markdown("<p class='custom-label'>Attach a photo of your room or mood board below</p>", unsafe_allow_html=True)
    upload_supplemental = st.file_uploader("", type=["jpeg", "png"])

    if upload_supplemental or uploaded_main_recording:
        if st.button("Submit"):
            st.session_state.button_triggered = True

if st.session_state.button_triggered:
    selected_name = st.selectbox("Choose a name to chat with:", list(st.session_state.names.keys()))
    selected_data = st.session_state.names[selected_name]
    embedding = selected_data['embedding']
    bio = selected_data['bio']

    # Display all previous chat messages
    for message in st.session_state.messages.messages:
        role = 'user' if isinstance(message, HumanMessage) else 'assistant'
        with st.chat_message(role):
            st.markdown(message.content)

    if prompt := st.chat_input('Your message', key='prompt'):
        st.session_state.messages.add_user_message(prompt)
        st.chat_message('user').markdown(prompt)

        response = llm.invoke(prompt).content
        st.session_state.messages.add_ai_message(response)
        
        with st.chat_message('assistant'):
            st.audio(speak(embedding, response), format="audio/wav", autoplay=True)
        
        sleep(0.5)