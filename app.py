import streamlit as st
import pandas as pd
import plotly.express as px
import joblib

st.set_page_config(layout="wide")

# ==============================
# Dashboard Theme Styling
# ==============================\

st.markdown("""
<style>

.main {
background-color:#f2f2f2;
}

.card {
background-color:white;
padding:18px;
border-radius:10px;
border:1px solid #d9d9d9;
box-shadow:0px 1px 3px rgba(0,0,0,0.08);
}

.metric-title {
font-size:14px;
color:#666;
}

.metric-value {
font-size:30px;
font-weight:600;
color:#14a2a8;
}

.section-title {
font-size:16px;
font-weight:600;
color:#444;
margin-bottom:10px;
}

</style>
""", unsafe_allow_html=True)

# ==============================
# Title
# ==============================

st.title("Dashboard for real time credit card fraud detection")

# ==============================
# Load Data
# ==============================

df = pd.read_csv("data/creditcard.csv")
model = joblib.load("models/fraud_model.pkl")

df["Hour"] = (df["Time"] // 3600) % 24

# ==============================
# KPI Cards
# ==============================

total = len(df)
fraud = df[df["Class"]==1].shape[0]
fraud_amount = df[df["Class"]==1]["Amount"].sum()

k1,k2,k3 = st.columns(3)

with k1:
    st.markdown(f"""
    <div class="card">
    <div class="metric-title">Fraudulent transactions</div>
    <div class="metric-value">{fraud}</div>
    </div>
    """, unsafe_allow_html=True)

with k2:
    st.markdown(f"""
    <div class="card">
    <div class="metric-title">% Fraudulent transactions</div>
    <div class="metric-value">{fraud/total:.4%}</div>
    </div>
    """, unsafe_allow_html=True)

with k3:
    st.markdown(f"""
    <div class="card">
    <div class="metric-title">Total fraud transactions amount</div>
    <div class="metric-value">${fraud_amount:,.0f}</div>
    </div>
    """, unsafe_allow_html=True)

st.write("")

# ==============================
# Row 1
# ==============================

c1,c2,c3 = st.columns(3)

# ------------------------------
# Map
# ------------------------------

with c1:

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Fraudulent transactions by location</div>', unsafe_allow_html=True)

    map_data = pd.DataFrame({
        "lat": 37 + (df.sample(300).index % 10) * 0.1,
        "lon": -95 + (df.sample(300).index % 10) * 0.1
    })

    st.map(map_data)

    st.markdown('</div>', unsafe_allow_html=True)

# ------------------------------
# Category Chart
# ------------------------------

with c2:

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Fraud percentage by category</div>', unsafe_allow_html=True)

    cat = df.groupby("Class")["Amount"].sum().reset_index()

    fig = px.bar(
        cat,
        x="Class",
        y="Amount",
        color="Class",
        color_discrete_sequence=["#14a2a8","#76d7c4"]
    )

    fig.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white"
    )

    st.plotly_chart(fig,use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ------------------------------
# Trend Chart
# ------------------------------

with c3:

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Average fraud percentage by date</div>', unsafe_allow_html=True)

    hour_data = df.groupby("Hour")["Class"].sum().reset_index()

    fig2 = px.line(
        hour_data,
        x="Hour",
        y="Class",
        markers=True,
        color_discrete_sequence=["#14a2a8"]
    )

    fig2.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white"
    )

    st.plotly_chart(fig2,use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ==============================
# Row 2
# ==============================

c4,c5 = st.columns(2)

# ------------------------------
# Risk Chart
# ------------------------------

with c4:

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Fraud percentage by risk</div>', unsafe_allow_html=True)

    risk = pd.DataFrame({
        "Risk":["High Risk","Medium Risk","Low Risk"],
        "Fraud":[60,30,10]
    })

    fig3 = px.bar(
        risk,
        x="Risk",
        y="Fraud",
        color="Risk",
        color_discrete_sequence=["#14a2a8","#76d7c4","#c9f0e9"]
    )

    fig3.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white"
    )

    st.plotly_chart(fig3,use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ------------------------------
# Fraud Table
# ------------------------------

with c5:

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Fraudulent transactions at merchant</div>', unsafe_allow_html=True)

    fraud_df = df[df["Class"]==1].head(10)

    st.dataframe(fraud_df)

    st.markdown('</div>', unsafe_allow_html=True)