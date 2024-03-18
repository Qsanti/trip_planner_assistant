import streamlit as st
import os
from time import sleep


import folium
import osmnx
import leafmap.foliumap as leafmap
import pandas as pd


from src.structures.travelplan import TravelPlan

travel_plan = TravelPlan()


roles_names = {
    "assistant": "Travis",
    "user": "You",
}

st.set_page_config(
    page_title="Friendly Travel Advisor", page_icon="🌍", layout="centered"
)

st.title("Friendly Travel Advisor")

st.write(
    "Welcome to the Friendly Travel Advisor! Ask me anything about travel and I'll do my best to help you out."
)


with st.sidebar:
    # Assuming you have some way of tracking if `travel_plan` changes

    # # make sidebar wider
    # st.markdown(
    #     "<style>div.Widget.row-widget.stRadio > div{flex-direction:column;}</style>",
    #     unsafe_allow_html=True,
    # )

    # add a image  in the sidebar
    st.image(
        "https://assets-global.website-files.com/62192ceb9199b3dd08431a6b/62192ceb9199b3803f431b3a_Light.svg",
        width=200,
    )
    # st.subheader("Add your api keys")
    # if "OPENAI_API_KEY" in st.secrets:
    #     st.success("API key already provided!", icon="✅")
    #     os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]
    # else:
    #     os.environ["OPENAI_API_KEY"] = st.text_input(
    #         "Enter your OpenAI API token:", type="password"
    #     )
    #     if not (
    #         os.environ.get("OPENAI_API_KEY", "").startswith("sk-")
    #         and len(os.environ.get("OPENAI_API_KEY", "")) == 51
    #     ):
    #         st.warning("Please enter your credentials!", icon="⚠️")
    #     else:
    #         st.success("API key set!", icon="👍")

    # BASEMAPS = ["Satellite", "Roadmap", "Terrain", "Hybrid", "OpenStreetMap"]
    # basemap = st.selectbox("Choose basemap", BASEMAPS)
    # if basemap in BASEMAPS[:-1]:
    #     basemap = basemap.upper()
    #     lat, lon = (40.7128, -74.0060)
    #     # get_location_from_address(address=ADDRESS_DEFAULT)

    #     m = leafmap.Map(center=(lat, lon), zoom=16)

    #     m.add_basemap(basemap)

    #     m.add_marker(
    #         location=(lat, lon),
    #         popup=f"lat, lon: {lat}, {lon}",
    #         icon=folium.Icon(color="green", icon="eye", prefix="fa"),
    #     )
    #     st.write(f"Lat, Lon: {lat}, {lon}")

    #     m.to_streamlit()

    total_carbon = (
        travel_plan.get_df()["Carbon"].sum() if not travel_plan.get_df().empty else 0
    )

    st.metric(label="Total Carbon Footprint (g CO2e)", value=f"{total_carbon:,.2f}")

    # SHow travel plan
    st.subheader("Travel Plan")

    travel_plan_df = travel_plan.get_df()
    if not travel_plan_df.empty:
        st.table(travel_plan_df)
    else:
        st.write("No routes added yet")

    # # add a button to download the data
    st.download_button(
        label="Download travel plan as CSV",
        data=travel_plan.get_df().to_csv(index=False),
        file_name="travel_plan.csv",
        mime="text/csv",
    )

    # Add clear button
    if st.button("Clear travel plan 🗑️"):
        travel_plan.clear()
        st.experimental_rerun()


# Set up the session state to store messages
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Hello! I'm Travis, your friendly travel advisor.",
        },
    ]

# Display the chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(f"**{roles_names[message['role']]}**: {message['content']}")


# Get the user's message
if prompt := st.chat_input("Write a message..."):
    from src.ai import generate_response

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(f"**{roles_names['user']}**: {prompt}")
    with st.chat_message("assistant"):
        message_placeholder = st.markdown(f"{roles_names['assistant']} is typing...")
        response = generate_response(st.session_state.messages)
        message_placeholder.markdown(f"**{roles_names['assistant']}**: {response}")
        st.session_state.messages.append({"role": "assistant", "content": response})

        # show_travel_plan()
        # refresh sidebar
    st.experimental_rerun()
