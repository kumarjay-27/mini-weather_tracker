"""
STREAMLIT WEATHER DASHBOARD
Run with: streamlit run dashboard.py
"""

import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from minitracker import setup_database, run_pipeline
DB_FILE = "weather.db"

# Initialize database and create weather table if needed
setup_database()

# PAGE CONFIG
st.set_page_config(
    page_title="Weather Tracker",
    page_icon="🌤️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CUSTOM CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1E3A8A;
        text-align: center;
        margin-bottom: 1rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)


# LOAD DATA FROM DATABASE
@st.cache_data(ttl=60)  # Cache for 60 seconds
def load_weather_data():
    """Fetch latest weather data from SQLite database."""
    conn = sqlite3.connect(DB_FILE)
    
    query = """
    SELECT w1.city,
           w1.country,
           w1.temperature,
           w1.feels_like,
           w1.humidity,
           w1.description,
           w1.wind_speed,
           w1.fetched_at
    FROM weather w1
    WHERE w1.fetched_at = (
        SELECT MAX(w2.fetched_at)
        FROM weather w2
        WHERE w2.city = w1.city
    )
    ORDER BY w1.temperature DESC
"""
    
    df = pd.read_sql_query(query, conn)
    conn.close()
    
    return df


def load_historical_data():
    """Load all historical weather records."""
    conn = sqlite3.connect(DB_FILE)
    query = "SELECT * FROM weather ORDER BY fetched_at DESC LIMIT 100"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df


