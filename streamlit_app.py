import streamlit as st
import streamlit.components.v1 as components
import random
import string
# -----------------------------
# Configurações
# -----------------------------
STORE_NAME = "The Best Açaí Brooklin"
LOGO_PATH = "logo.png"  # arquivo na raiz do projeto

st.set_page_config(page_title=STORE_NAME,  layout="centered")

# -----------------------------
# Logo e Nome lado a lado
# -----------------------------
col1, col2 = st.columns([1, 6])
with col1:
    st.image(LOGO_PATH, width=80)  # ajusta o tamanho do logo
with col2:
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
    st.header("🎯 Como funciona a promoção")
    st.markdown("""
    1. Faça pedidos pelo iFood ou 99Food. Os pontos são contabilizados separadamente para cada plataforma.  
    2. Cada pedido dá **1 ponto**.  
    3. **Acumule 10 pontos** e ganhe **1 copo de 300ml** para montar do seu jeito.  
    4. **Acumule 15 pontos** e troque por **1 copo de 500ml** do seu jeito.  
    5. Promoção válida apenas para consumo **na loja**.  
    """)
#    st.image(
#        "DSC01260.png",
#        caption="Monte seu açaí perfeito 🍓"
#    )

    st.subheader("📍 Localização da loja")

    components.iframe(
        "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3655.80918643787!2d-46.68532869999999!3d-23.611175299999996!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x94ce51a8021ba92f%3A0x2f55a749211a1259!2zVGhlIEJlc3QgQcOnYcOt!5e0!3m2!1spt-BR!2sbr!4v1757531755277!5m2!1spt-BR!2sbr",
        width=700,   # largura do mapa
        height=450   # altura do mapa
    )
# -----------------------------
# Aba 2: Consultar Pedidos
# -----------------------------



import streamlit as st
import random
import string

# Inicializa o estado da sessão se ele não existir
if "show_results" not in st.session_state:
    st.session_state.show_results = False
if "total" not in st.session_state:
    st.session_state.total = 0
if "resgatados_300" not in st.session_state:
    st.session_state.resgatados_300 = 0
if "resgatados_500" not in st.session_state:
    st.session_state.resgatados_500 = 0
if "resgate_code" not in st.session_state:
    st.session_state.resgate_code = None
    
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
    # st.rerun() foi removido

def on_resgatar_300_click():
    """Função para resgatar cupom de 300ml."""
    st.session_state.resgate_code = gerar_codigo()
    st.session_state.resgatados_300 += 1
    # st.rerun() foi removido

with tabs[1]:
    st.header("🔍 Consultar meus pontos")
    identifier = st.text_input("Digite seu **telefone (99Food)** ou **CPF (iFood)**:", key="identifier_input")
    st.button("Consultar", on_click=on_consultar_click)
    
    if st.session_state.show_results:
        st.success(f"Você já fez **{st.session_state.total} pedidos** conosco! 🎉")

        cupom_500_disponivel = (st.session_state.total // 15) - st.session_state.resgatados_500
        cupom_300_disponivel = ((st.session_state.total % 15) // 10) - st.session_state.resgatados_300

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
                    st.write(f"• Cupom 500ml #{i+1} - Resgate na loja")
                with col2:
                    st.button(f"Resgatar 500ml #{i+1}", key=f"resgatar_500ml_{i}", on_click=on_resgatar_500_click)

        # Cupons 300ml
        if cupom_300_disponivel > 0:
            st.markdown("## 🎉 Cupons para 300ml disponíveis!")
            for i in range(cupom_300_disponivel):
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(f"• Cupom 300ml #{i+1} - Resgate na loja")
                with col2:
                    st.button(f"Resgatar 300ml #{i+1}", key=f"resgatar_300ml_{i}", on_click=on_resgatar_300_click)
        
        # Próximos cupons
        proximo_300 = 10 - ((st.session_state.total - st.session_state.resgatados_300 * 10) % 10)
        proximo_500 = 15 - ((st.session_state.total - st.session_state.resgatados_500 * 15) % 15)
        st.info(f"Faltam **{proximo_300} pedidos** para o próximo cupom de 300ml.")
        st.info(f"Faltam **{proximo_500} pedidos** para o próximo cupom de 500ml.")
    else:
        st.info("Digite seu identificador e clique em 'Consultar' para ver seus pontos.")