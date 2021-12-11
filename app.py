import pydeck as pdk
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import seaborn as sns
import intro
import listings
import heatmap
import priceFactors
import insights
import sidebar
import footer

sns.set_style("whitegrid")

PAGES = {
    "Introduction": intro,
    "Accomidation listings or search": listings,
    "Heatmap of accomidations": heatmap,
    "Factors influencing prices": priceFactors,
    "Few more Insights": insights
}


def get_page(page="Introduction"):
    return PAGES[page]


def get_data():
    return pd.read_csv("data/listings.csv")


def main():
    df = get_data()
    df.drop(['neighbourhood_group'], axis=1)
    st.title("Data Exploration on London Airbnb data")
    sidebar.write()
    st.sidebar.title("Navigation")
    selection = st.sidebar.radio("Go to", list(PAGES.keys()))
    page = get_page(selection)
    with st.spinner(f"Loading Page"):
        page.write(df)
        footer.write()


if __name__ == '__main__':
    main()
