import streamlit as st
import streamlit.components.v1 as components
import uuid
import datetime

GA_ID = "G-Q98R3VDZ5N"
# Cria um ID de sessão único (para diferenciar usuários anônimos)
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
    
def add_google_analytics():
    """Carrega o script do Google Analytics."""
    ga_code = f"""
    <!-- Google tag (gtag.js) -->
    <script async src="https://www.googletagmanager.com/gtag/js?id={GA_ID}"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){{dataLayer.push(arguments);}}
      gtag('js', new Date());
      gtag('config', '{GA_ID}', {{
        'session_id': '{st.session_state.session_id}'
      }});
    </script>
    """
    st.markdown(ga_code, unsafe_allow_html=True)
#add_google_analytics()
#
#st.title("Minha Aplicação Streamlit")
#st.write("Conteúdo da aplicação.")

def track_event(event_name: str, category: str, label: str = ""):
    """Função genérica para enviar eventos customizados."""
    timestamp = datetime.datetime.utcnow().isoformat()
    js = f"""
    <script>
      gtag('event', '{event_name}', {{
        'event_category': '{category}',
        'event_label': '{label}',
        'session_id': '{st.session_state.session_id}',
        'timestamp': '{timestamp}'
      }});
    </script>
    """
    st.markdown(js, unsafe_allow_html=True)


def track_page_view(page_name: str):
    """Marca visualização de página."""
    track_event("page_view", "Navegacao", page_name)


def track_tab(tab_name: str):
    """Marca acesso a aba."""
    track_event("acesso_aba", "Navegacao", tab_name)


def track_button(button_name: str):
    """Marca clique em botão."""
    track_event("click", "Botao", button_name)