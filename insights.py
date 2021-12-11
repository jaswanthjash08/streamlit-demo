import matplotlib.pyplot as plt
import streamlit as st
import seaborn as sns
sns.set_style("whitegrid")


def write(df):
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

    ############################ MOST EXPENSIVE ACCOMIDATIONS #############################

    st.header("Most expensive accomidations")

    expensive_accom_fig = plt.figure()
    expensive_ranked = df.groupby(['name'])['price'].count(
    ).sort_values(ascending=False).reset_index()
    expensive_ranked = expensive_ranked.head(5)
    ax = sns.barplot(x="price", y="name", data=expensive_ranked)
    ax.set_xlabel(xlabel='Price in $', fontsize=15)
    ax.set_ylabel(ylabel='Name', fontsize=15)
    st.pyplot(expensive_accom_fig)
