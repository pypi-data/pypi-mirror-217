import os
import streamlit as st
import streamlit.components.v1 as components

_RELEASE = True

if not _RELEASE:
    _component_func = components.declare_component(
        "chat_box_streamlit",
        url="http://localhost:5173",
    )
else:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/dist")
    _component_func = components.declare_component("chat_box_streamlit", path=build_dir)


def st_message(isLeft=True, message="", loading=False, loadingText="Loading...", placeholder="Enter your input", height=500, key=None):
    component_value =  _component_func(component="message", isLeft=isLeft, message=message, placeholder=placeholder, loading=loading, loadingText=loadingText, height=height, key=key)
    return component_value

def st_input(placeholder="Enter your input", loading=False, loadingText="Loading...", rows=1, key=None):
    component_value = _component_func(component="input", placeholder=placeholder, rows=rows, loading=loading, loadingText=loadingText, key=key)
    return component_value

def st_display_chat(leftMessages = [], rightMessages=[], height=500, rows=1, key=None):
    component_value = _component_func(component="", leftMessages=leftMessages, rightMessages=rightMessages, rows=rows, height=height, key=key)
    return component_value

if not _RELEASE:
    st.title("Chat Box Streamlit")
    st.write("This is a demo of the chat box component")
    st.write("### Input:")
    keyword = st_input(placeholder="Enter your input", loading=False, loadingText="Loading...", rows=1, key=None)
    st.write("### Messages:")
    st_display_chat(leftMessages = ["Hello", "How are you?"], rightMessages=["Hi", "I am fine"], height=500, rows=1, key=None)
    