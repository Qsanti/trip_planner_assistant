import streamlit as st
import os

from src.structures.travelplan import TravelPlan

travel_plan = TravelPlan()


roles_names = {
    "assistant": "Travis",
    "user": "You",
}

st.set_page_config(
    page_title="Friendly Travel Advisor", page_icon="🌍", layout="centered"
)

st.markdown(
    """
        <style>
               .block-container {
                    padding-top: 1.5rem;
                    padding-bottom: 0rem;
                    padding-left: 5rem;
                    padding-right: 5rem;
                }
        </style>
        """,
    unsafe_allow_html=True,
)


# title_container = st.container(border=1)
col1, col2 = st.columns([1, 4])
# with title_container:
with col1:
    st.image(
        "https://techjobsforgood-prod.s3.amazonaws.com/company_profile_photos/e080999a-a87d-44ea-8b4c-4f7aafa9d25d-20220405-153523.jpeg",
        width=110,
    )
with col2:
    st.title("Trip Assistant")
    # st.markdown('<h1 style="color: blue;">Suzieq</h1>', unsafe_allow_html=True)


st.write(
    "Welcome to a friendly travel advisor! 🌍 Use this assistant to plan your trips based on the carbon footprint of yours movements. 🚗🚲🚆"
)

with st.sidebar:

    st.markdown(
        """
    <style>
        .css-znku1x.e16nr0p33 {
        margin-top: -75px;
        }
    </style>
    """,
        unsafe_allow_html=True,
    )

    st.subheader("Add your api keys")

    key_columns = st.columns(2)

    if "OPENAI_API_KEY" in st.secrets:
        st.success("API key already provided!", icon="✅")
        os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]
        openai_flag = True
    else:
        with key_columns[0]:
            os.environ["OPENAI_API_KEY"] = st.text_input(
                "Enter your OpenAI API key:", type="password"
            )
        if not (
            os.environ.get("OPENAI_API_KEY", "").startswith("sk-")
            and len(os.environ.get("OPENAI_API_KEY", "")) == 51
        ):
            openai_flag = False
        else:
            openai_flag = True

    if "GMAPS_API_KEY" in st.secrets:
        st.success("API key already provided!", icon="✅")
        os.environ["GMAPS_API_KEY"] = st.secrets["GMAPS_API_KEY"]
        gmaps_flag = True
    else:
        with key_columns[1]:
            os.environ["GMAPS_API_KEY"] = st.text_input(
                "Enter your Google Maps API key:", type="password"
            )
        if not (
            os.environ.get("GMAPS_API_KEY", "").startswith("AIza")
            and len(os.environ.get("GMAPS_API_KEY", "")) == 39
        ):
            gmaps_flag = False
        else:
            gmaps_flag = True

    if not openai_flag or not gmaps_flag:
        st.warning("Please enter your credentials!", icon="⚠️")
    else:
        st.success("API keys set!", icon="✅")

    # TODO: Add MAP
    # st.subheader("Map")
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
        label="Download travel plan as CSV 📂",
        data=travel_plan.get_df().to_csv(index=False),
        file_name="travel_plan.csv",
        mime="text/csv",
    )

    # Add clear button
    if st.button("Clear travel plan 🗑️"):
        travel_plan.clear()
        st.rerun()


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

    if not openai_flag:
        st.error("Please enter your OpenAI API key!")
        st.stop()
    if not gmaps_flag:
        st.error("Please enter your Google Maps API key!")
        st.stop()
    from src.ai import generate_response

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(f"**{roles_names['user']}**: {prompt}")
    with st.chat_message("assistant"):
        message_placeholder = st.markdown(f"{roles_names['assistant']} is typing...")
        response = generate_response(st.session_state.messages)
        message_placeholder.markdown(f"**{roles_names['assistant']}**: {response}")
        st.session_state.messages.append({"role": "assistant", "content": response})

    st.rerun()
