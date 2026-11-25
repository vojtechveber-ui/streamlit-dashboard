import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title="Veber | Vypracovaný úkol",
    page_icon="📊",
    layout="wide",
)


@st.cache_data
def load_data() -> pd.DataFrame:
    rng = np.random.default_rng(42)
    dates = pd.date_range("2025-01-01", periods=365)
    return pd.DataFrame({
        "datum": dates,
        "hodnota": rng.normal(0, 1, len(dates)).cumsum() + 100,
        "kategorie": rng.choice(["A", "B", "C"], len(dates)),
    })


df = load_data()

st.sidebar.header("Filtry")
kategorie = st.sidebar.multiselect(
    "Kategorie", sorted(df["kategorie"].unique()), default=sorted(df["kategorie"].unique())
)
od, do = st.sidebar.date_input(
    "Období", (df["datum"].min().date(), df["datum"].max().date())
)

filtered = df[
    df["kategorie"].isin(kategorie)
    & (df["datum"].dt.date >= od)
    & (df["datum"].dt.date <= do)
]

st.title("Vypracovaný úkol")
st.caption("Vojtěch Veber · datová analýza")

tab_zadani, tab_data, tab_analyza, tab_zavery = st.tabs(
    ["Zadání", "Data", "Analýza", "Závěry"]
)

with tab_zadani:
    st.subheader("Zadání")
    st.write("Stručné shrnutí zadání a použitých předpokladů.")

with tab_data:
    st.subheader("Přehled dat")
    c1, c2, c3 = st.columns(3)
    c1.metric("Počet záznamů", f"{len(filtered):,}".replace(",", " "))
    c2.metric("Průměr", f"{filtered['hodnota'].mean():.1f}")
    c3.metric("Maximum", f"{filtered['hodnota'].max():.1f}")
    st.dataframe(filtered, hide_index=True)

with tab_analyza:
    st.subheader("Vývoj v čase")
    fig = px.line(filtered, x="datum", y="hodnota", color="kategorie")
    st.plotly_chart(fig)

with tab_zavery:
    st.subheader("Závěry a doporučení")
    st.write("Hlavní zjištění, interpretace a doporučený postup.")