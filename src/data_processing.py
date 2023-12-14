# import geopandas as gpd
from collections import namedtuple
import src
import pandas as pd
import streamlit as st


## Functions for creating list of options for the widgets
# generic options
def create_options(df, exact_column_name: str) -> list:
    """Take a column from df and output just the unique values.
    Used populate list of options for widgets"""
    options = df[exact_column_name].unique()
    return options


# customized functions for formatted options
def options_NAICS(df) -> list:
    """Take a pd df and pull multiselect names from naics_description column.
    Custom formatting applied. Outputs list of options for widget.
    """
    naics_labels = src.format_naics()

    df["naics_cat_description"] = df["naics_cat"].replace(naics_labels)
    naics = sorted(df["naics_cat_description"].unique())
    return naics


def options_employee_size() -> list:
    """Take a pd df and pull slider names from location_employee_size_actual column.
    Custom formatting applied. Outputs list of options for widget.
    """
    employee_sizes = src.format_employee_sizes()
    return employee_sizes


def options_telcom() -> list:
    """Take a pd df and pull slider names from telcom_expenses column.
    Custom formatting applied. Outputs list of options for widget.
    """
    telcom_expenses = src.format_telcom()
    return telcom_expenses


def options_subdivision(df) -> list:
    """
    Take pd df and define cabinet locations.
    Areas outside cabinet boundaries are out of current phase.
    """
    # replace null values (locations outside current cab boundaries) with descriptive string
    df["cabinet_name"].fillna("Not in Phase", inplace=True)
    subdivisions = sorted(df["cabinet_name"].unique())
    return subdivisions


def options_fiberhood(df, greenlit_checkbox: bool):
    """
    Checks if greenlit selection box selected. If yes, return 'greenlit' to mask_nt.
    If no, return 'not_greenlit' to mask_nt and turn off all values
    """
    if greenlit_checkbox:
        # set session option
        fiberhood_selection = "greenlit"
    else:
        # set session option
        fiberhood_selection = "not_greenlit"
        # force all values in df 'greenlit_true' column off -- bool_array() will handle map breaking issues
        df["greenlit_true"] = "not_greenlit"

    return fiberhood_selection


## Functions for defining the dataframe masking ##

# define the named tuple that collects session selections here
Mask = namedtuple(
    "Mask",
    [
        "session_city",
        "session_segments",
        "session_subdivisions",
        "session_fiberhood",
        "session_naics",
        "session_employees",
        "session_telcom",
    ],
)


def bool_array(df, column_name, namedtuple_arg):
    """
    Create boolean arrays to mask options from the widgets.
    Each widget should have chosen session options.  They may be a single string, or a list.
    Outputs an array of True/False, to be used in the mask funct to create final displayed map
    """
    # the tuple args are usually lists, but select-one, like drop down widgest, use str
    if type(namedtuple_arg) == str:
        bool_mask = df[column_name] == namedtuple_arg
    else:
        bool_mask = df[column_name].isin(namedtuple_arg)

    # if an array is all false, df will return empty after masking, breaking the map
    if bool_mask.sum() == 0:
        # set to all true when there is an all false condition (filter unused)
        bool_mask = pd.Series(True, index=df.index)
        # st.write(bool_mask)
    return bool_mask


def df_mask(df, mask_nt: namedtuple) -> pd.DataFrame:
    """Create boolean masks for df information.
    Takes a namedtuple to keep args clean.
    """
    # build boolean mask arrays
    fiberhood_mask = bool_array(df, "greenlit_true", mask_nt.session_fiberhood)
    subdivision_mask = bool_array(df, "cabinet_name", mask_nt.session_subdivisions)
    city_mask = bool_array(df, "location_city", mask_nt.session_city)
    segment_mask = bool_array(df, "segment", mask_nt.session_segments)
    naics_mask = bool_array(df, "naics_cat_description", mask_nt.session_naics)
    employee_mask = bool_array(
        df, "location_employee_size_range", mask_nt.session_employees
    )
    telcom_mask = bool_array(df, "telcom_expenses", mask_nt.session_telcom)

    # boolean operation to mask selected session options
    mask = (
        (city_mask)
        & (segment_mask)
        & (subdivision_mask)
        & (fiberhood_mask)
        & (naics_mask)
        & (employee_mask)
        & (telcom_mask)
    )
    # check_mask(mask, df)

    # if an array is all false, df will return empty after masking, breaking the map
    if mask.sum() == 0:
        # set to all true when there is an all false condition (filter unused)
        mask = pd.Series(True, index=df.index)
        st.write("**:red[No companies found!]**   Please reset filters and try again")

    return df[mask]


def check_mask(mask, df) -> None:
    ##TODO : tried to use this function in df_mask() above and in src.cabinets.cabs_df_mask()
    ##but it breaks the map and causes a JSON syntax error when the session has city/subdivision mismatch

    # if an array is all false, df will return empty after masking, breaking the map
    if mask.sum() == 0:
        # set to all true when there is an all false condition (filter unused)
        mask = pd.Series(True, index=df.index)
        st.write("**:red[No companies found!]**   Please reset filters and try again")

    # #apply boolean masking to filter df to only the info we need based on session choices
    # df = df[mask]
    # return df
