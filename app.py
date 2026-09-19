import streamlit as st
import duckdb
import plotly.express as px

# -----------------------------
# PAGE SETUP
# -----------------------------

st.set_page_config(
    page_title="TravelLens ✈️",
    page_icon="✈️",
    layout="wide"
)

# -----------------------------
# CUSTOM STYLE
# -----------------------------

st.markdown("""
<style>

.stApp {
    background: linear-gradient(135deg, #fff7d6 0%, #e8f7ff 45%, #f8e8ff 100%);
}

.main-title {
    font-size: 58px;
    font-weight: 800;
    text-align: center;
    color: #5b4b8a;
    margin-bottom: 0;
}

.subtitle {
    text-align: center;
    font-size: 21px;
    color: #756b85;
    margin-bottom: 25px;
}

.travel-note {
    background: #ffffffcc;
    padding: 18px;
    border-radius: 20px;
    text-align: center;
    font-size: 17px;
    box-shadow: 0 5px 20px #00000012;
    margin-bottom: 25px;
}

.metric-card {
    background: white;
    padding: 20px;
    border-radius: 24px;
    text-align: center;
    box-shadow: 0 6px 20px #00000012;
    border: 2px solid #ffffff;
}

.section-title {
    color: #5b4b8a;
    font-size: 27px;
    font-weight: 700;
    margin-top: 25px;
}

.footer {
    text-align: center;
    color: #756b85;
    padding: 30px;
    font-size: 15px;
}

</style>
""", unsafe_allow_html=True)


# -----------------------------
# DATABASE
# -----------------------------

con = duckdb.connect("travellens.duckdb")
airlines = con.execute("""
    SELECT DISTINCT AIRLINE
    FROM flights_cleaned
    ORDER BY AIRLINE
""").fetchdf()["AIRLINE"].tolist()

airlines.insert(0, "All Airlines")
st.sidebar.title("🎒 Explore TravelLens")

selected_airline = st.sidebar.selectbox(
    "✈️ Choose an airline",
    airlines
)


# -----------------------------
# HEADER
# -----------------------------

