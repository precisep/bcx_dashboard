import pandas as pd
import streamlit as st
from filtering_module import apply_filters
from visualization_module import (
    display_kpis,
    display_business_unit,
    display_gtm1,
    display_gtm2,
)

def main():

    data = pd.read_excel('clean_data.xlsx')

    st.title("BCX Opportunity Dashboard")
    st.markdown('<p style="text-align: center;"> BCX Salesforce opportunities</p>', unsafe_allow_html=True)

    st.sidebar.title("Filters")
    selected_bus_unit = st.sidebar.selectbox("Select Business Unit", ['All'] + list(data['Bus_Unit'].unique()))
    selected_range = st.sidebar.selectbox("Select Range", ['All', 'Won', 'Lost'])

    filtered_data = apply_filters(data, selected_bus_unit, selected_range)
    
    display_kpis(filtered_data)
    st.write("## Business Unit Wise")
    display_business_unit(filtered_data, selected_range)
    st.write("## GTM1 Wise")
    display_gtm1(filtered_data,selected_range)
    st.write("## GTM2 Wise")
    display_gtm2(filtered_data,selected_range)

if __name__ == '__main__':
    main()
