from data.db_data import load_cabinets
import src
import pandas as pd
import streamlit as st


def cabinets_load(cab_boundaries_on):
    """Check if cab_boundaries_on checkbox is seleceted. If so, run load_cabinets query"""
    if cab_boundaries_on:
        return load_cabinets()


def cabs_df_mask(df, mask_nt):
    """Drawing the boundary layer for subdivisions requires bool_array to mask.
    Note, mask check should at somepoint be a separate function.
    """
    mask = src.bool_array(df, "cabinet_name", mask_nt.session_subdivisions)
    # src.check_mask(mask, df)
    # TODO : get this check_mask() to work instead of lines below
    # if an array is all false, df will return empty after masking, breaking the map
    if mask.sum() == 0:
        # set to all true when there is an all false condition (filter unused)
        mask = pd.Series(True, index=df.index)
        st.write("**:red[No companies found!]**   Please reset filters and try again")

    return df[mask]


def display_cabinet_boundaries(cabs_df):
    """Create dataframe that calculates the polygon.
    Takes that dataframe and creates the boundary layer for pydeck layer.
    """
    polygon_df = src.create_polygon_df(cabs_df)
    cab_boundary = src.create_cab_boundary_layer(polygon_df)
    return cab_boundary


def display_cabinet_labels(cabs_df):
    """Creates text dataframe to capture cabinet labels.
    Takes that dataframe and creates the cabinet layer for the pydeck layer.
    """
    text_df = src.create_cab_text_df(cabs_df)
    cab_labels = src.create_cab_labels(text_df)
    return cab_labels
