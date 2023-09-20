import pandas as pd
import streamlit as st
from filtering_module import apply_filters
from visualization_module import (
    display_kpis,
    display_business_unit,
    display_gtm1,
    display_gtm2,
    display_account_kpis
)

def main():

    data = pd.read_excel('source/clean_data.xlsx')

    st.title("BCX Opportunity Dashboard")
    st.markdown('<p style="text-align: center;"> BCX Salesforce opportunities</p>', unsafe_allow_html=True)

    st.sidebar.title("Filters")
    selected_bus_unit = st.sidebar.selectbox("Select Business Unit", ['All'] + list(data['Bus_Unit'].unique()))
    selected_range = st.sidebar.selectbox("Select Range", ['All', 'Won', 'Lost'])
    selected_account_names = st.sidebar.selectbox("Select Account Name", ['All'] + list(data['Account_Name'].unique()))
    
    filtered_data = apply_filters(data, selected_bus_unit, selected_range, selected_account_names)
    
    if selected_account_names != 'All':
        account_data = filtered_data[filtered_data['Account_Name'] == selected_account_names]
        display_account_kpis(account_data)
    else:
        display_kpis(filtered_data)

    st.write("## Business Unit Wise")
    display_business_unit(filtered_data, selected_range, selected_account_names)
    st.write("## GTM1 Wise")
    display_gtm1(filtered_data, selected_range, selected_account_names)
    st.write("## GTM2 Wise")
    display_gtm2(filtered_data, selected_range, selected_account_names)


if __name__ == '__main__':
    main()
