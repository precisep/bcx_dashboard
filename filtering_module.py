import streamlit as st
import pandas as pd

def apply_filters(data, selected_bus_unit, selected_range, selected_account_names):
    filtered_data = data.copy()

    if selected_bus_unit != 'All':
        filtered_data = filtered_data[filtered_data['Bus_Unit'] == selected_bus_unit]

    if selected_range != 'All':
        filtered_data = filtered_data[filtered_data['Range'] == selected_range]

    if selected_account_names != 'All':
        filtered_data = filtered_data[filtered_data['Account_Name'] == selected_account_names]

    return filtered_data

