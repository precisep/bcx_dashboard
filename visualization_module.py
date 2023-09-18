import streamlit as st
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go

def display_kpis(data):
    data['TCV'] = pd.to_numeric(data['TCV'], errors='coerce')
    num_deal_won = data[data['Range'] == 'Won'].shape[0]
    num_deal_lost = data[data['Range'] == 'Lost'].shape[0]
    data['TCV'] = pd.to_numeric(data['TCV'], errors='coerce')
    total_tcv_won = data[data['Range'] == 'Won']['TCV'].sum() / 1000000000
    total_tcv_lost = data[data['Range'] == 'Lost']['TCV'].sum() / 1000000000
    total_tcv = data['TCV'].sum() / 1000000000

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


def display_business_unit(data, selected_range):

    if selected_range == 'All':

        range_counts = data['Bus_Unit'].value_counts()
        fig_bus_unit_pie = px.pie(
            values=range_counts.values,
            names=range_counts.index,
            title='Bus Unit Wise',
            hole=0.7,
            color_discrete_sequence=px.colors.qualitative.Set2,
            labels={'Bus_Unit': 'Business Unit'},
            template='plotly'
        )

        fig_bar = px.bar(
            data_frame=data.sort_values(by='TCV', ascending=False),
            y='Bus_Unit',
            x='TCV',
            orientation='h',
            title='Business Unit Trends'
        )
        
        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(fig_bus_unit_pie, use_container_width=True)

        with col2:
            st.plotly_chart(fig_bar, use_container_width=True)
    else:

        range_counts = data[data['Range'] == selected_range]['Bus_Unit'].value_counts()
        fig_bus_unit_pie = px.pie(
            values=range_counts.values,
            names=range_counts.index,
            title=f'Bus Unit Wise ({selected_range} Only)',
            hole=0.7,
            color_discrete_sequence=px.colors.qualitative.Set2,
            labels={'Bus_Unit': 'Business Unit'},
            template='plotly'
        )

        fig_bar = px.bar(
            data_frame=data.sort_values(by='TCV', ascending=False),
            y='Bus_Unit',
            x='TCV',
            orientation='h',
            title='Business Unit Trends'
        )

        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(fig_bus_unit_pie, use_container_width=True)

        with col2:
            st.plotly_chart(fig_bar, use_container_width=True)





def display_gtm1(data, selected_range):
    if selected_range == 'All':
      
        sorted_data = data.sort_values(by='TCV', ascending=False)

        fig_gtm1_bar = go.Figure()

        for status, color in zip(['Won', 'Lost'], ['#66c2a5', '#fc8d62']):
            filtered_data = sorted_data[sorted_data['Range'] == status]
            fig_gtm1_bar.add_trace(go.Bar(
                y=filtered_data['GTM1'],
                x=filtered_data['TCV'],
                orientation='h',
                name=status,
                marker_color=color
            ))

        fig_gtm1_bar.update_layout(
            title='GTM1 Trends (Combined TCV)',
            xaxis_title='Total Contract Value',
            yaxis_title='GTM1',
            barmode='stack'
        )
    else:
        filtered_data = data[data['Range'].isin(['Won', 'Lost'])]

        sorted_data = filtered_data.sort_values(by='TCV', ascending=False)

        fig_gtm1_bar = go.Figure()


        for status, color in zip(['Won', 'Lost'], ['#66c2a5', '#fc8d62']):
            filtered_data = sorted_data[sorted_data['Range'] == status]
            fig_gtm1_bar.add_trace(go.Bar(
                y=filtered_data['GTM1'],
                x=filtered_data['TCV'],
                orientation='h',
                name=status,
                marker_color=color
            ))

        fig_gtm1_bar.update_layout(
            title=f'GTM1 Trends ({selected_range} Only)',
            xaxis_title='Total Contract Value',
            yaxis_title='GTM1',
            barmode='stack'
        )

    st.plotly_chart(fig_gtm1_bar, use_container_width=True)

def display_gtm2(data, selected_range):
    if selected_range == 'All':
        sorted_data = data.sort_values(by='TCV', ascending=False)

        fig_gtm1_bar = go.Figure()

        for status, color in zip(['Won', 'Lost'], ['#66c3a5', '#fc7d62']):
            filtered_data = sorted_data[sorted_data['Range'] == status]
            fig_gtm1_bar.add_trace(go.Bar(
                y=filtered_data['GTM2'],
                x=filtered_data['TCV'],
                orientation='h',
                name=status,
                marker_color=color
            ))

        fig_gtm1_bar.update_layout(
            title='GTM1 Trends (Combined TCV)',
            xaxis_title='Total Contract Value',
            yaxis_title='GTM2',
            barmode='stack'
        )
    else:
        filtered_data = data[data['Range'].isin(['Won', 'Lost'])]

        sorted_data = filtered_data.sort_values(by='TCV', ascending=False)

        fig_gtm1_bar = go.Figure()

        for status, color in zip(['Won', 'Lost'], ['#66c3a5', '#fc7d62']):
            filtered_data = sorted_data[sorted_data['Range'] == status]
            fig_gtm1_bar.add_trace(go.Bar(
                y=filtered_data['GTM2'],
                x=filtered_data['TCV'],
                orientation='h',
                name=status,
                marker_color=color
            ))

        fig_gtm1_bar.update_layout(
            title=f'GTM2 Trends ({selected_range} Only)',
            xaxis_title='Total Contract Value',
            yaxis_title='GTM2',
            barmode='stack'
        )

    st.plotly_chart(fig_gtm1_bar, use_container_width=True)



