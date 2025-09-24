import streamlit as st
import streamlit.components.v1 as components
import random
import string
import pandas as pd
from read_customer_coupons import read_99food_coupons_data , read_ifood_coupons_data , validate_number_input
from validate_docbr import CPF
import uuid

from insert_coupon import insert_coupon
from add_google_analytics import add_google_analytics , track_tab , track_button
cpf_validator = CPF()
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
add_google_analytics()

# -----------------------------
# Configurações
# -----------------------------
STORE_NAME = "The Best Açaí Brooklin"
LOGO_PATH = "logo.png"  # arquivo na raiz do projeto
image_url = "logo_nav.bd660df458335873b1b2.webp"
#st.image(image_url, use_container_width=True)

st.set_page_config(page_title=STORE_NAME,  layout="centered")

# -----------------------------
# Logo e Nome lado a lado
# -----------------------------
#col1, col2 = st.columns([1, 6])
#with col1:
#    st.image(LOGO_PATH, width=80)  # ajusta o tamanho do logo
#with col2:
st.title(f"{STORE_NAME}")
st.subheader("Faça pedidos no delivery e resgate seu prêmio na loja!")

# -----------------------------
# Abas
# -----------------------------
tabs = st.tabs(["Como Funciona", "Consultar Pontos"])

# -----------------------------
# Aba 1: Como Funciona
# -----------------------------
with tabs[0]:
    st.header("🎯 Como funciona :")
    st.markdown("""
    1. Faça seus pedidos pelo iFood ou pelo 99Food. (Os pontos de cada aplicativo são acumulados separadamente).  
    2. A cada pedido realizado, você ganha **1 ponto**.  
    3. **Junte 10 pontos** e troque por **1 copo de 300ml** montado do seu jeito.  
    4. **Junte 15 pontos** e troque por **1 copo de 500ml** montado do seu jeito.
    5. Para acompanhar sua pontuação e gerar o cupom, acesse a aba "Consultar Pontos"  
    6. Mostre o código do cupom no caixa da loja para resgatar.
    7. Promoção válida somente para resgates presenciais na loja. Pedidos acumulam pontos a partir de 12/08/2025.  
    """)
#    st.image(
#        "DSC01260.png",
#        caption="Monte seu açaí perfeito 🍓"
#    )
    st.markdown("Clique no link para falar conosco no WhatsApp:")

    phone_number = "5511970370720" # Exemplo: 55 (Brasil) 11 (DDD) 987654321 (número)
    pre_filled_message = "Olá, gostaria de saber mais sobre a promoção de comprar no delivery e e resgate seu prêmio na loja!"

    link_url = f"https://wa.me/{phone_number}?text={pre_filled_message}"

    st.markdown(f"**[Fale Conosco no WhatsApp](<{link_url}>)**")
    st.subheader("📍 Venha retirar seu prêmio aqui:")

    components.iframe(
        "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3655.80918643787!2d-46.68532869999999!3d-23.611175299999996!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x94ce51a8021ba92f%3A0x2f55a749211a1259!2zVGhlIEJlc3QgQcOnYcOt!5e0!3m2!1spt-BR!2sbr!4v1757531755277!5m2!1spt-BR!2sbr",
        width=700,   # largura do mapa
        height=450   # altura do mapa
    )
    track_tab("Página Como Funciona")
# -----------------------------
# Aba 2: Consultar Pedidos
# -----------------------------





# Estado da sessão para controlar a exibição dos resultados
if 'show_results' not in st.session_state:
    st.session_state.show_results = False

if 'total' not in st.session_state:
    st.session_state.total = 0

if 'pontos_resgatados' not in st.session_state:
    st.session_state.pontos_resgatados = 0

if 'resgate_code' not in st.session_state:
    st.session_state.resgate_code = None

if 'identifier_input' not in st.session_state:
    st.session_state.identifier_input = ""

if 'resgatados_300' not in st.session_state:
    st.session_state.resgatados_300 = 0

if 'resgatados_500' not in st.session_state:
    st.session_state.resgatados_500 = 0

if 'df_coupons' not in st.session_state:
    st.session_state.df_coupons = pd.DataFrame()
    
def gerar_codigo(tamanho=6):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=tamanho))

def on_consultar_click():
    """Função para ser executada ao clicar em 'Consultar'."""
    if st.session_state.identifier_input:
        # Simula a consulta e salva os dados no estado
        st.session_state.show_results = True
        st.session_state.total = 50
        st.session_state.resgatados_300 = 1
        st.session_state.resgatados_500 = 1
    else:
        st.session_state.show_results = False
        st.error("Digite um telefone ou CPF para consultar.")

def on_resgatar_500_click():
    """Função para resgatar cupom de 500ml."""
    st.session_state.resgate_code = gerar_codigo()
    st.session_state.resgatados_500 += 1
    if st.session_state.channel_select =='99Food' :
        phone_number = st.session_state.identifier_input
        document_number = None
    else :
        phone_number = None
        document_number = st.session_state.identifier_input
    insert_coupon(coupon_code= st.session_state.resgate_code ,description='Copo de 500ml' , points=15 , phone_number = phone_number ,  document_number = document_number)
    # st.rerun() foi removido
    st.session_state.total = st.session_state.total - 15
    st.session_state.show_balloons = True   # <<< aqui

def on_resgatar_300_click():
    """Função para resgatar cupom de 300ml."""
    st.session_state.resgate_code = gerar_codigo()
    st.session_state.resgatados_300 += 1
    if st.session_state.channel_select =='99Food' :
        phone_number = st.session_state.identifier_input
        document_number = None
    else :
        phone_number = None
        document_number = st.session_state.identifier_input
    insert_coupon(coupon_code= st.session_state.resgate_code , description='Copo de 300ml' , points=10 , phone_number = phone_number  , document_number = document_number)
    st.session_state.total = st.session_state.total - 10
    st.session_state.show_balloons = True   # <<< aqui

    # st.rerun() foi removido

