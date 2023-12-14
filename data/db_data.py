import data_science_utils as dsu
import streamlit as st
from dotenv import load_dotenv

load_dotenv()  # TODO: move to dsu package

# Test the connection
conn = dsu.create_redshift_connection()


@st.cache_data
def load_business_data():
    """
    Get Segment data from cur_data_axle.business_data.
    WHERE clause filters out bad data and sets up cabinets
    """
    query = """
        -- get the greenlit fiberhoods
        WITH greenlit AS (
        SELECT
                    id as subdivision_id,
                    LEFT(name, POSITION('-' IN name) - 1) as cabinet,
                    name as fiberhood
                    , JSON_EXTRACT_PATH_TEXT(metadata, 'estimatedAvailabilityDate')::date as estimated_availability_date

                    , case 
                        when estimated_availability_date < CURRENT_DATE
                            Then 'greenlit'
                        else 'not_greenlit'
                    End as greenlit_true
                FROM cur_community.subdivisions 
                WHERE type = 'fiberhood'
                )

        -- join the greenlit information with the staging business data
        SELECT
            fiberhood, 
            CASE
                When greenlit_true is not null
                THEN greenlit_true
                ELSE 'not_greenlit'
            END as greenlit_true,
            adhoc_subdivision_name AS cabinet_name,
            company_name, 
            location_address,
            CASE  
                WHEN location_city LIKE '%Lucie%'
                    OR location_city LIKE '%Port St%'
                    OR location_city LIKE '%Siloam Springs%'
                    OR location_city LIKE '%Port Saint%'
                THEN 'Port St Lucie'
                WHEN company_name LIKE 'Mcelroy Tutoring%'
                    OR location_city LIKE 'Black Forest'
                    OR location_city LIKE 'Colorado-Springs'
                    OR location_city LIKE '%Colorado Spr%'
                THEN 'Colorado Springs'
            ELSE location_city
            END as location_city,
            location_state, loc_sales_vol_int,
            latitude as latitude,
            longitude as longitude,
            geometry, segment, naics,
            naics_description,
            left(naics,2) as naics_cat,
            location_employee_size_range,
            telcom_expenses
        FROM cur_data_axle.business_data_subdivisions AS bds
        LEFT JOIN greenlit AS g ON g.subdivision_id = bds.fiberhood_id
        WHERE company_name NOT in ('Ecannplus', 'Payne I P Law', 
                                    'Sisters Of St Francis', '360 Tour Designs')  
        AND mailing_address != '2348 Sijan Hall'
        """

    df = dsu.run_query(query)
    return df


@st.cache_data
def load_cabinets():
    """
    Load cabinet locations from business data subdivisions
    """
    query = """
        SELECT 
            latitude as latitude,
            longitude as longitude
            , ST_AsText(shape) as shape
            , adhoc_subdivision_name AS cabinet_name

        FROM cur_data_axle.business_data_subdivisions
        WHERE adhoc_subdivision_name is not null
    """

    return dsu.run_query(query)


def create_df(query):
    """
    Creates pandas dataframe from redshift query string
    """
    with conn.cursor() as cursor:
        cursor.execute(query)
        df = cursor.fetch_dataframe()
    return df