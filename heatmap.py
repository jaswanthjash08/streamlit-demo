import pydeck as pdk
import pandas as pd
import streamlit as st


def write(df):
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
