import pandas as pd
import streamlit as st
import plotly.express as px

def dashboard():
    # Read data from the CSV or Excel file
    data = pd.read_excel('clean_data.xlsx')
    table = data.copy()

    # Convert TCV column to numeric
    table['TCV'] = pd.to_numeric(table['TCV'], errors='coerce')

    # Set page title and center it
    st.title("BCX Opportunity Dashboard")
    st.markdown('<p style="text-align: center;"> BCX Salesforce opportunities</p>', unsafe_allow_html=True)

    # Sidebar filters
    st.sidebar.title("Filters")
    selected_bus_unit = st.sidebar.selectbox("Select Business Unit", ['All'] + list(table['Bus_Unit'].unique()))
    selected_gtm1 = st.sidebar.multiselect("Select GTM1", ['All'] + list(table['GTM1'].unique()))
    selected_gtm2 = st.sidebar.multiselect("Select GTM2", ['All'] + list(table['GTM2'].unique()))
    selected_range = st.sidebar.multiselect("Select Range", ['All'] + list(table['Range'].unique()))

    # Apply filters
    if selected_bus_unit != 'All':
        table = table[table['Bus_Unit'] == selected_bus_unit]
    if 'All' not in selected_gtm1:
        table = table[table['GTM1'].isin(selected_gtm1)]
    if 'All' not in selected_gtm2:
        table = table[table['GTM2'].isin(selected_gtm2)]
    if 'All' not in selected_range:
        table = table[table['Range'].isin(selected_range)]

    # Calculate KPIs based on filtered data
    num_deal_won = table[table['Range'] == 'Won'].shape[0]
    num_deal_lost = table[table['Range'] == 'Lost'].shape[0]
    total_tcv_won = table[table['Range'] == 'Won']['TCV'].sum() / 1000000000
    total_tcv_lost = table[table['Range'] == 'Lost']['TCV'].sum() / 1000000000
    total_tcv = table['TCV'].sum() / 1000000000

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

    # Create a section for visualizations
    st.write("## Visualizations")

    # Create Bus Unit pie chart
    st.subheader("Bus Unit Wise")
    range_counts = table['Bus_Unit'].value_counts()
    fig_bus_unit_pie = px.pie(values=range_counts.values, names=range_counts.index, title='Bus Unit Wise', hole=0.7,
                              color_discrete_sequence=px.colors.qualitative.Set2)
    fig_bus_unit_pie.update_traces(textinfo='percent+label', sort=False)
    st.plotly_chart(fig_bus_unit_pie)

    # Display Business Unit TCV trends
    st.subheader("Business Unit Trends")
    fig_bar = px.bar(data_frame=table.sort_values(by='TCV', ascending=False), y='Bus_Unit', x='TCV', orientation='h', title='Business Unit Trends')
    st.plotly_chart(fig_bar)

if __name__ == '__main__':
    dashboard()
