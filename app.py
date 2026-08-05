import streamlit as st

# =====================================================
# CONFIGURACIÓN
# =====================================================

st.set_page_config(
    page_title="SolidRisk",
    page_icon="🛡️",
    layout="wide"
)

# =====================================================
# ESTILOS
# =====================================================

st.markdown("""
<style>

.stApp {
    background-color: #f4f6f9;
}

.titulo {
    text-align:center;
    font-size:60px;
    font-weight:bold;
    color:#0B3C5D;
    margin-bottom:0;
}

.subtitulo {
    text-align:center;
    font-size:20px;
    color:#F37021;
    margin-bottom:20px;
}

.footer {
    text-align:center;
    color:gray;
    margin-top:50px;
    font-size:14px;
}

.stButton > button {
    width:100%;
    border-radius:12px;
    height:70px;
    font-size:22px;
    font-weight:bold;
    background-color:#0B3C5D;
    color:white;
}

.stButton > button:hover {
    background-color:#F37021;
    color:white;
}

.banner {
    background:white;
    padding:20px;
    border-radius:15px;
    box-shadow:0px 2px 10px rgba(0,0,0,0.10);
    margin-bottom:20px;
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# LOGIN SESSION
# =====================================================

if "login" not in st.session_state:
    st.session_state.login = False

if "modulo" not in st.session_state:
    st.session_state.modulo = None


# =====================================================
# LOGIN
# =====================================================

if not st.session_state.login:

    st.markdown(
        """
        <div class='titulo'>
        🛡️ SolidRisk
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class='subtitulo'>
        Plataforma Integral de Gestión de Riesgos
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")

    usuario = st.text_input(
        "👤 Usuario"
    )

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
                "❌ Credenciales incorrectas"
            )

    st.markdown(
        """
        <div class='footer'>
        By PwC - Analfe
        </div>
        """,
        unsafe_allow_html=True
    )


# =====================================================
# PÁGINA PRINCIPAL
# =====================================================

else:

    # ========================
    # SIDEBAR
    # ========================

    with st.sidebar:

        st.image(
            "https://img.icons8.com/color/96/shield.png",
            width=80
        )

        st.markdown("## SolidRisk")

        st.markdown("---")

        if st.button("🚪 Cerrar Sesión"):

            st.session_state.login = False
            st.session_state.modulo = None
            st.rerun()

    # ========================
    # CABECERA
    # ========================

    st.markdown(
        """
        <div class='titulo'>
        🛡️ SolidRisk
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class='subtitulo'>
        By PwC - Analfe
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("---")

    st.markdown(
        """
        ### Sistemas de Administración de Riesgos
        """
    )

    # ========================
    # BOTONES PRINCIPALES
    # ========================

    col1, col2 = st.columns(2)

    with col1:

        if st.button("🏦 SARC"):

            st.session_state.modulo = "SARC"

    with col2:

        if st.button("💧 SARL"):

            st.session_state.modulo = "SARL"

    col3, col4 = st.columns(2)

    with col3:

        if st.button("📈 SARM"):

            st.session_state.modulo = "SARM"

    with col4:

        if st.button("⚙️ SARO"):

            st.session_state.modulo = "SARO"

    st.write("")

    if st.button("📊 Dashboard Ejecutivo"):

        st.session_state.modulo = "Dashboard"

    st.markdown("---")

    # ========================
    # CONTENIDO
    # ========================

    if st.session_state.modulo == "SARC":

        st.success("🏦 Módulo SARC")

        st.info("""
        Sistema de Administración de Riesgo de Crédito

        Próximamente:

        • Pérdida Esperada

        • NIIF 9

        • Score

        • PD

        • LGD

        • EAD

        • Concentración
        """)

    elif st.session_state.modulo == "SARL":

        st.success("💧 Módulo SARL")

        st.info("""
        Sistema de Administración de Riesgo de Liquidez

        Próximamente:

        • Gap de Liquidez

        • IRL

        • Stress Testing
        """)

    elif st.session_state.modulo == "SARM":

        st.success("📈 Módulo SARM")

        st.info("""
        Sistema de Administración de Riesgo de Mercado

        Próximamente:

        • VaR

        • Backtesting

        • Monte Carlo
        """)

    elif st.session_state.modulo == "SARO":

        st.success("⚙️ Módulo SARO")

        st.info("""
        Sistema de Administración de Riesgo Operacional

        Próximamente:

        • Eventos de Riesgo

        • Matrices

        • Indicadores KRI
        """)

    elif st.session_state.modulo == "Dashboard":

        st.success("📊 Dashboard Ejecutivo")

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "Liquidez",
            "1.85"
        )

        col2.metric(
            "ROA",
            "4.8%"
        )

        col3.metric(
            "ROE",
            "12.5%"
        )

        col4.metric(
            "Solvencia",
            "145%"
        )

        st.info("""
        Este espacio será utilizado para indicadores
        financieros, CAMEL, VEA, NIIF 9, Riesgo de Crédito,
        Riesgo Actuarial y Solvencia.
        """)

    st.markdown("---")

    st.markdown(
        """
        <div class='footer'>
        © 2026 SolidRisk | By PwC - Analfe
        </div>
        """,
        unsafe_allow_html=True
    )
