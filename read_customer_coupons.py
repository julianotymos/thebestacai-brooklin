import streamlit as st
import pandas as pd
from get_bigquery_client import get_bigquery_client
import re
from read_coupons_by_identifier import read_coupons_by_identifier
#@st.cache_data(ttl=600, show_spinner=False)
def read_ifood_coupons_data(document_number: str):
    """
    Busca dados de compras e cupons de clientes iFood e os separa em dois DataFrames.
    Retorna:
    - customer_df: DataFrame com dados do cliente e total de pontos.
    - coupons_df: DataFrame com detalhes de cada cupom.
    """
    client = get_bigquery_client()

    query = f"""
    SELECT 
        CI.FIRST_NAME,
        CI.LAST_NAME, 
        CI.DOCUMENT_NUMBER,
        OT.NUM_COMPRAS
    FROM CUSTOMER CI
    INNER JOIN 
        (
            SELECT OT.CUSTOMER_ID, COUNT(1) AS NUM_COMPRAS FROM ORDERS_TABLE OT
            WHERE 1=1
            AND DATE(OT.CREATED_AT) >= '2025-08-12' 
            AND OT.SALES_CHANNEL = 'iFood'
            GROUP BY OT.CUSTOMER_ID 
        ) OT ON OT.CUSTOMER_ID = CI.ID
    

    WHERE 1=1  
    AND CI.DOCUMENT_NUMBER = '{document_number}'
    """
    
    try:
        query_job = client.query(query)
        df = query_job.to_dataframe()
        
        if df.empty:
            return pd.DataFrame(), pd.DataFrame()

        customer_df = df[[
            'FIRST_NAME', 
            'LAST_NAME', 
            'DOCUMENT_NUMBER', 
            'NUM_COMPRAS'
        ]].drop_duplicates()
        coupons_df = read_coupons_by_identifier(document_number = document_number)
        #print(coupons_df)
        #total_points = df['COUPON_POINTS'].sum()
        #customer_df['TOTAL_POINTS'] = total_points
#
        #coupons_df = df.dropna(subset=['COUPON_CODE'])[[
        #    'COUPON_CODE',
        #    'COUPON_DESC',
        #    'COUPON_POINTS',
        #    'COUPON_IS_USED'
        #]]

        return customer_df, coupons_df

    except Exception as e:
        st.error(f"Erro ao buscar dados de cupons iFood: {e}")
        return pd.DataFrame(), pd.DataFrame()

def read_99food_coupons_data(phone_number: str):
    """
    Busca dados de compras e cupons de clientes 99Food e os separa em dois DataFrames.
    Retorna:
    - customer_df: DataFrame com dados do cliente e total de pontos.
    - coupons_df: DataFrame com detalhes de cada cupom.
    """
    client = get_bigquery_client()

    query = f"""
    SELECT 
        C9.FIRST_NAME,
        C9.LAST_NAME, 
        C9.PHONE_NUMBER,
        OT.NUM_COMPRAS
        
    FROM CUSTOMER_99_FOOD C9
    INNER JOIN 
        (
            SELECT OT.C_UID, COUNT(1) AS NUM_COMPRAS FROM ORDERS_TABLE OT
            WHERE 1=1
            AND DATE(OT.CREATED_AT) >= '2025-08-12' 
            AND OT.SALES_CHANNEL = '99food'
            GROUP BY OT.C_UID 
        ) OT ON OT.C_UID = C9.C_UID
    

    WHERE 1=1   
    AND C9.PHONE_NUMBER = '{phone_number}'
    """

    try:
        query_job = client.query(query)
        df = query_job.to_dataframe()

        if df.empty:
            return pd.DataFrame(), pd.DataFrame()

        customer_df = df[[
            'FIRST_NAME',
            'LAST_NAME',
            'PHONE_NUMBER',
            'NUM_COMPRAS'
        ]].drop_duplicates()
        coupons_df = read_coupons_by_identifier(phone_number= phone_number)

        #total_points = df['COUPON_POINTS'].sum()
        #customer_df['POINTS_USED'] = total_points
#
        #coupons_df = df.dropna(subset=['COUPON_CODE'])[[
        #    'COUPON_CODE',
        #    'COUPON_DESC',
        #    'COUPON_POINTS',
        #    'COUPON_IS_USED'
        #]]

        return customer_df, coupons_df

    except Exception as e:
        st.error(f"Erro ao buscar dados de cupons 99Food: {e}")
        return pd.DataFrame(), pd.DataFrame()


def validate_number_input():
    # Acessa o valor do campo de texto pelo seu 'key'
    current_value = st.session_state.identifier_input

    # Usa uma expressão regular para verificar se o valor contém apenas dígitos
    if not re.fullmatch(r'\d*', current_value):
        # Se contiver algo que não seja um número, limpa o campo
        st.session_state.identifier_input = re.sub(r'[^0-9]', '', current_value)
        st.warning("Por favor, digite apenas números.")
        
#        
#df1 , df2 = read_ifood_coupons_data(document_number='36141494803')
#
#print(df1)
#
#print(df2)


#df1 , df2 = read_99food_coupons_data(phone_number='36141494803')
#print(df1)
#
#print(df2)