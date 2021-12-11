import streamlit as st


def write(df):
    st.title("Airbnb listings Data Analysis")
    st.markdown('-----------------------------------------------------')

    st.markdown(
        "*Through Airbnb data we will conduct an exploratory analysis and offer insights into that data. For this we will use the data publicly available information on the Airbnb website available [here](http://insideairbnb.com/london/)*")

    st.header("Summary")

    st.markdown("Airbnb is a platform that provides and guides the opportunity to link two groups - the hosts and the guests. Anyone with an open room or free space can provide services on Airbnb to the global community. It is a good way to provide extra income with minimal effort. It is an easy way to advertise space, because the platform has traffic and a global user base to support it. Airbnb offers hosts an easy way to monetize space that would be wasted.")

    st.markdown("On the other hand, we have guests with very specific needs - some may be looking for affordable accommodation close to the city's attractions, while others are a luxury apartment by the sea. They can be groups, families or local and foreign individuals. After each visit, guests have the opportunity to rate and stay with their comments. We will try to find out what contributes to the listing's popularity and predict whether the listing has the potential to become one of the 100 most reviewed accommodations based on its attributes.")

    st.markdown('-----------------------------------------------------')

    st.header("Airbnb New York Listings: Data Analysis")
    st.markdown("Following is presented the first 10 records of Airbnb data. These records are grouped along 16 columns with a variety of informations as host name, price, room type, minimum of nights,reviews and reviews per month.")
    st.markdown("We will start with familiarizing ourselves with the columns in the dataset, to understand what each feature represents.")
    st.dataframe(df.head(10))
    st.markdown("")
