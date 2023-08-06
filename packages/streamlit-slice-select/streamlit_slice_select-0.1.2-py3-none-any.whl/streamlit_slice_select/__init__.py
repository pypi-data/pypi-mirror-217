"""
Streamlit Slice Select Python Interface
"""

import os
import json
import streamlit.components.v1 as components

_RELEASE = False

parent_path = os.path.dirname(os.path.abspath(__file__))
build_dir = os.path.join(parent_path, "frontend", "dist")

_component_func = components.declare_component(
    "slicer",
    path=build_dir
)

def slice_select(name, default=[], key=None):
    component_value = _component_func(name=name, key=key, default=default)
    return component_value

if __name__ == "__main__":
    import streamlit as st
    st.subheader("A like Excel-slicer input widget for Streamlit")
    st.text("This is a custom component that behaves like Excel's slicer control")
    col1, col2 = st.columns(2)
    with col1:
        options = slice_select("Colors",
                default=["Yellow", "Blue", "Red", "Violet", "Green"])
        st.write("below")
    col2.write(options)
