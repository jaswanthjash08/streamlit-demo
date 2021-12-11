import streamlit as st


def write(df):
    st.header("Listing Locations")
    st.markdown(
        "We could filter by listing **price**, **minimum nights** on a listing or minimum of **reviews** received, **neighborhood** and **room type**. ")

    values = st.slider("Price Range ($)", float(df.price.min()), float(
        df.price.clip(upper=10000.).max()), (500., 1500.))
    min_nights_values = st.slider('Minimum Nights', 0, 30, (1))
    reviews = st.slider('Minimum Reviews', 0, 700, (0))
    neighborhood_val = st.selectbox(
        "Neighborhood", df.neighbourhood.unique(), (2))
    room_type_val = st.selectbox("Room type", df.room_type.unique(), (0))
    st.map(df.query(f"price.between{values} and minimum_nights<={min_nights_values} and number_of_reviews>={reviews} and neighbourhood=='{neighborhood_val}' and room_type=='{room_type_val}'")[
           ["latitude", "longitude"]].dropna(how="any"), zoom=11)
