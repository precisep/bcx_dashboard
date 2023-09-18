import streamlit as st
import pandas as pd

def apply_filters(data, selected_bus_unit, selected_range):
 
    if selected_bus_unit != 'All':
        filtered_data = data[data['Bus_Unit'] == selected_bus_unit]
    else:
        filtered_data = data.copy()

    if selected_range != 'All':
        filtered_data = filtered_data[filtered_data['Range'] == selected_range]

    return filtered_data
