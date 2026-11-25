import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="Test dashboard", layout="wide")
st.title("Můj první Streamlit dashboard")

n = st.sidebar.slider("Počet dní", 7, 365, 90)

dates = pd.date_range("2026-01-01", periods=n)
df = pd.DataFrame({
    "datum": dates,
    "spotřeba": np.random.randn(n).cumsum() + 100,
})

st.metric("Průměrná spotřeba", f"{df['spotřeba'].mean():.1f}")
st.plotly_chart(px.line(df, x="datum", y="spotřeba"), use_container_width=True)
st.dataframe(df)