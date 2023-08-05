import os
import streamlit as st
import streamlit.components.v1 as components

_RELEASE = True

if not _RELEASE:
    _chat_box_streamlit = components.declare_component(
        "chat_box_streamlit",
        url="http://localhost:5173",
    )
else:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/dist")
    _chat_box_streamlit = components.declare_component("chat_box_streamlit", path=build_dir)


def display_chat(component="", isLeft=True, message="", placeholder="Enter your input", loading=False, loadingText="Loading...", height=500, leftMessages=[], rightMessages=[], rows=1, key=None):
    if component == "message":
        component_value = _chat_box_streamlit(component="message", isLeft=isLeft, message=message, placeholder=placeholder, loading=loading, loadingText=loadingText, height=height, key=key)
    elif component == "input":
        component_value = _chat_box_streamlit(component="input", placeholder=placeholder, rows=rows, loading=loading, loadingText=loadingText, key=key)
    else:
        component_value = _chat_box_streamlit(component="", leftMessages=leftMessages, rightMessages=rightMessages, rows=rows, height=height, key=key)

    return component_value

if not _RELEASE:
    st.title("Chat Box Streamlit")
    st.write("This is a demo of the chat box component")
    st.write("### Input:")
    input_value = display_chat(component="input", placeholder="Enter your input", rows=1)
    