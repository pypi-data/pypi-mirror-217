import os
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
    options = slice_select("Options",
            default=["Hello", "World", "Everybody"])
    color_values = [
        {"label": "blue", "status": False, "enabled": True},
        {"label": "red", "status": True, "enabled": True},
        {"label": "yellow", "status": False, "enabled": False},
        {"label": "violet", "status": True, "enabled": False},
    ]
    st.session_state["colors"] = color_values
    slice_select("Colors", default=color_values, key="colors")
    st.write("Hello")
    st.write(options)
