import psycopg2
from datetime import datetime
from typing import Optional

# Supondo que a função get_connection() já está definida
# para retornar uma conexão com o PostgreSQL.
from get_conection import get_connection

def insert_coupon(
    coupon_code: str,
    description: str,
    points: int,
    phone_number: Optional[str] = None,
    document_number: Optional[str] = None,
    is_used: bool = False,
    used_at: Optional[datetime] = None
) -> bool:
    """
    Insere um novo cupom na tabela 'COUPONS' no PostgreSQL.

    Args:
        coupon_code (str): O código único do cupom.
        description (str): Descrição do cupom.
        points (int): Pontos associados ao cupom.
        phone_number (str, opcional): Número de telefone do cliente.
        document_number (str, opcional): CPF do cliente.
        is_used (bool, opcional): Se o cupom já foi usado. Padrão é False.
        used_at (datetime, opcional): Data e hora em que o cupom foi usado.
    """
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                query = """
                INSERT INTO COUPONS (
                  PHONE_NUMBER,
                  DOCUMENT_NUMBER,
                  COUPON_CODE,
                  DESCRIPTION,
                  POINTS,
                  IS_USED,
                  CREATED_AT,
                  USED_AT
                ) VALUES (%s, %s, %s, %s, %s, %s, NOW(), %s);
                """
                # psycopg2 converte valores None do Python para NULL no SQL
                values = (
                    phone_number,
                    document_number,
                    coupon_code,
                    description,
                    points,
                    is_used,
                    used_at
                )
                
                cursor.execute(query, values)
                conn.commit()  # Confirma a transação
                print("Novo cupom inserido com sucesso no PostgreSQL.")
                return True
    except (Exception, psycopg2.Error) as error:
        print(f"Ocorreu um erro ao inserir o cupom no PostgreSQL: {error}")
        return False

# --- Exemplo de uso da função ---

#is_success = insert_coupon(
#    document_number='36141494803',
#    coupon_code='WXMPB8',
#    description='Copo de 300ml',
#    points=10,
#    is_used=False
#)