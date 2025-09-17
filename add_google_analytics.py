import streamlit as st

def add_google_analytics():
    ga_script = """
    <!-- Google tag (gtag.js) -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-Q98R3VDZ5N"></script>
    <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());

    gtag('config', 'G-Q98R3VDZ5N');
    </script>
    """
    st.markdown(ga_script, unsafe_allow_html=True)

#add_google_analytics()
#
#st.title("Minha Aplicação Streamlit")
#st.write("Conteúdo da aplicação.")



def send_ga_event(event_name: str):
    st.markdown(f"""
    <script>
    if (typeof gtag === 'function') {{
        gtag('event', '{event_name}');
    }}
    </script>
    """, unsafe_allow_html=True)