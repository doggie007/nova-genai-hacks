from langchain_openai import ChatOpenAI
import streamlit as st
import gui
Jose = None
Hamza = None
James = None
submit1 = None
submit2 = None
dummyDropDowns = [Jose, Hamza, James]
instance = gui.gui(dummyDropDowns)

if instance != None:
    submit1, submit2 = instance

