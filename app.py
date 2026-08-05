import streamlit as st

# ==================================
# CONFIGURACION
# ==================================

st.set_page_config(
    page_title="SolidRisk",
    page_icon="🛡️",
    layout="wide"
)

# ==================================
# ESTILO
# ==================================

st.markdown("""
<style>

.main {
    background-color:#f5f7fa;
}

.titulo {
    font-size:55px;
    font-weight:700;
    color:#0C3B60;
    text-align:center;
}

.subtitulo{
    text-align:center;
    color:#666;
    margin-bottom:30px;
}

.tarjeta{
    background:white;
    padding:30px;
    border-radius:15px;
    text-align:center;
    font-size:28px;
    font-weight:bold;
    border-left:8px solid #F37021;
    box-shadow:0px 3px 10px rgba(0,0,0,0.10);
}

.footer{
    text-align:center;
    color:gray;
    margin-top:30px;
}

</style>
""", unsafe_allow_html=True)

# ==================================
# SESSION
# ==================================

if "login" not in st.session_state:
    st.session_state.login = False

# ==================================
# LOGIN
# ==================================

if not st.session_state.login:

    st.markdown(
        '<div class="titulo">🛡️ SolidRisk</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitulo">Plataforma Integral de Riesgos y Analítica Financiera</div>',
        unsafe_allow_html=True
    )

    usuario = st.text_input("👤 Usuario")

    password = st.text_input(
        "🔒 Contraseña",
        type="password"
    )

    if st.button("Ingresar"):

        if usuario == "admin" and password == "1234":

            st.session_state.login = True
            st.rerun()

        else:

            st.error(
                "Credenciales incorrectas"
            )

    st.markdown(
        """
        <div class="footer">
        By PwC - Analfe
        </div>
        """,
        unsafe_allow_html=True
    )

# ==================================
# DASHBOARD PRINCIPAL
# ==================================

else:

    st.markdown(
        '<div class="titulo">🛡️ SolidRisk</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitulo">By PwC - Analfe</div>',
        unsafe_allow_html=True
    )

    st.markdown("## Sistemas de Administración de Riesgos")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("🏦 SARC", use_container_width=True):
            st.success("Módulo SARC")

    with col2:
        if st.button("💧 SARL", use_container_width=True):
            st.success("Módulo SARL")


    col3, col4 = st.columns(2)

    with col3:
        if st.button("📈 SARM", use_container_width=True):
            st.success("Módulo SARM")

    with col4:
        if st.button("⚙️ SARO", use_container_width=True):
            st.success("Módulo SARO")

    st.markdown("---")

    if st.button(
        "📊 Dashboard Ejecutivo",
        use_container_width=True
    ):
        st.success(
            "Dashboard de Indicadores Financieros"
        )

    st.markdown("---")

    st.info(
        """
        Próximos módulos:

        • CAMEL

        • Pérdida Esperada NIIF 9

        • Riesgo Crédito

        • Riesgo Liquidez

        • Riesgo Mercado

        • IBNR

        • RSA

        • ARNF

        • Solvencia
        """
    )