st.markdown(
    '<div class="main-title">✈️ TravelLens 🌈</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">A colourful little journey through flight data ☁️🗺️</div>',
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="travel-note">
    🎒 Pack your curiosity and explore the hidden stories inside
    thousands of flights from 2015.
    </div>
    """,
    unsafe_allow_html=True
)


# -----------------------------
# METRICS
# -----------------------------

if selected_airline == "All Airlines":
    total_flights = con.execute("""
        SELECT COUNT(*)
        FROM flights_cleaned
    """).fetchone()[0]
else:
    total_flights = con.execute("""
        SELECT COUNT(*)
        FROM flights_cleaned
        WHERE AIRLINE = ?
    """, [selected_airline]).fetchone()[0]
if selected_airline == "All Airlines":
    avg_delay = con.execute("""
        SELECT AVG(ARRIVAL_DELAY)
        FROM flights_cleaned
        WHERE CANCELLED = 0
    """).fetchone()[0]
else:
    avg_delay = con.execute("""
        SELECT AVG(ARRIVAL_DELAY)
        FROM flights_cleaned
        WHERE CANCELLED = 0
        AND AIRLINE = ?
    """, [selected_airline]).fetchone()[0]

if selected_airline == "All Airlines":
    cancelled_flights = con.execute("""
        SELECT COUNT(*)
        FROM flights_cleaned
        WHERE CANCELLED = 1
    """).fetchone()[0]
else:
    cancelled_flights = con.execute("""
        SELECT COUNT(*)
        FROM flights_cleaned
        WHERE CANCELLED = 1
        AND AIRLINE = ?
    """, [selected_airline]).fetchone()[0]


col1, col2, col3 = st.columns(3)

with col1:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.metric("✈️ Flights Explored", total_flights)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.metric("⏱️ Average Delay", f"{avg_delay:.1f} min")
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.metric("❌ Cancelled Flights", cancelled_flights)
    st.markdown('</div>', unsafe_allow_html=True)


# -----------------------------
# DELAY CHART
# -----------------------------

st.markdown(
    '<div class="section-title">☁️ Who experienced the most delays?</div>',
    unsafe_allow_html=True
)

if selected_airline == "All Airlines":
    delay_data = con.execute("""
        SELECT
            AIRLINE,
            AVG(ARRIVAL_DELAY) AS AVG_DELAY
        FROM flights_cleaned
        WHERE CANCELLED = 0
        GROUP BY AIRLINE
        ORDER BY AVG_DELAY DESC
    """).fetchdf()
else:
    delay_data = con.execute("""
        SELECT
            AIRLINE,
            AVG(ARRIVAL_DELAY) AS AVG_DELAY
        FROM flights_cleaned
        WHERE CANCELLED = 0
        AND AIRLINE = ?
        GROUP BY AIRLINE
    """, [selected_airline]).fetchdf()

fig1 = px.bar(
    delay_data,
    x="AIRLINE",
    y="AVG_DELAY",
    title="Average Arrival Delay by Airline",
    labels={
        "AIRLINE": "Airline",
        "AVG_DELAY": "Average Delay (minutes)"
    }
)

fig1.update_layout(
    plot_bgcolor="rgba(255,255,255,0.7)",
    paper_bgcolor="rgba(255,255,255,0)",
    title_x=0.5
)

st.plotly_chart(fig1, use_container_width=True)


# -----------------------------
# CANCELLATION CHART
# -----------------------------

st.markdown(
    '<div class="section-title">🌧️ Where did cancellations happen?</div>',
    unsafe_allow_html=True
)

if selected_airline == "All Airlines":
    cancel_data = con.execute("""
        SELECT
            AIRLINE,
            COUNT(*) AS CANCELLED_FLIGHTS
        FROM flights_cleaned
        WHERE CANCELLED = 1
        GROUP BY AIRLINE
        ORDER BY CANCELLED_FLIGHTS DESC
    """).fetchdf()
else:
    cancel_data = con.execute("""
        SELECT
            AIRLINE,
            COUNT(*) AS CANCELLED_FLIGHTS
        FROM flights_cleaned
        WHERE CANCELLED = 1
        AND AIRLINE = ?
        GROUP BY AIRLINE
    """, [selected_airline]).fetchdf()

fig2 = px.bar(
    cancel_data,
    x="AIRLINE",
    y="CANCELLED_FLIGHTS",
    title="Cancelled Flights by Airline",
    labels={
        "AIRLINE": "Airline",
        "CANCELLED_FLIGHTS": "Cancelled Flights"
    }
)

fig2.update_layout(
    plot_bgcolor="rgba(255,255,255,0.7)",
    paper_bgcolor="rgba(255,255,255,0)",
    title_x=0.5
)

st.plotly_chart(fig2, use_container_width=True)


# -----------------------------
# ROUTE CHART
# -----------------------------

st.markdown(
    '<div class="section-title">🗺️ Where are travellers flying?</div>',
    unsafe_allow_html=True
)

route_data = con.execute("""
    SELECT
        ORIGIN_AIRPORT || ' → ' || DESTINATION_AIRPORT AS ROUTE,
        COUNT(*) AS FLIGHT_COUNT
    FROM flights_cleaned
    GROUP BY ORIGIN_AIRPORT, DESTINATION_AIRPORT
    ORDER BY FLIGHT_COUNT DESC
    LIMIT 5
""").fetchdf()

fig3 = px.bar(
    route_data,
    x="FLIGHT_COUNT",
    y="ROUTE",
    orientation="h",
    title="Top 5 Busiest Flight Routes",
    labels={
        "ROUTE": "Route",
        "FLIGHT_COUNT": "Number of Flights"
    }
)

fig3.update_layout(
    plot_bgcolor="rgba(255,255,255,0.7)",
    paper_bgcolor="rgba(255,255,255,0)",
    title_x=0.5
)

st.plotly_chart(fig3, use_container_width=True)


# -----------------------------
# FOOTER
# -----------------------------

st.markdown(
    """
    <div class="footer">
    🌤️ TravelLens · Follow the data, discover the journey ✈️
    </div>
    """,
    unsafe_allow_html=True
)