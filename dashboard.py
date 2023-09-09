import pandas as pd
import streamlit as st
import plotly.express as px

def dashboard(data):
    # Convert TCV column to numeric
    

    # Set page title and center it
    st.title("BCX Opportunity Dashboard")
    st.markdown('<p style="text-align: center;"> BCX Salesforce opportunities</p>', unsafe_allow_html=True)

    # Create a section for toggling filtered data
    st.sidebar.title("View Options")
    show_filtered_data = st.sidebar.checkbox("Show Filtered Data", value=False)

    if show_filtered_data:
        visualize_filtered_data(data)
    else:
        visualize_original_data(data)

def visualize_filtered_data(data):
    # Sidebar filters
    st.sidebar.title("Filters")
    selected_bus_unit = st.sidebar.selectbox("Select Business Unit", ['All'] + list(data['Bus_Unit'].unique()))
    selected_gtm1 = st.sidebar.multiselect("Select GTM1", ['All'] + list(data['GTM1'].unique()))
    selected_gtm2 = st.sidebar.multiselect("Select GTM2", ['All'] + list(data['GTM2'].unique()))
    selected_range = st.sidebar.multiselect("Select Range", ['All'] + list(data['Range'].unique()))

    # Apply filters
    filtered_data = data.copy()
    if selected_bus_unit != 'All':
        filtered_data = filtered_data[filtered_data['Bus_Unit'] == selected_bus_unit]
    if 'All' not in selected_gtm1:
        filtered_data = filtered_data[filtered_data['GTM1'].isin(selected_gtm1)]
    if 'All' not in selected_gtm2:
        filtered_data = filtered_data[filtered_data['GTM2'].isin(selected_gtm2)]
    if 'All' not in selected_range:
        filtered_data = filtered_data[filtered_data['Range'].isin(selected_range)]

    visualize_data(filtered_data)

def visualize_original_data(data):
    visualize_data(data)

def visualize_data(data):
    # Calculate KPIs based on data
    num_deal_won = data[data['Range'] == 'Won'].shape[0]
    num_deal_lost = data[data['Range'] == 'Lost'].shape[0]
    data['TCV'] = pd.to_numeric(data['TCV'], errors='coerce')
    total_tcv_won = data[data['Range'] == 'Won']['TCV'].sum() / 1000000000
    total_tcv_lost = data[data['Range'] == 'Lost']['TCV'].sum() / 1000000000
    total_tcv = data['TCV'].sum() / 1000000000

    # Display KPIs layout
    kpi_col1, kpi_col2, kpi_col3 = st.columns(3)
    with kpi_col1:
        st.metric(label='Total TCV (Billion ZAR)', value=f'ZAR {total_tcv:.2f} B')
    with kpi_col2:
        st.metric(label='Total TCV Won (Billion ZAR)', value=f'ZAR {total_tcv_won:.2f} B', delta_color="inverse")
    with kpi_col3:
        st.metric(label='Total TCV Lost (Billion ZAR)', value=f'ZAR {total_tcv_lost:.2f} B', delta_color="inverse")

    kpi_col4, kpi_col5, kpi_col6 = st.columns(3)
    with kpi_col4:
        st.metric(label='Total Deals', value=num_deal_won + num_deal_lost, delta_color="inverse")
    with kpi_col5:
        st.metric(label='Number of Deals Won', value=num_deal_won, delta_color="inverse")
    with kpi_col6:
        st.metric(label='Number of Deals Lost', value=num_deal_lost, delta_color="inverse")

        # Streamlit layout
    st.write("## Bus Unit Wise")
    kpi_col7, kpi_col8 = st.columns(2)
    with kpi_col7:
        # Display Business Unit pie chart
        range_counts = data['Bus_Unit'].value_counts()
        fig_bus_unit_pie = px.pie(values=range_counts.values, names=range_counts.index, title='Bus Unit Wise', hole=0.7,
                                color_discrete_sequence=px.colors.qualitative.Set2)
        fig_bus_unit_pie.update_traces(textinfo='percent+label', sort=False)
        st.plotly_chart(fig_bus_unit_pie)

    with kpi_col8:
        # Display Business Unit TCV trends
        fig_bar = px.bar(data_frame=data.sort_values(by='TCV', ascending=False), y='Bus_Unit', x='TCV', orientation='h', title='Business Unit Trends')
        st.plotly_chart(fig_bar)

    st.write("## GTM1 Wise")
    kpi_col9, kpi_col10 = st.columns(2)
    with kpi_col9:
        # Display GTM1 pie chart
        range_counts = data['GTM1'].value_counts()
        fig_gtm1_pie = px.pie(values=range_counts.values, names=range_counts.index, title='GTM1 Wise', hole=0.7,
                            color_discrete_sequence=px.colors.qualitative.Set2)
        fig_gtm1_pie.update_traces(textinfo='percent+label', sort=False)
        st.plotly_chart(fig_gtm1_pie)

    with kpi_col10:
        # Display GTM1 TCV trends
        fig_bar_gtm1 = px.bar(data_frame=data.sort_values(by='TCV', ascending=False), y='GTM1', x='TCV', orientation='h', title='GTM1 Trends')
        st.plotly_chart(fig_bar_gtm1)

    st.write("## GTM2 Wise")
    kpi_col11, kpi_col12 = st.columns(2)
    with kpi_col11:
        # Display GTM2 pie chart
        range_counts = data['GTM2'].value_counts()
        fig_gtm2_pie = px.pie(values=range_counts.values, names=range_counts.index, title='GTM2 Wise', hole=0.7,
                            color_discrete_sequence=px.colors.qualitative.Set2)
        fig_gtm2_pie.update_traces(textinfo='percent+label', sort=False)
        st.plotly_chart(fig_gtm2_pie)

    with kpi_col12:
        # Display GTM2 TCV trends
        fig_bar_gtm2 = px.bar(data_frame=data.sort_values(by='TCV', ascending=False), y='GTM2', x='TCV', orientation='h', title='GTM2 Trends')
        st.plotly_chart(fig_bar_gtm2)

if __name__ == '__main__':
    # Read data from the CSV or Excel file
    data = pd.read_excel('clean_data.xlsx')

    # Call the dashboard function
    dashboard(data)