with tabs[1]:
    track_tab("Página Consultar Pontos")

    st.header("🔍 Consultar meus pontos")
    # Botão de rádio para selecionar o canal de consulta
    selected_channel = st.radio(
        "Selecione o canal de venda:",
        ('99Food', 'iFood'),
        key="channel_select",
        horizontal=True
    )

    # Lógica para mudar o rótulo do input
    if selected_channel == '99Food':
        input_label = "Digite seu **telefone**:"
    else:
        input_label = "Digite seu **CPF**:"

    identifier = st.text_input(input_label, key="identifier_input")
    
    if st.button("Consultar"):
        # A lógica da sua função on_consultar_click agora vai aqui
        track_button("Consultar")

        if not identifier:
            st.session_state.show_results = False
            st.error("Digite um identificador para consultar.")
        else:
            df = pd.DataFrame()
            if selected_channel == '99Food':
                # Remove qualquer coisa que não seja dígito (ex: parênteses, espaços, traços)
                phone_number = "".join(filter(str.isdigit, identifier))
                
                if len(phone_number) != 11:
                    st.session_state.show_results = False
                    st.error("Por favor, digite um telefone válido com 11 dígitos (DDD + número).")
                    
                else:
                    df, df_coupons = read_99food_coupons_data(phone_number=phone_number)
            elif selected_channel == 'iFood':
                document_number = "".join(filter(str.isdigit, identifier))
                
                if len(document_number) != 11:
                    st.error("O CPF deve conter exatamente 11 dígitos.")
                    st.session_state.show_results = False
                
                # 2. Se o comprimento estiver correto, valida o CPF
                elif not cpf_validator.validate(document_number):
                    st.error("O CPF digitado é inválido. Por favor, verifique os números.")
                    st.session_state.show_results = False
                else: 
                    df, df_coupons = read_ifood_coupons_data(document_number=document_number)

            if not df.empty:
                st.session_state.show_results = True
                num_compras = df.iloc[0]['NUM_COMPRAS']
                cupons_resgatados = df_coupons['points'].sum() if not df_coupons.empty else 0
                st.session_state.total = num_compras - cupons_resgatados
                
                # Armazena o DataFrame de cupons no estado da sessão
                st.session_state.df_coupons = df_coupons
                st.session_state.pontos_resgatados = cupons_resgatados
                #print ('ds' , st.session_state.df_coupons )
            else:
                st.session_state.show_results = False
                if selected_channel == '99Food':
                    identificador = "Telefone"
                else :
                    identificador = "CPF"
                st.error(f"Nenhum cliente encontrado para o App **{selected_channel}** com este **{identificador}**.")

    if st.session_state.show_results:
        st.success(f"Você tem **{st.session_state.total} pontos** conosco! 🎉")

        
        
        cupom_500_disponivel = (st.session_state.total // 15) - (st.session_state.pontos_resgatados // 500)
        cupom_300_disponivel = ((st.session_state.total % 15) // 10) - (st.session_state.pontos_resgatados // 300)

        if st.session_state.resgate_code:
            st.success(f"✅ Resgate Confirmado! Código: **{st.session_state.resgate_code}**")
            # Limpa o código para que não apareça novamente
            del st.session_state.resgate_code

        # Cupons 500ml
        if cupom_500_disponivel > 0:
            st.markdown("## 🏆 Cupons para 500ml disponíveis!")
            for i in range(cupom_500_disponivel):
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(f"• Copo de 500ml do seu jeito !#{i+1} - Resgate na loja")
                with col2:
                    st.button(f"Resgatar 500ml #{i+1}", key=f"resgatar_500ml_{i}", on_click=on_resgatar_500_click)

        # Cupons 300ml
        if cupom_300_disponivel > 0:
            st.markdown("## 🎉 Cupons para 300ml disponíveis!")
            for i in range(cupom_300_disponivel):
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(f"• Copo de 300ml do seu jeito !#{i+1} - Resgate na loja")
                with col2:
                    st.button(f"Resgatar 300ml #{i+1}", key=f"resgatar_300ml_{i}", on_click=on_resgatar_300_click)
        
        # Seção para exibir os cupons resgatados
    # Seção para exibir todos os cupons

        
        # Próximos cupons
        proximo_300 = 10 - ((st.session_state.total - (st.session_state.pontos_resgatados // 300) * 10) % 10)
        proximo_500 = 15 - ((st.session_state.total - (st.session_state.pontos_resgatados // 500) * 15) % 15)
        st.info(f"Faltam **{proximo_300} pedidos** para o próximo cupom de 300ml.")
        st.info(f"Faltam **{proximo_500} pedidos** para o próximo cupom de 500ml.")
    # Seção para exibir todos os cupons
        if not st.session_state.df_coupons.empty:
            st.markdown("---")
            st.subheader("Seus Cupons")

            for index, row in st.session_state.df_coupons.iterrows():
                if row['is_used']:
                    # Mostra o cupom como resgatado (caixa verde)
                    st.success(f"✅ Cupom Utilizado: {row['coupon_code']} - {row['description']}")
                else:
                    # Mostra o cupom como disponível (caixa azul)
                    st.info(f"⏳ Cupom Disponível: {row['coupon_code']} - {row['description']}")
        
    else:
        st.info("Digite seu identificador e clique em 'Consultar' para ver seus pontos.")
        
if st.session_state.get("show_balloons", False):
    st.balloons()
    st.session_state.show_balloons = False