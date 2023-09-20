import pandas as pd
import streamlit as st
from filtering_module import apply_filters
from visualization_module import (
    display_kpis,
    display_business_unit,
    display_gtm1,
    display_gtm2,
    display_account_kpis,
    display_business_unit_time_series
)

def main():

    data = pd.read_excel('source/clean_data.xlsx')
    st.markdown(
        '<div style="background-color: black; padding: 10px; color: white; text-align: center; font-size: 36px;">'
        "BCX Opportunities Dashboard"
        '</div>',
        unsafe_allow_html=True
    )
    
    st.markdown(
        '<div style="background-color: red; padding: 10px; color: black; text-align: center; font-size: 18px;">'
        'BCX Salesforce opportunities'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown("<br>", unsafe_allow_html=True)

    st.sidebar.title("Filters")
    selected_bus_unit = st.sidebar.selectbox("Select Business Unit", ['All'] + list(data['Bus_Unit'].unique()))
    selected_account_names = st.sidebar.selectbox("Select Account Name", ['All'] + list(data['Account_Name'].unique()))
    selected_range = st.sidebar.radio("Select Range", ['All', 'Won', 'Lost'])
    
    filtered_data = apply_filters(data, selected_bus_unit, selected_range, selected_account_names)
    
    if selected_account_names != 'All':
        account_data = filtered_data[filtered_data['Account_Name'] == selected_account_names]
        display_account_kpis(account_data)
    else:
        display_kpis(filtered_data)

    st.write("## Business Unit Wise")
    display_business_unit(filtered_data, selected_range, selected_account_names)
    st.write("## Business Unit Wise Time Series")
    display_business_unit_time_series(filtered_data, selected_range, selected_bus_unit)
    st.write("## GTM1 Wise")
    display_gtm1(filtered_data, selected_range, selected_account_names)
    st.write("## GTM2 Wise")
    display_gtm2(filtered_data, selected_range, selected_account_names)

    relative_image_path = "source/footer.jpg"
    st.image(relative_image_path, use_column_width=True)


if __name__ == '__main__':
    main()
