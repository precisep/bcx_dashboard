import streamlit as st
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go

def format_currency(value):
    if abs(value) >= 1000000000:
        return f'ZAR {value / 1000000000:.2f} B'
    elif abs(value) >= 1000000:
        return f'ZAR {value / 1000000:.2f} M'
    elif abs(value) >= 1000:
        return f'ZAR {value / 1000:.2f} K'
    else:
        return f'ZAR {value:.2f}'


def display_kpis(data):
    data['TCV'] = pd.to_numeric(data['TCV'], errors='coerce')
    num_deal_won = data[data['Range'] == 'Won'].shape[0]
    num_deal_lost = data[data['Range'] == 'Lost'].shape[0]
    total_tcv_won = data[data['Range'] == 'Won']['TCV'].sum()
    total_tcv_lost = data[data['Range'] == 'Lost']['TCV'].sum()
    total_tcv = data['TCV'].sum()

    kpi_col1, kpi_col2, kpi_col3 = st.columns(3)
    with kpi_col1:
        st.metric(label='**Total TCV**', value=format_currency(total_tcv))
    with kpi_col2:
        st.metric(label='**Total TCV Won**', value=format_currency(total_tcv_won), delta_color="inverse")
    with kpi_col3:
        st.metric(label='**Total TCV Lost**', value=format_currency(total_tcv_lost), delta_color="inverse")

    kpi_col4, kpi_col5, kpi_col6 = st.columns(3)
    with kpi_col4:
        st.metric(label='**Total Deals**', value=num_deal_won + num_deal_lost, delta_color="inverse")
    with kpi_col5:
        st.metric(label='**Number of Deals Won**', value=num_deal_won, delta_color="inverse")
    with kpi_col6:
        st.metric(label='**Number of Deals Lost**', value=num_deal_lost, delta_color="inverse")

def display_account_kpis(account_data):
    account_data['TCV'] = pd.to_numeric(account_data['TCV'], errors='coerce')
    num_deal_won = account_data[account_data['Range'] == 'Won'].shape[0]
    num_deal_lost = account_data[account_data['Range'] == 'Lost'].shape[0]
    total_tcv_won = account_data[account_data['Range'] == 'Won']['TCV'].sum()
    total_tcv_lost = account_data[account_data['Range'] == 'Lost']['TCV'].sum()
    total_tcv = account_data['TCV'].sum()

    kpi_col1, kpi_col2, kpi_col3 = st.columns(3)
    with kpi_col1:
        st.metric(label='Total TCV', value=format_currency(total_tcv))
    with kpi_col2:
        st.metric(label='Total TCV Won', value=format_currency(total_tcv_won), delta_color="inverse")
    with kpi_col3:
        st.metric(label='Total TCV Lost', value=format_currency(total_tcv_lost), delta_color="inverse")

    kpi_col4, kpi_col5, kpi_col6 = st.columns(3)
    with kpi_col4:
        st.metric(label='Total Deals', value=num_deal_won + num_deal_lost, delta_color="inverse")
    with kpi_col5:
        st.metric(label='Number of Deals Won', value=num_deal_won, delta_color="inverse")
    with kpi_col6:
        st.metric(label='Number of Deals Lost', value=num_deal_lost, delta_color="inverse")




def display_business_unit(data, selected_range, selected_account_names):
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

        st.plotly_chart(fig_bus_unit_pie, use_container_width=True)
        st.plotly_chart(fig_bar, use_container_width=True)
    else:
        filtered_data = data[data['Range'] == selected_range]

        range_counts = filtered_data['Bus_Unit'].value_counts()
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
            data_frame=filtered_data.sort_values(by='TCV', ascending=False),
            y='Bus_Unit',
            x='TCV',
            orientation='h',
            title='Business Unit Trends'
        )

        
        st.plotly_chart(fig_bus_unit_pie, use_container_width=True)
        st.plotly_chart(fig_bar, use_container_width=True)

def display_gtm1(data, selected_range, selected_account_names):
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
        filtered_data = data[data['Range'] == selected_range]

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

def display_gtm2(data, selected_range, selected_account_names):
    if selected_range == 'All':
        sorted_data = data.sort_values(by='TCV', ascending=False)

        fig_gtm2_bar = go.Figure()

        for status, color in zip(['Won', 'Lost'], ['#66c3a5', '#fc7d62']):
            filtered_data = sorted_data[sorted_data['Range'] == status]
            fig_gtm2_bar.add_trace(go.Bar(
                y=filtered_data['GTM2'],
                x=filtered_data['TCV'],
                orientation='h',
                name=status,
                marker_color=color
            ))

        fig_gtm2_bar.update_layout(
            title='GTM2 Trends (Combined TCV)',
            xaxis_title='Total Contract Value',
            yaxis_title='GTM2',
            barmode='stack'
        )
    else:
        filtered_data = data[data['Range'] == selected_range]

        sorted_data = filtered_data.sort_values(by='TCV', ascending=False)

        fig_gtm2_bar = go.Figure()

        for status, color in zip(['Won', 'Lost'], ['#66c3a5', '#fc7d62']):
            filtered_data = sorted_data[sorted_data['Range'] == status]
            fig_gtm2_bar.add_trace(go.Bar(
                y=filtered_data['GTM2'],
                x=filtered_data['TCV'],
                orientation='h',
                name=status,
                marker_color=color
            ))

        fig_gtm2_bar.update_layout(
            title=f'GTM2 Trends ({selected_range} Only)',
            xaxis_title='Total Contract Value',
            yaxis_title='GTM2',
            barmode='stack'
        )

    st.plotly_chart(fig_gtm2_bar, use_container_width=True)


def display_business_unit_time_series(data, selected_range, selected_bus_unit=None):
    filtered_data = data.copy()
    if selected_range != 'All':
        filtered_data = filtered_data[filtered_data['Range'] == selected_range]
    if selected_bus_unit and selected_bus_unit != 'All':
        filtered_data = filtered_data[filtered_data['Bus_Unit'] == selected_bus_unit]

    grouped_data = filtered_data.groupby(['First_Schedule_Date', 'Bus_Unit'])['TCV'].sum().reset_index()

    fig = px.line(grouped_data, x='First_Schedule_Date', y='TCV', color='Bus_Unit', title='Business Unit Time Series')
    fig.update_yaxes(range=[100000, grouped_data['TCV'].max()])

    fig.update_xaxes(
        rangeslider_visible=True,
        rangeselector=dict(
            buttons=list([
                dict(count=1, label="1Y", step="year", stepmode="backward"),
                dict(count=3, label="3Y", step="year", stepmode="backward"),
                dict(count=6, label="6Y", step="year", stepmode="backward"),
                dict(step="all"),
            ])
        )
    )

    st.plotly_chart(fig, use_container_width=True)




