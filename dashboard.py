"""
Simple Streamlit Dashboard for Enhanced Pool Listener
Run with: streamlit run dashboard.py
"""

import streamlit as st
import pandas as pd
import sqlite3
import json
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go

# Configure page
st.set_page_config(
    page_title="🏊 Pool Listener Dashboard",
    page_icon="🏊",
    layout="wide"
)

def load_data():
    """Load data from SQLite database"""
    try:
        conn = sqlite3.connect('pool_listener.db')
        
        # Load pools data
        pools_df = pd.read_sql_query("""
            SELECT * FROM discovered_pools 
            ORDER BY discovered_at DESC
        """, conn)
        
        # Load notifications data  
        notifications_df = pd.read_sql_query("""
            SELECT * FROM notification_log 
            ORDER BY sent_at DESC
        """, conn)
        
        conn.close()
        return pools_df, notifications_df
    except Exception as e:
        st.error(f"Database error: {e}")
        return pd.DataFrame(), pd.DataFrame()

def main():
    st.title("🏊 Enhanced Pool Listener Dashboard")
    st.markdown("---")
    
    # Load data
    pools_df, notifications_df = load_data()
    
    if pools_df.empty:
        st.warning("No data available. Make sure the Enhanced Pool Listener is running.")
        return
    
    # Metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Pools", len(pools_df))
    
    with col2:
        tradeable_count = len(pools_df[pools_df['is_tradeable'] == True])
        st.metric("Tradeable Pools", tradeable_count)
    
    with col3:
        total_notifications = len(notifications_df)
        st.metric("Notifications Sent", total_notifications)
    
    with col4:
        if not pools_df.empty:
            avg_liquidity = pools_df['current_liquidity'].mean()
            st.metric("Avg Liquidity", f"{avg_liquidity:,.0f}")
    
    st.markdown("---")
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Pool Discovery Timeline")
        if not pools_df.empty:
            pools_df['discovered_at'] = pd.to_datetime(pools_df['discovered_at'])
            daily_pools = pools_df.groupby(pools_df['discovered_at'].dt.date).size()
            
            fig = px.line(x=daily_pools.index, y=daily_pools.values,
                         title="Pools Discovered Per Day")
            fig.update_layout(xaxis_title="Date", yaxis_title="Pools")
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("💰 Liquidity Distribution")
        if not pools_df.empty:
            fig = px.histogram(pools_df, x='current_liquidity', nbins=20,
                             title="Pool Liquidity Distribution")
            fig.update_layout(xaxis_title="Liquidity", yaxis_title="Count")
            st.plotly_chart(fig, use_container_width=True)
    
    # Tables
    st.subheader("🏊 Recent Pools")
    if not pools_df.empty:
        display_pools = pools_df.head(10)[['address', 'fee', 'current_liquidity', 'is_tradeable', 'discovered_at']]
        display_pools['current_liquidity'] = display_pools['current_liquidity'].apply(lambda x: f"{x:,}")
        st.dataframe(display_pools, use_container_width=True)
    
    st.subheader("📧 Recent Notifications")
    if not notifications_df.empty:
        display_notifications = notifications_df.head(10)[['pool_address', 'notification_type', 'success', 'sent_at']]
        st.dataframe(display_notifications, use_container_width=True)
    
    # Auto-refresh
    st.sidebar.button("🔄 Refresh Data")
    auto_refresh = st.sidebar.checkbox("Auto Refresh (30s)")
    
    if auto_refresh:
        import time
        time.sleep(30)
        st.experimental_rerun()

if __name__ == "__main__":
    main() 