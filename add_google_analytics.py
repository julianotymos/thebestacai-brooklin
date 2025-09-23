import streamlit as st

def add_google_analytics(measurement_id="G-Q98R3VDZ5N"):
    st.markdown(
        f"""
        <script async src="https://www.googletagmanager.com/gtag/js?id={measurement_id}"></script>
        <script>
            window.dataLayer = window.dataLayer || [];
            function gtag(){{dataLayer.push(arguments);}}
            gtag('js', new Date());
            gtag('config', '{measurement_id}');
        </script>
        """,
        unsafe_allow_html=True
    )
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