import matplotlib.pyplot as plt
import streamlit as st
import seaborn as sns
sns.set_style("whitegrid")


def write(df):
    st.header('Factors effecting the price')
    st.subheader('Categorical factors influencing the price')
    st.markdown("Summary information for string features")
    st.dataframe(df.describe(include='object'))

    neighbourhood_listings_fig = plt.figure()
    neighbourhood_listings = df.groupby(
        "neighbourhood").size().reset_index(name="count")
    ax = sns.barplot(x="count", y="neighbourhood", data=neighbourhood_listings)
    ax.set_xlabel(xlabel='Count', fontsize=15)
    ax.set_ylabel(ylabel='Neighbourhood', fontsize=15)
    ax.set_title(label='Number of listings by neighbourhood', fontsize=15)
    st.pyplot(neighbourhood_listings_fig)

    room_type_listings_fig = plt.figure()
    room_type_listings = df.groupby(
        "room_type").size().reset_index(name="count")
    ax = sns.barplot(x="count", y="room_type", data=room_type_listings)
    ax.set_xlabel(xlabel='Count', fontsize=15)
    ax.set_ylabel(ylabel='Room type', fontsize=15)
    ax.set_title(label='Number of listings by room type', fontsize=15)
    st.pyplot(room_type_listings_fig)

    neighbourhood_distribution = plt.figure()
    plt.style.use('ggplot')
    ax = sns.boxplot(x=df['neighbourhood'],
                     y=df['price'], data=df, palette='Set3')
    ax.set_xlabel(xlabel='Neighbourhood', fontsize=15)
    ax.set_ylabel(ylabel='Price', fontsize=15)
    ax.set_title(
        label='Distribution of prices across neighbourhood', fontsize=15)
    plt.xticks(rotation=90)
    st.pyplot(neighbourhood_distribution)
    st.markdown("""
    <h6>Inference</h6>
    <ul>
      <li>The average prices of Westminster is more and it is low for Enfield and Havering</li>
    </ul>
    """, unsafe_allow_html=True)

    room_type_distribution = plt.figure()
    plt.style.use('ggplot')
    ax = sns.boxplot(x=df['room_type'], y=df['price'], data=df, palette='Set3')
    ax.set_xlabel(xlabel='Room type', fontsize=15)
    ax.set_ylabel(ylabel='Price', fontsize=15)
    ax.set_title(label='Distribution of prices across room type', fontsize=15)
    plt.xticks(rotation=90)
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
    sns.heatmap(df[["name", "host_id", "host_name", "neighbourhood", "latitude", "longitude", "room_type", "price",
                "minimum_nights", "number_of_reviews", "last_review", "reviews_per_month", "calculated_host_listings_count", "availability_365"]].corr(), cmap="YlGnBu", annot=True)
    st.pyplot(heatmap_fig)
    st.markdown("From the correlation heatmap we can see that the facators effecting the price are **calculated_host_listings_count**,**minimum_nights**,**host**")

    ###################### PRICE AVERAGE BY ACOMMODATION #########################

    st.header("Average price by room type")

    st.markdown("To listings based on room type, we can show price average.")

    avg_price_room = df.groupby("room_type").price.mean().reset_index()\
        .round(2).sort_values("price", ascending=False)\
        .assign(avg_price=lambda x: x.pop("price").apply(lambda y: "%.2f" % y))

    avg_price_room = avg_price_room.rename(
        columns={'room_type': 'Room Type', 'avg_price': 'Average Price ($)', })

    st.table(avg_price_room)

    ############################ MOST RATED HOSTS #############################

    st.header("Most rated hosts")

    rankings_fig = plt.figure()
    ranked = df.groupby(['host_name'])['number_of_reviews'].count(
    ).sort_values(ascending=False).reset_index()
    ranked = ranked.head(5)
    ax = sns.barplot(x="number_of_reviews", y="host_name", data=ranked)
    ax.set_xlabel(xlabel='Number of reviews', fontsize=15)
    ax.set_ylabel(ylabel='Host', fontsize=15)
    st.pyplot(rankings_fig)

    st.write(f"""The host **{ranked.iloc[0].host_name}** is at the top with {ranked.iloc[0].number_of_reviews} reviews.
    **{ranked.iloc[1].host_name}** is second with {ranked.iloc[1].number_of_reviews} reviews. It should also be noted that reviews are not positive or negative reviews, but a count of feedbacks provided for the accommodation.""")