# MAIN APP
def main():
    # HEADER
    st.markdown('<h1 class="main-header">🌤️ Weather Tracker Dashboard</h1>', 
                unsafe_allow_html=True)
    
    # SIDEBAR
    with st.sidebar:
        st.header("⚙️ Controls")
        
        if st.button("🌤️ Fetch Latest Weather", use_container_width=True):
          with st.spinner("Fetching weather data..."):
           run_pipeline()

          st.cache_data.clear()
          st.success("Weather data updated successfully!")
          st.rerun()
        
        st.markdown("---")
        st.markdown("### 📊 Dashboard Info")
        st.info("Live weather data for multiple cities. Updates every 60 seconds.")
        
        # Auto-refresh toggle
        auto_refresh = st.checkbox("Auto-refresh (60s)", value=False)
        
        if auto_refresh:
            import time
            time.sleep(60)
            st.rerun()
    
    # LOAD DATA FROM THE WEATHER_DB
    try:
        df = load_weather_data()
        
        if df.empty:
           st.warning("⚠️ No weather data available yet.")
           st.info("Click **🌤️ Fetch Latest Weather** in the sidebar to fetch live weather data.")
           return
        
    except Exception as e:
        st.error(f"❌ Error loading data: {e}")
        st.info("Make sure `weather.db` exists. Run the pipeline script first!")
        return
    
    # LAST UPDATED TIME
    last_update = df['fetched_at'].iloc[0] if not df.empty else "N/A"
    st.caption(f"🕐 Last updated: {last_update}")
    
    # KEY METRICS (Top Row)
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        hottest = df.loc[df['temperature'].idxmax()]
        st.metric(
            label="🔥 Hottest City",
            value=f"{hottest['city']}",
            delta=f"{hottest['temperature']}°C"
        )
    
    with col2:
        coldest = df.loc[df['temperature'].idxmin()]
        st.metric(
            label="❄️ Coldest City",
            value=f"{coldest['city']}",
            delta=f"{coldest['temperature']}°C"
        )
    
    with col3:
        avg_temp = round(df['temperature'].mean(), 1)
        st.metric(
            label="📊 Average Temp",
            value=f"{avg_temp}°C",
            delta=f"{len(df)} cities"
        )
    
    with col4:
        avg_humidity = round(df['humidity'].mean(), 0)
        st.metric(
            label="💧 Avg Humidity",
            value=f"{avg_humidity}%",
            delta=f"{df['wind_speed'].mean():.1f} m/s wind"
        )
    
    st.markdown("---")
    
    # MAIN CONTENT - TWO COLUMNS
    col_left, col_right = st.columns([2, 1])
    
    with col_left:
        st.subheader("🌡️ Temperature Comparison")
        
        # Temperature bar chart
        fig = px.bar(
            df,
            x='city',
            y='temperature',
            color='temperature',
            color_continuous_scale='RdYlBu_r',
            text='temperature',
            labels={'temperature': 'Temperature (°C)', 'city': 'City'},
            title="Current Temperature by City"
        )
        
        fig.update_traces(texttemplate='%{text}°C', textposition='outside')
        fig.update_layout(showlegend=False, height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col_right:
        st.subheader("💨 Wind Speed")
        
        # Wind speed gauge (example for one city)
        fig_wind = go.Figure(go.Indicator(
            mode="gauge+number",
            value=df['wind_speed'].mean(),
            title={'text': "Avg Wind Speed (m/s)"},
            gauge={
                'axis': {'range': [0, 20]},
                'bar': {'color': "#667eea"},
                'steps': [
                    {'range': [0, 5], 'color': "#E0F2FE"},
                    {'range': [5, 10], 'color': "#BAE6FD"},
                    {'range': [10, 20], 'color': "#7DD3FC"}
                ],
            }
        ))
        
        fig_wind.update_layout(height=300)
        st.plotly_chart(fig_wind, use_container_width=True)
    
    st.markdown("---")
    
    # DETAILED CITY DATA
    st.subheader("📍 Detailed Weather by City")
    
    # City selector
    selected_cities = st.multiselect(
        "Select cities to compare:",
        options=df['city'].tolist(),
        default=df['city'].tolist()[:3]
    )
    
    if selected_cities:
        filtered_df = df[df['city'].isin(selected_cities)]
        
        # Create weather cards
        cols = st.columns(len(selected_cities))
        
        for idx, (_, row) in enumerate(filtered_df.iterrows()):
            with cols[idx]:
                st.markdown(f"""
                    <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                                padding: 1.5rem; border-radius: 10px; color: white;'>
                        <h3 style='margin:0; color: white;'>📍 {row['city']}, {row['country']}</h3>
                        <h1 style='margin: 0.5rem 0; color: white;'>{row['temperature']}°C</h1>
                        <p style='margin: 0.2rem 0;'>Feels like: {row['feels_like']}°C</p>
                        <p style='margin: 0.2rem 0;'>💧 {row['humidity']}% humidity</p>
                        <p style='margin: 0.2rem 0;'>💨 {row['wind_speed']} m/s wind</p>
                        <p style='margin: 0.5rem 0; font-style: italic;'>☁️ {row['description']}</p>
                    </div>
                """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.subheader("🔬 Temperature vs Humidity Analysis")
    
    fig_scatter = px.scatter(
        df,
        x='temperature',
        y='humidity',
        size='wind_speed',
        color='city',
        hover_data=['description', 'feels_like'],
        labels={
            'temperature': 'Temperature (°C)',
            'humidity': 'Humidity (%)',
            'wind_speed': 'Wind Speed (m/s)'
        },
        title="Temperature vs Humidity with Wind Speed"
    )
    
    fig_scatter.update_layout(height=400)
    st.plotly_chart(fig_scatter, use_container_width=True)
    
    st.markdown("---")
    
    # RAW DATA TABLE
    with st.expander("📊 View Raw Data"):
        st.dataframe(
            df.style.background_gradient(subset=['temperature'], cmap='RdYlBu_r'),
            use_container_width=True
        )
        csv = df.to_csv(index=False)
        st.download_button(
            label="📥 Download CSV",
            data=csv,
            file_name=f"weather_data_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
            mime="text/csv"
        )
    
    # HISTORICAL DATA (if available)
    st.markdown("---")
    st.subheader("📈 Historical Trends")
    
    try:
        hist_df = load_historical_data()
        
        if not hist_df.empty and len(hist_df) > 5:
            # Convert fetched_at to datetime
            hist_df['fetched_at'] = pd.to_datetime(hist_df['fetched_at'])
            
            # Temperature trend over time
            fig_trend = px.line(
                hist_df,
                x='fetched_at',
                y='temperature',
                color='city',
                markers=True,
                labels={
                    'fetched_at': 'Time',
                    'temperature': 'Temperature (°C)'
                },
                title="Temperature Trends Over Time"
            )
            
            fig_trend.update_layout(height=400)
            st.plotly_chart(fig_trend, use_container_width=True)
        else:
            st.info("📊 Not enough historical data yet. Run the pipeline multiple times to see trends!")
    
    except Exception as e:
        st.warning(f"Historical data unavailable: {e}")
    
    # FOOTER
    st.markdown("---")
    st.caption("Built with ❤️ using Streamlit | Data from OpenWeatherMap API")


if __name__ == "__main__":
    main()