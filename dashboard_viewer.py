#!/usr/bin/env python3
"""
Simple Dashboard Viewer for Retail Data Warehouse
Alternative to Metabase - uses Streamlit for web interface
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import mysql.connector
from config.database_config import get_connection_params
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

st.set_page_config(
    page_title="Retail Data Warehouse Dashboard",
    page_icon="📊",
    layout="wide"
)

@st.cache_data
def load_data_from_mysql():
    """Load data from MySQL database"""
    try:
        db_params = get_connection_params()
        conn = mysql.connector.connect(**db_params)
        
        # Load all tables
        queries = {
            'transactions': "SELECT * FROM transactions LIMIT 1000",
            'customers': "SELECT * FROM customers",
            'products': "SELECT * FROM products LIMIT 500",
            'monthly_summary': "SELECT * FROM monthly_summary"
        }
        
        data = {}
        for table, query in queries.items():
            data[table] = pd.read_sql(query, conn)
        
        conn.close()
        return data
    except Exception as e:
        st.error(f"Error connecting to database: {e}")
        return None

def main():
    st.title("🏪 Retail Data Warehouse Dashboard")
    st.markdown("---")
    
    # Load data
    data = load_data_from_mysql()
    
    if data is None:
        st.error("Could not connect to database. Please check your connection.")
        return
    
    # Sidebar
    st.sidebar.title("📊 Dashboard Controls")
    
    # Main metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_revenue = data['monthly_summary']['total_revenue'].sum()
        st.metric("Total Revenue", f"${total_revenue:,.2f}")
    
    with col2:
        total_customers = len(data['customers'])
        st.metric("Total Customers", f"{total_customers:,}")
    
    with col3:
        total_products = len(data['products'])
        st.metric("Total Products", f"{total_products:,}")
    
    with col4:
        avg_order_value = data['monthly_summary']['avg_order_value'].mean()
        st.metric("Avg Order Value", f"${avg_order_value:.2f}")
    
    st.markdown("---")
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📅 Monthly Revenue Trend")
        monthly_chart = px.line(
            data['monthly_summary'], 
            x='year_month', 
            y='total_revenue',
            title="Revenue Over Time"
        )
        monthly_chart.update_layout(height=400)
        st.plotly_chart(monthly_chart, use_container_width=True)
    
    with col2:
        st.subheader("👥 Customer Segmentation")
        customer_segments = data['customers']['customer_segment'].value_counts()
        segment_chart = px.pie(
            values=customer_segments.values,
            names=customer_segments.index,
            title="Customer Distribution by Segment"
        )
        segment_chart.update_layout(height=400)
        st.plotly_chart(segment_chart, use_container_width=True)
    
    # Product performance
    st.subheader("🏆 Top 10 Products by Revenue")
    top_products = data['products'].nlargest(10, 'total_revenue')
    product_chart = px.bar(
        top_products,
        x='product_name',
        y='total_revenue',
        title="Top Products by Revenue"
    )
    product_chart.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(product_chart, use_container_width=True)
    
    # Customer analysis
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("💰 Customer Revenue Distribution")
        revenue_hist = px.histogram(
            data['customers'],
            x='total_revenue',
            nbins=30,
            title="Customer Revenue Distribution"
        )
        st.plotly_chart(revenue_hist, use_container_width=True)
    
    with col2:
        st.subheader("📦 Product Category Performance")
        category_revenue = data['products'].groupby('category')['total_revenue'].sum().reset_index()
        category_chart = px.bar(
            category_revenue,
            x='category',
            y='total_revenue',
            title="Revenue by Category"
        )
        st.plotly_chart(category_chart, use_container_width=True)
    
    # Data tables
    st.markdown("---")
    st.subheader("📋 Data Tables")
    
    tab1, tab2, tab3, tab4 = st.tabs(["Transactions", "Customers", "Products", "Monthly Summary"])
    
    with tab1:
        st.dataframe(data['transactions'].head(100))
    
    with tab2:
        st.dataframe(data['customers'])
    
    with tab3:
        st.dataframe(data['products'].head(100))
    
    with tab4:
        st.dataframe(data['monthly_summary'])

if __name__ == "__main__":
    main()
