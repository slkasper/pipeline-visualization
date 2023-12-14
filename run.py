from collections import namedtuple
import streamlit as st
import time

from data.db_data import load_business_data, load_cabinets
import data_science_utils as dsu
import src

start = time.time()

# Add title for  page
st.title("Business Data Explorer")

# load in SQL data
df = load_business_data()  # dataframe for segement and cities
df = src.add_color(df)

# Define options lists for widgets
cities_array = src.create_options(df, "location_city")
cities = list(cities_array)
cities.insert(
    0, cities.pop(cities.index("Colorado Springs"))
)  # make Colorado Springs initial city

segments = src.create_options(df, "segment")
subdivisions = src.options_subdivision(df)
naics = src.options_NAICS(df)
employee_sizes = src.options_employee_size()
telcoms = src.options_telcom()

# Call the widgets
with st.sidebar:
    # st.header('Choose a city')
    city_selection = src.selection_box_widget("**Cities**", cities)

    # st.header('Business Segments')
    segment_selection = src.multiselect_widget("**Business Segments**", segments)

    st.markdown(
        """##### Segment Key (in millions):
    Large Enterprise = Greater than $10
    Small-Medium Enterprise = $5 to $10
    Small Business = $1 to $5
    Microenterprise = Less than $1
    """
    )

    st.text("")  # add vertical space
    # Subdivision multiselect
    subdivision_selection = st.multiselect(
        "**Subdivisions** - add 'Not in phase' to see outside cabinet boundaries",
        subdivisions,
        default=subdivisions[:-1],
    )

    # Employee Size multi-select
    employee_size_selection = src.multiselect_widget(
        "**Employee Size**", employee_sizes
    )

    # Telcom mutltiselect
    telcom_selection = src.multiselect_widget("**Telcom Expenses**", telcoms)

    # NAICS mutltiselect
    naics_selection = src.multiselect_widget("**NAICS**", naics)

# Above the map, set the Greenlit checkbox
greenlit_checkbox = st.checkbox(
    "Display Greenlit Fiberhoods only", value=True
)  # get bool on or off
fiberhood_selection = src.options_fiberhood(df, greenlit_checkbox)

# Use Mask namedtuple to create the map with current session selections
mask_nt = src.Mask(
    city_selection,
    segment_selection,
    subdivision_selection,
    fiberhood_selection,
    naics_selection,
    employee_size_selection,
    telcom_selection,
)
df = src.df_mask(df, mask_nt)

scatterplot = src.create_scatter_layer(df)

# cabs_df = src.cabinets_load(cab_boundaries_on)
cabs_df = src.load_cabinets()

# filter based on user inputs
cabs_df = src.cabs_df_mask(cabs_df, mask_nt)

cab_boundary = src.display_cabinet_boundaries(cabs_df)
cab_labels = src.display_cabinet_labels(cabs_df)


layers = [scatterplot, cab_boundary, cab_labels]

r = src.create_view(df, layers)

st.pydeck_chart(r)

# dataframe for cabinet locations


# Output the current session dataframe for export to csv
display_cols = [
    "company_name",
    "location_address",
    "location_city",
    "location_state",
    "segment",
    "naics",
    "naics_description",
    "location_employee_size_range",
    "loc_sales_vol_int",
    "telcom_expenses",
    "cabinet_name",
    "greenlit_true",
]

st.write(df[display_cols])


@st.cache_data
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode("utf-8")


csv = convert_df(df[display_cols])
date = src.build_datetime_name()

st.download_button(
    label="Download data as CSV",
    data=csv,
    file_name=f"Business_data_explorer-{date}.csv",
    key="download-csv",
)

# check load time
st.write(f"TIME: {time.time() - start:.3f} sec")
