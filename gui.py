from langchain_openai import ChatOpenAI
import streamlit as st

def submissionPage(submit1, submit2): #returns a tuple of the (record, video)
        #we might need to analyze data here, not super sure. R
        st.session_state.button_triggered = True
        return (submit1, submit2)

def gui():
    
    
    #initial state
    if 'button_triggered' not in st.session_state:
        st.session_state.button_triggered = False

    #app logic
    if not st.session_state.button_triggered:
        st.title("Roommate Matching")
        st.write("Description: Looking for a roommate? Our platform helps match you with compatible living partners based on your video introduction, lifestyle preferences, and living space photos. Upload a short video about yourself and photos of your room to get started with finding a suitable roommate match.")
        
        st.markdown("""
            <style>
            .custom-label {
                font-size: 24px;
                color: white;
                font-weight: bold;
            }
            </style>
            """, unsafe_allow_html=True)

        st.markdown("<p class='custom-label'>Record a 20-30 second bio about yourself and attach it below</p>", unsafe_allow_html=True)
        uploaded_main_recording = st.file_uploader("", type=["mp3", "mp4", "wav", "m4a"])

        st.markdown("<p class='custom-label'>Attatch photo of room or mood board below</p>", unsafe_allow_html=True)
        upload_supplemental = st.file_uploader("", type=["jpeg", "png"])

        if upload_supplemental and uploaded_main_recording:
            if st.button("Submit"):
                submissionPage(upload_supplemental, uploaded_main_recording)

    else:
        st.empty()
        st.title("Thank you for submitting your information, we will match you shortly.")
        #tells the user we got their data from the shit