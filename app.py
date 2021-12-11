import pydeck as pdk
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import seaborn as sns
import io
sns.set_style("whitegrid")


def get_data():
    return pd.read_csv("data/listings.csv")


def main():
    df = get_data()
    df.drop(['neighbourhood_group'], axis = 1)
    ################################ INTRODUCTION ################################

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
    buffer = io.StringIO()
    df.info(buf=buffer)
    s = buffer.getvalue()

    st.text(s)

    #################### LISTING LOCATIONS ######################

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

    #################### Heat Map ######################
    st.header("Heat Map")
    st.markdown("Heat maps will help the customer determine how busy and active neighborhood are. Small dots indicates neighborhoods that are not rented in often and big dots represents a high number of visits.")
    # st.map(df[["latitude", "longitude"]].dropna(how="any"), zoom=10)

    neighbourhoods = df.groupby("neighbourhood").first().reset_index()
    neighbourhoodvisits = df.groupby(
        "neighbourhood").size().reset_index(name="count")
    heatmap = pd.merge(neighbourhoods, neighbourhoodvisits,
                       on="neighbourhood")[["neighbourhood", "count", "longitude", "latitude"]]

    # Set viewport for the deckgl map
    view = pdk.ViewState(longitude=-0.0775, latitude=51.4975, zoom=10,)
	
    # Create the scatter plot layer
    countLayer = pdk.Layer(
        "ScatterplotLayer",
        data=heatmap,
        pickable=False,
        opacity=0.3,
        stroked=True,
        filled=True,
        radius_scale=10,
        radius_min_pixels=5,
        radius_max_pixels=60,
        line_width_min_pixels=1,
        get_position=["longitude", "latitude"],
        get_radius="count/30",
        get_fill_color=[252, 136, 3],
        get_line_color=[255, 0, 0],
        tooltip="test test",
    )

    # Create the deck.gl map
    r = pdk.Deck(
        layers=[countLayer],
        map_style="mapbox://styles/mapbox/light-v10",
        initial_view_state=view
    )

    # Render the deck.gl map in the Streamlit app as a Pydeck chart
    st.pydeck_chart(r)

    #################### Factors OF INTEREST ######################
    st.header('Factors effecting the price')
    st.subheader('Categorical factors influencing the price')
    st.markdown("Summary information for string features")
    st.dataframe(df.describe(include='object'))

    neighbourhood_listings_fig = plt.figure()
    neighbourhood_listings = df.groupby("neighbourhood").size().reset_index(name="count")
    ax = sns.barplot(x="count", y="neighbourhood", data=neighbourhood_listings)
    ax.set_xlabel(xlabel = 'Count', fontsize = 15)
    ax.set_ylabel(ylabel = 'Neighbourhood', fontsize = 15)
    ax.set_title(label = 'Number of listings by neighbourhood', fontsize = 15)
    st.pyplot(neighbourhood_listings_fig)

    room_type_listings_fig = plt.figure()
    room_type_listings = df.groupby("room_type").size().reset_index(name="count")
    ax = sns.barplot(x="count", y="room_type", data=room_type_listings)
    ax.set_xlabel(xlabel = 'Count', fontsize = 15)
    ax.set_ylabel(ylabel = 'Room type', fontsize = 15)
    ax.set_title(label = 'Number of listings by room type', fontsize = 15)
    st.pyplot(room_type_listings_fig)


    neighbourhood_distribution = plt.figure()
    plt.style.use('ggplot')
    ax = sns.boxplot(x = df['neighbourhood'], y =df['price'], data = df, palette = 'Set3')
    ax.set_xlabel(xlabel = 'Neighbourhood', fontsize = 15)
    ax.set_ylabel(ylabel = 'Price', fontsize = 15)
    ax.set_title(label = 'Distribution of prices across neighbourhood', fontsize = 15)
    plt.xticks(rotation = 90)
    st.pyplot(neighbourhood_distribution)
    st.markdown("""
    <h6>Inference</h6>
    <ul>
      <li>The average prices of Westminster is more and it is low for Enfield and Havering</li>
    </ul>
    """, unsafe_allow_html=True)

    room_type_distribution = plt.figure()
    plt.style.use('ggplot')
    ax = sns.boxplot(x = df['room_type'], y =df['price'], data = df, palette = 'Set3')
    ax.set_xlabel(xlabel = 'Room type', fontsize = 15)
    ax.set_ylabel(ylabel = 'Price', fontsize = 15)
    ax.set_title(label = 'Distribution of prices across room type', fontsize = 15)
    plt.xticks(rotation = 90)
    st.pyplot(room_type_distribution)
    st.markdown("""
    <h6>Inference</h6>
    <ul>
      <li>The average prices of Entire home/apt is more</li>
      <li>The average prices of Shared room is the lowest followed by hotel room</li>
    </ul>
    """, unsafe_allow_html=True)

    st.subheader('Numerical factors influencing the price')
    st.dataframe(df.describe(exclude='object'))
    
    heatmap_fig = plt.figure()
    sns.heatmap(df[[ "name", "host_id", "host_name", "neighbourhood", "latitude", "longitude", "room_type", "price",
                "minimum_nights", "number_of_reviews", "last_review", "reviews_per_month", "calculated_host_listings_count", "availability_365"]].corr(),cmap="YlGnBu", annot=True)
    st.pyplot(heatmap_fig)
    st.markdown("From the correlation heatmap we can see that the facators effecting the price are **calculated_host_listings_count**,**minimum_nights**,**host**")

    ###################### PRICE AVERAGE BY ACOMMODATION #########################

    st.header("Average price by room type")

    st.markdown("To listings based on room type, we can show price average.")

    avg_price_room = df.groupby("room_type").price.mean().reset_index()\
        .round(2).sort_values("price", ascending=False)\
        .assign(avg_price=lambda x: x.pop("price").apply(lambda y: "%.2f" % y))

    avg_price_room = avg_price_room.rename(columns={'room_type':'Room Type', 'avg_price': 'Average Price ($)', })

    st.table(avg_price_room)

    ############################ MOST RATED HOSTS #############################

    st.header("Most rated hosts")


    rankings_fig = plt.figure()
    ranked = df.groupby(['host_name'])['number_of_reviews'].count().sort_values(ascending=False).reset_index()
    ranked = ranked.head(5)
    ax = sns.barplot(x="number_of_reviews", y="host_name", data=ranked)
    ax.set_xlabel(xlabel = 'Number of reviews', fontsize = 15)
    ax.set_ylabel(ylabel = 'Host', fontsize = 15)
    st.pyplot(rankings_fig)

    st.write(f"""The host **{ranked.iloc[0].host_name}** is at the top with {ranked.iloc[0].number_of_reviews} reviews.
    **{ranked.iloc[1].host_name}** is second with {ranked.iloc[1].number_of_reviews} reviews. It should also be noted that reviews are not positive or negative reviews, but a count of feedbacks provided for the accommodation.""")



    ################################### FOOTER #####################

    st.markdown('-----------------------------------------------------')
    st.text('Developed by Rev Munnangi - 2021')
    st.text('Mail: Rev.Munnangi@gmail.com')


if __name__ == '__main__':
    main()
