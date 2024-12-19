import streamlit as st

overview = st.Page("overview.py", title="Overview", icon=":material/database:")
medias_mensais = st.Page(
    "medias_mensais.py", title="Medias mensais", icon=":material/calendar_month:"
)
comparacoes = st.Page("comparacoes.py", title="Comparar", icon=":material/compare:")

pg = st.navigation([overview, medias_mensais, comparacoes])
pg.run()
