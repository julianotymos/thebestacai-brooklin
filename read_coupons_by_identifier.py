import psycopg2
import pandas as pd
from psycopg2.extras import RealDictCursor
from typing import Optional

# Supondo que a função get_connection() já está definida
from get_conection import get_connection

def read_coupons_by_identifier(
    document_number: Optional[str] = None, 
    phone_number: Optional[str] = None
) -> pd.DataFrame:
    """
    Pesquisa por cupons de um cliente usando o CPF ou telefone e retorna um DataFrame.
    
    Args:
        document_number (str, opcional): O CPF do cliente.
        phone_number (str, opcional): O telefone do cliente.
        
    Retorna:
        Um DataFrame contendo os cupons encontrados.
        Retorna um DataFrame vazio se nenhum cupom for encontrado.
    """
    if not document_number and not phone_number:
        return pd.DataFrame()
        
    query = """
    SELECT 
        PHONE_NUMBER,
        DOCUMENT_NUMBER,
        COUPON_CODE,
        DESCRIPTION,
        POINTS,
        IS_USED,
        CREATED_AT,
        USED_AT
    FROM COUPONS
    WHERE DOCUMENT_NUMBER = %s OR PHONE_NUMBER = %s;
    """
    
    try:
        with get_connection() as conn:
            # Usa o RealDictCursor para retornar resultados como dicionários
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                # Executa a consulta
                cursor.execute(query, (document_number, phone_number))
                # Busca todos os resultados
                data = cursor.fetchall()
            
            # Converte a lista de dicionários para um DataFrame
            df = pd.DataFrame(data)
            print(f"Consulta executada. {len(df)} cupons encontrados.")
            return df
                
    except (Exception, psycopg2.Error) as error:
        print(f"Ocorreu um erro ao consultar os cupons: {error}")
        return pd.DataFrame()

# --- Exemplo de uso da função ---

#Pesquisar por CPF:
#cupons_df_ifood = read_coupons_by_identifier(document_number='36141494803')
#print(cupons_df_ifood)
##Pesquisar por telefone:
#cupons_df_99food = read_coupons_by_identifier(phone_number='36141494803')
#print(cupons_df_99food)