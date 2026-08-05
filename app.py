import streamlit as st

st.set_page_config(
    page_title="SolidRisk",
    page_icon="🛡️",
    layout="centered"
)

# =========================
# ESTILO
# =========================

st.markdown("""
<style>

.main {
    background-color: #f5f7fa;
}

.titulo {
    font-size: 52px;
    font-weight: 700;
    color: #1F4E79;
    text-align: center;
    margin-bottom: 5px;
}

.subtitulo {
    font-size: 18px;
    color: #666666;
    text-align: center;
    margin-bottom: 30px;
}

.logo {
    text-align: center;
    font-size: 85px;
}

.footer {
    text-align: center;
    color: #888888;
    margin-top: 40px;
    font-size: 14px;
}

.stButton > button {
    width: 100%;
    background-color: #F37021 !important;
    color: white !important;
    border-radius: 8px;
    height: 45px;
    font-size: 18px;
    font-weight: bold;
}

</style>
""", unsafe_allow_html=True)

# =========================
# CABECERA
# =========================

st.markdown(
    """
    <div class="logo">
        🛡️
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    '<div class="titulo">SolidRisk</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitulo">Plataforma de Riesgo, Analítica Financiera y Solvencia</div>',
    unsafe_allow_html=True
)

# =========================
# LOGIN
# =========================

usuario = st.text_input(
    "👤 Usuario"
)

password = st.text_input(
    "🔒 Contraseña",
    type="password"
)

if st.button("Ingresar"):

    if usuario == "admin" and password == "1234":

        st.success("✅ Bienvenido a SolidRisk")

    else:

        st.error("❌ Credenciales incorrectas")

# =========================
# FOOTER
# =========================

st.markdown(
    """
    <div class="footer">
        By PwC - Analfe <br>
        © 2026 SolidRisk Platform
    </div>
    """,
    unsafe_allow_html=True
)
