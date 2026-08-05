import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import os

# =====================================================
# CONFIGURACION GENERAL
# =====================================================

st.set_page_config(
    page_title="SolidRisk",
    page_icon="SR",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================================
# PALETA CORPORATIVA PREMIUM 2026
# =====================================================

PRIMARY = "#1E293B"       # Gris azulado oscuro
SECONDARY = "#475569"     # Gris corporativo
ACCENT = "#FD5108"        # Naranja principal
ACCENT_2 = "#FE8C39"      # Naranja medio
ACCENT_3 = "#FFAA72"      # Naranja suave

BG = "#F5F5F5"
CARD = "#FFFFFF"

TEXT = "#111111"
MUTED = "#6B7280"
BORDER = "#D8DCE2"

GREY_1 = "#A1A8B3"
GREY_2 = "#B5BCC4"
GREY_3 = "#CBD2D8"

GREEN = "#1B7F5C"
RED = "#B42318"
AMBER = "#B7791F"

css = f"""
<style>

.stApp {{
    background-color: {BG};
    color: {TEXT};
    font-family: "Segoe UI", Arial, sans-serif;
}}

section[data-testid="stSidebar"] {{
    background: linear-gradient(180deg, {PRIMARY} 0%, {SECONDARY} 100%);
}}

section[data-testid="stSidebar"] * {{
    color: white !important;
}}

.main-header {{
    background: linear-gradient(
        135deg,
        #1E293B 0%,
        #334155 60%,
        #FD5108 100% 
    );
    padding: 32px;
    border-radius: 20px;
    color: white;
    margin-bottom: 25px;
    box-shadow: 0px 15px 40px rgba(0,0,0,0.15);
}}
.main-title {{
    font-size: 38px;
    font-weight: 800;
    letter-spacing: 1.8px;
    margin: 0;
}}

.main-subtitle {{
    font-size: 15px;
    color: #DDE7F0;
    margin-top: 6px;
    margin-bottom: 0;
}}

.brand-line {{
    font-size: 13px;
    color: #F8C99B;
    margin-top: 10px;
    font-weight: 600;
}}

.login-box {{
    background-color: white;
    padding: 34px;
    border-radius: 20px;
    box-shadow: 0 12px 34px rgba(11,31,58,0.15);
    border: 1px solid {BORDER};
    max-width: 480px;
    margin: 45px auto 10px auto;
}}

.login-title {{
    font-size: 34px;
    font-weight: 800;
    color: {PRIMARY};
    text-align: center;
    letter-spacing: 1.6px;
    margin-bottom: 4px;
}}

.login-subtitle {{
    text-align: center;
    color: {MUTED};
    font-size: 14px;
    margin-bottom: 26px;
}}

.module-card {{
    background-color: white;
    border: 1px solid {BORDER};
    border-radius: 18px;
    padding: 24px;
    min-height: 155px;
    box-shadow: 0 6px 18px rgba(11,31,58,0.08);
    border-top: 5px solid {ACCENT};
    transition: all 0.2s ease-in-out;
}}

.module-card:hover {{
    transform: translateY(-2px);
    box-shadow: 0 10px 28px rgba(11,31,58,0.14);
}}

.module-title {{
    font-size: 22px;
    font-weight: 800;
    color: {PRIMARY};
    margin-bottom: 8px;
}}

.module-text {{
    font-size: 14px;
    color: {MUTED};
    line-height: 1.45;
}}

.section-card {{
    background-color: white;
    border: 1px solid {BORDER};
    border-radius: 18px;
    padding: 22px;
    box-shadow: 0 6px 18px rgba(11,31,58,0.06);
    margin-bottom: 18px;
}}

.kpi-card{{
    background:white;
    border-radius:18px;
    padding:22px;
    border:none;
    box-shadow:0px 8px 25px rgba(0,0,0,0.07);
    border-top:5px solid #FD5108;
    transition:all .25s ease;
}}

.kpi-card:hover {{
    transform: translateY(-4px);
    transition: all .25s ease;
}}

.kpi-value {{
    font-size: 29px;
    color: {PRIMARY};
    font-weight: 800;
    margin-top: 8px;
}}

.kpi-label {{
    font-size: 12px;
    color: {MUTED};
    text-transform: uppercase;
    font-weight: 700;
    letter-spacing: 0.6px;
}}

.kpi-note {{
    font-size: 12px;
    color: {MUTED};
    margin-top: 4px;
}}

.status-normal {{
    display: inline-block;
    padding: 5px 10px;
    background-color: rgba(27,127,92,0.12);
    color: {GREEN};
    border-radius: 999px;
    font-size: 12px;
    font-weight: 700;
    margin-top: 8px;
}}

.status-warning {{
    display: inline-block;
    padding: 5px 10px;
    background-color: rgba(183,121,31,0.12);
    color: {AMBER};
    border-radius: 999px;
    font-size: 12px;
    font-weight: 700;
    margin-top: 8px;
}}

.status-critical {{
    display: inline-block;
    padding: 5px 10px;
    background-color: rgba(180,35,24,0.12);
    color: {RED};
    border-radius: 999px;
    font-size: 12px;
    font-weight: 700;
    margin-top: 8px;
}}

.footer {{
    text-align:center;
    color:{MUTED};
    font-size:12px;
    margin-top:36px;
    padding-top:18px;
    border-top:1px solid {BORDER};
}}

div.stButton > button {{
    width: 100%;
    background: linear-gradient(135deg, {ACCENT_2} 0%, {ACCENT} 100%);
    color: white;
    border-radius: 12px;
    border: 1px solid {ACCENT};
    padding: 0.65rem 1rem;
    font-weight: 700;
    font-size: 15px;
    transition: background 0.3s ease;
}}

div.stButton > button:hover {{
    background: linear-gradient(135deg, {ACCENT} 0%, {ACCENT_2} 100%);
    color: white;
    border: 1px solid {ACCENT_2};
}}

.stTabs [data-baseweb="tab-list"] {{
    gap: 8px;
}}

.stTabs [data-baseweb="tab"] {{
    background-color: white;
    border: 1px solid {BORDER};
    border-radius: 12px 12px 0 0;
    padding: 12px 18px;
    color: {PRIMARY};
    font-weight: 700;
}}

.stTabs [aria-selected="true"] {{
    border-top: 4px solid {ACCENT};
    color: {PRIMARY};
}}

</style>
"""

st.markdown(css, unsafe_allow_html=True)

# =====================================================
# FUNCIONES DE UTILIDAD
# =====================================================

def format_cop_millions(value):
    try:
        value = float(value)
        return f"${value:,.0f}"
    except Exception:
        return "n/d"


def format_pct(value):
    try:
        if pd.isna(value) or np.isinf(value):
            return "n/d"
        return f"{float(value):,.2f}%"
    except Exception:
        return "n/d"


def status_badge(value, green_max=None, amber_max=None, inverse=False):
    """
    Si inverse=False: menor es mejor.
    Si inverse=True: mayor es mejor.
    """
    try:
        v = float(value)
    except Exception:
        return "<span class='status-warning'>Sin clasificación</span>"

    if inverse:
        if green_max is not None and v >= green_max:
            return "<span class='status-normal'>Adecuado</span>"
        if amber_max is not None and v >= amber_max:
            return "<span class='status-warning'>Observación</span>"
        return "<span class='status-critical'>Crítico</span>"

    if green_max is not None and v <= green_max:
        return "<span class='status-normal'>Adecuado</span>"
    if amber_max is not None and v <= amber_max:
        return "<span class='status-warning'>Observación</span>"
    return "<span class='status-critical'>Crítico</span>"


def kpi_card(label, value, note="", badge_html=""):
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">{value}</div>
            <div class="kpi-note">{note}</div>
            {badge_html}
        </div>
        """,
        unsafe_allow_html=True
    )


def page_header(title, subtitle):
    st.markdown(
        f"""
        <div class="main-header">
            <p class="main-title">{title}</p>
            <p class="main-subtitle">{subtitle}</p>
            <p class="brand-line">By PwC - Analfe</p>
        </div>
        """,
        unsafe_allow_html=True
    )


def safe_sum(df, codes):
    existing_codes = [c for c in codes if c in df.columns]
    if not existing_codes:
        return pd.Series(0, index=df.index)
    return df[existing_codes].sum(axis=1)


def limpiar_valor(x):
    if isinstance(x, str):
        return x.strip()
    return x


def plot_layout(fig, title=None, yaxis_title=None):
    fig.update_layout(
        template="plotly_white",
        height=430,
        margin=dict(l=20, r=20, t=70, b=40),
        title=dict(
            text=title,
            font=dict(size=19, color=PRIMARY, family="Segoe UI"),
            x=0.02,
            xanchor="left"
        ) if title else None,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(size=12, color=TEXT)
        ),
        hovermode="x unified",
        paper_bgcolor="white",
        plot_bgcolor="white",
        font=dict(color=TEXT, family="Segoe UI")
    )
    fig.update_xaxes(
        showgrid=False,
        linecolor=BORDER,
        tickfont=dict(size=11, color=MUTED)
    )
    fig.update_yaxes(
        gridcolor="#EEF2F6",
        linecolor=BORDER,
        tickfont=dict(size=11, color=MUTED),
        title=yaxis_title
    )
    return fig


def professional_line(df, x, y, title, name, color=PRIMARY, reference=None, reference_label=None):
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=df[x],
            y=df[y],
            mode="lines+markers",
            name=name,
            line=dict(color=color, width=3),
            marker=dict(size=7, color=color, line=dict(width=1, color="white")),
            fill="tozeroy",
            fillcolor="rgba(29,59,92,0.08)"
        )
    )

    if reference is not None:
        fig.add_hline(
            y=reference,
            line_dash="dash",
            line_color=ACCENT,
            annotation_text=reference_label if reference_label else f"Referencia {reference}",
            annotation_position="top left"
        )

    return plot_layout(fig, title=title, yaxis_title="%")


def professional_multi_line(df, x, series, title, yaxis_title="%"):
    fig = go.Figure()

    colors = [PRIMARY, ACCENT, "#6B7280", GREEN, RED, AMBER]

    for i, item in enumerate(series):
        fig.add_trace(
            go.Scatter(
                x=df[x],
                y=df[item["col"]],
                mode="lines+markers",
                name=item["name"],
                line=dict(color=colors[i % len(colors)], width=3),
                marker=dict(size=7, line=dict(width=1, color="white"))
            )
        )

    return plot_layout(fig, title=title, yaxis_title=yaxis_title)


def professional_stacked_bar(df, x, columns, title, yaxis_title="%"):
    fig = go.Figure()

    colors = [PRIMARY, ACCENT, "#6B7280", "#9CA3AF", "#CBD5E1", GREEN, AMBER]

    for i, col in enumerate(columns):
        fig.add_trace(
            go.Bar(
                x=df[x],
                y=df[col],
                name=col,
                marker_color=colors[i % len(colors)],
                hovertemplate="%{x}<br>" + col + ": %{y:.2f}%<extra></extra>"
            )
        )

    fig.update_layout(barmode="stack")
    return plot_layout(fig, title=title, yaxis_title=yaxis_title)


def professional_bar(df, x, y, title, yaxis_title="%"):
    fig = px.bar(
        df,
        x=x,
        y=y,
        color=y,
        color_continuous_scale=[
            [0.0, PRIMARY],
            [0.5, SECONDARY],
            [1.0, ACCENT]
        ],
        text_auto=".2f"
    )

    fig.update_traces(
        textposition="outside",
        marker_line_color="white",
        marker_line_width=0.8
    )

    fig.update_layout(showlegend=False)
    return plot_layout(fig, title=title, yaxis_title=yaxis_title)




# =====================================================
# PROCESAMIENTO DE EXCEL BL
# =====================================================

def procesar_balance_excel(archivo_excel):
    try:
        df_raw = pd.read_excel(
            archivo_excel,
            sheet_name="BL",
            header=None,
            engine="openpyxl"
        )
    except Exception as e:
        st.error(f"No fue posible leer la hoja BL del archivo. Detalle: {e}")
        return None

    df_raw = df_raw.apply(lambda col: col.map(limpiar_valor))

    data = []
    current_period = None

    meses = [
        "dic", "ene", "feb", "mar", "abr", "may", "jun",
        "jul", "ago", "sep", "oct", "nov",
        "diciembre", "enero", "febrero", "marzo", "abril",
        "mayo", "junio", "julio", "agosto", "septiembre",
        "octubre", "noviembre"
    ]

    for _, row in df_raw.iterrows():

        val_col0 = row.iloc[0]
        val_col1 = row.iloc[1] if len(row) > 1 else None

        if pd.notna(val_col0) and pd.isna(val_col1):
            val_str = str(val_col0).strip()
            parsed_date = pd.to_datetime(val_str, errors="coerce", dayfirst=True)

            if pd.notna(parsed_date):
                current_period = parsed_date.strftime("%Y-%m-%d")
                continue

            val_lower = val_str.lower()

            if (
                "/" in val_str
                or "-" in val_str
                or any(m in val_lower for m in meses)
                or "24" in val_lower
                or "25" in val_lower
                or "26" in val_lower
            ):
                current_period = val_str
                continue

        if current_period is not None and pd.notna(val_col0):

            codigo_str = str(val_col0).strip()

            codigos_excluidos = [
                "cedula", "codigo", "nombre", "nombre de las variables",
                "nombrt", "salant", "debito", "credit", "nuesal"
            ]

            if codigo_str.lower() not in codigos_excluidos and not codigo_str.isalpha():

                val_nuesal = row.iloc[7] if len(row) > 7 else None
                nuesal_val = pd.to_numeric(val_nuesal, errors="coerce")

                if not pd.isna(nuesal_val):
                    data.append(
                        {
                            "FECHA": current_period,
                            "CODIGO_CONTABLE": codigo_str,
                            "nuesal": nuesal_val
                        }
                    )

    df_base = pd.DataFrame(data)

    if df_base.empty:
        return None

    df_base["FECHA_DT"] = pd.to_datetime(
        df_base["FECHA"],
        errors="coerce",
        dayfirst=True
    )

    pivot_bl = df_base.pivot_table(
        index="FECHA",
        columns="CODIGO_CONTABLE",
        values="nuesal",
        aggfunc="sum"
    ).fillna(0)

    fechas = (
        df_base[["FECHA", "FECHA_DT"]]
        .drop_duplicates()
        .set_index("FECHA")
    )

    pivot_bl = pivot_bl.join(fechas, how="left")
    pivot_bl = pivot_bl.sort_values("FECHA_DT")
    pivot_bl = pivot_bl.drop(columns=["FECHA_DT"], errors="ignore")

    return pivot_bl


# =====================================================
# PROCESAMIENTO DE CSV CARTERA
# =====================================================

def leer_csv_subido(archivo):
    encodings = ["utf-8", "latin1", "cp1252"]

    for enc in encodings:
        try:
            archivo.seek(0)
            df = pd.read_csv(
                archivo,
                sep=None,
                engine="python",
                dtype=str,
                encoding=enc,
                on_bad_lines="skip"
            )
            return df
        except Exception:
            pass

    return None


def procesar_archivos_cartera(archivos_csv):
    if not archivos_csv:
        return None

    variables_interes = [
        "TipoIden", "NIT", "CodigoContable", "ModificacionesAlCredito",
        "NroCredito", "FechaDesembolsoInicial", "FechaVencimiento",
        "Morosidad", "TipoCuota", "AlturaCuota", "Amortizacion",
        "Modalidad", "TasaIntereNominal", "TasaInteresEfectiva",
        "ValorPrestamo", "ValorCuotaFija", "SaldoCapital",
        "SaldoIntereses", "OtrosSaldos", "Garantia", "FechaAvaluo",
        "Provision", "ProvisionInteres", "Contingencia",
        "ValosCuotasExtra", "MesesCuotaExtra", "fechaultimopago",
        "clasegarantia", "destinocredito", "CodOficina",
        "AmortiCapital", "ValorMora", "TipoVivienda", "VIS",
        "RangoTipo", "EntidadRedescuento", "MargenRedescuento",
        "Subsidio", "Desembolso", "Moneda", "FechaReestructuracion",
        "CategoriaReestr", "AportesSociales", "LineaCredEntidad",
        "NumModificaciones", "Estadocredito", "NITPatronal",
        "NombrePatronal"
    ]

    dataframes = []

    for archivo in archivos_csv:
        nombre_archivo = archivo.name
        fecha_str = os.path.splitext(nombre_archivo)[0]

        fecha_eval = pd.to_datetime(
            "01" + fecha_str,
            format="%d%m%Y",
            errors="coerce"
        )

        df = leer_csv_subido(archivo)

        if df is None:
            continue

        cols_presentes = [c for c in variables_interes if c in df.columns]

        if not cols_presentes:
            continue

        temp = df[cols_presentes].copy()
        temp["FECHA_CORTE"] = fecha_eval
        dataframes.append(temp)

    if not dataframes:
        return None

    cartera = pd.concat(dataframes, ignore_index=True)

    columnas_base = [
        "NroCredito", "NIT", "CodigoContable",
        "Morosidad", "NITPatronal", "NombrePatronal"
    ]

    for col in columnas_base:
        if col not in cartera.columns:
            cartera[col] = np.nan

    cartera = cartera[
        ~(
            cartera["NroCredito"].isna()
            & cartera["NIT"].isna()
            & cartera["CodigoContable"].isna()
            & cartera["Morosidad"].isna()
            & cartera["NITPatronal"].isna()
            & cartera["NombrePatronal"].isna()
        )
    ]

    columnas_numericas = [
        "SaldoCapital", "SaldoIntereses", "ValorMora",
        "Morosidad", "ValorPrestamo", "Provision", "AportesSociales"
    ]

    for col in columnas_numericas:
        if col not in cartera.columns:
            cartera[col] = 0

        cartera[col] = (
            cartera[col]
            .astype(str)
            .str.replace("$", "", regex=False)
            .str.replace(",", ".", regex=False)
            .str.replace(" ", "", regex=False)
        )

        cartera[col] = pd.to_numeric(cartera[col], errors="coerce").fillna(0)

    cartera["FECHA_CORTE"] = pd.to_datetime(cartera["FECHA_CORTE"], errors="coerce")

    cartera["NombrePatronal"] = (
        cartera["NombrePatronal"]
        .astype(str)
        .str.strip()
    )

    return cartera


# =====================================================
# SESSION STATE
# =====================================================

if "login" not in st.session_state:
    st.session_state.login = False

if "modulo" not in st.session_state:
    st.session_state.modulo = "Dashboard Ejecutivo"


# =====================================================
# LOGIN
# =====================================================

if not st.session_state.login:

    st.markdown(
        """
        <div class="login-box">
            <div class="login-title">SolidRisk</div>
            <div class="login-subtitle">
                Enterprise Risk Intelligence Platform<br>
                By PwC - Analfe
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    col_a, col_b, col_c = st.columns([1, 1.2, 1])

    with col_b:
        usuario = st.text_input("Usuario")
        password = st.text_input("Contraseña", type="password")

        if st.button("Ingresar"):
            if usuario == "admin" and password == "1234":
                st.session_state.login = True
                st.session_state.modulo = "Dashboard Ejecutivo"
                st.rerun()
            else:
                st.error("Credenciales incorrectas")

    st.stop()


# =====================================================
# SIDEBAR
# =====================================================

with st.sidebar:

    st.markdown(
        """
        <div style="padding: 8px 4px 20px 4px;">
            <div style="font-size:28px;font-weight:800;letter-spacing:1.4px;">
                SolidRisk
            </div>
            <div style="font-size:12px;color:#D8E1EA;">
                Enterprise Risk Intelligence Platform
            </div>
            <div style="font-size:12px;color:#F8C99B;margin-top:6px;">
                By PwC - Analfe
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("---")

    if st.button("SARC"):
        st.session_state.modulo = "SARC"

    if st.button("SARL"):
        st.session_state.modulo = "SARL"

    if st.button("SARM"):
        st.session_state.modulo = "SARM"

    if st.button("SARO"):
        st.session_state.modulo = "SARO"

    if st.button("Dashboard Ejecutivo"):
        st.session_state.modulo = "Dashboard Ejecutivo"
    
    if st.button("Reportes"):
        st.session_state.modulo = "Reportes"  
    
    st.markdown("---")
    
    logout_placeholder = st.empty()
    
    with logout_placeholder.container():
        if st.button("Cerrar sesión"):
            st.session_state.login = False
            st.session_state.modulo = "Dashboard Ejecutivo"
            st.rerun()

section[data-testid="stSidebar"] div.stButton:last-child > button {
    background: #6B7280; /* Gris */
    border: 1px solid #4B5563;
}

section[data-testid="stSidebar"] div.stButton:last-child > button:hover {
    background: #4B5563; /* Gris más oscuro */
    border: 1px solid #374151;
}

# =====================================================
# DASHBOARD EJECUTIVO
# =====================================================

if st.session_state.modulo == "Dashboard Ejecutivo":

    page_header(
        "SolidRisk",
        "Dashboard Ejecutivo de Indicadores Financieros, Cartera, Deterioro y Concentración"
    )

    st.markdown(
        """
        <div class="section-card">
            <b>Objetivo del módulo.</b> Este tablero permite cargar los insumos financieros y de cartera para generar una visión ejecutiva de la estructura de cartera, calidad crediticia, deterioro, cobertura, concentración y fondeo. 
            El diseño está orientado a comités de riesgo, alta gerencia y miembros de junta directiva.
        </div>
        """,
        unsafe_allow_html=True
    )

    col_upload_1, col_upload_2 = st.columns(2)

    with col_upload_1:
        archivo_excel = st.file_uploader(
            "Archivo Excel de indicadores financieros",
            type=["xlsx", "xlsm"]
        )

    with col_upload_2:
        archivos_csv = st.file_uploader(
            "Archivos CSV de cartera, opcional",
            type=["csv"],
            accept_multiple_files=True
        )

    col_btn_1, col_btn_2, col_btn_3 = st.columns([1, 1, 1])

    with col_btn_2:
        graficar = st.button("Generar visualización ejecutiva")

    if graficar:

        if archivo_excel is None:
            st.error("Debes cargar el archivo Excel de indicadores financieros.")
            st.stop()

        with st.spinner("Procesando información y generando tablero ejecutivo..."):

            pivot_bl = procesar_balance_excel(archivo_excel)

            if pivot_bl is None or pivot_bl.empty:
                st.error("No fue posible procesar la hoja BL del archivo cargado.")
                st.stop()

            cartera = procesar_archivos_cartera(archivos_csv)

            # =====================================================
            # CALCULOS DESDE BL
            # =====================================================

            periodos = pivot_bl.index.astype(str).tolist()

            cods_cartera_activos = [
                "1120", "12", "13", "141105", "141110", "144205", "144210"
            ]

            cartera_g1 = safe_sum(pivot_bl, cods_cartera_activos)

            columna_activos = [
                c for c in pivot_bl.columns
                if str(c).strip() in ["1", "1.0"]
            ]

            if columna_activos:
                activos_g1 = pivot_bl[columna_activos[0]]
            else:
                activos_g1 = safe_sum(pivot_bl, ["1"])

            ratio_cartera_activos = np.where(
                activos_g1 != 0,
                cartera_g1 / activos_g1 * 100,
                0
            )

            columna_depositos = [
                c for c in pivot_bl.columns
                if str(c).strip() in ["21", "21.0"]
            ]

            if columna_depositos:
                depositos_g1 = pivot_bl[columna_depositos[0]]
            else:
                depositos_g1 = safe_sum(pivot_bl, ["21"])

            cods_cartera_total = [
                "1120", "13", "141105", "141110", "144205", "144210"
            ] + [
                c for c in pivot_bl.columns if str(c).startswith("12")
            ]

            cartera_total_bl = safe_sum(pivot_bl, cods_cartera_total)

            crecimiento_mensual = cartera_total_bl.pct_change(1) * 100
            crecimiento_anual = cartera_total_bl.pct_change(12) * 100

            cods_14 = [c for c in pivot_bl.columns if str(c).startswith("14")]

            cartera_bruta = safe_sum(pivot_bl, cods_14) + safe_sum(
                pivot_bl,
                ["146805", "146810"]
            )

            cods_1411 = [c for c in pivot_bl.columns if str(c).startswith("1411")]

            cartera_libranza = safe_sum(pivot_bl, cods_1411)
            cartera_no_libranza = cartera_bruta - cartera_libranza

            lib_share = np.where(
                cartera_bruta != 0,
                cartera_libranza / cartera_bruta * 100,
                0
            )

            nolib_share = np.where(
                cartera_bruta != 0,
                cartera_no_libranza / cartera_bruta * 100,
                0
            )

            cat_a = safe_sum(pivot_bl, ["141105", "141205"])
            cat_b = safe_sum(pivot_bl, ["141110"])
            cat_c = safe_sum(pivot_bl, ["141115"])
            cat_d = safe_sum(pivot_bl, ["141120", "144220"])
            cat_e = safe_sum(pivot_bl, ["144225"])

            total_cat = cat_a + cat_b + cat_c + cat_d + cat_e

            a_pct = np.where(total_cat != 0, cat_a / total_cat * 100, 0)
            b_pct = np.where(total_cat != 0, cat_b / total_cat * 100, 0)
            c_pct = np.where(total_cat != 0, cat_c / total_cat * 100, 0)
            d_pct = np.where(total_cat != 0, cat_d / total_cat * 100, 0)
            e_pct = np.where(total_cat != 0, cat_e / total_cat * 100, 0)

            cartera_nueva = cartera_bruta.diff().clip(lower=0)

            new_share = np.where(
                cartera_bruta != 0,
                cartera_nueva / cartera_bruta * 100,
                0
            )

            provision_total = safe_sum(pivot_bl, ["146805", "146810"])

            cobertura_total = np.where(
                cartera_total_bl != 0,
                provision_total / cartera_total_bl * 100,
                0
            )

            cartera_vencida = safe_sum(
                pivot_bl,
                ["141120", "144220", "144225"]
            )

            cobertura_vencida = np.where(
                cartera_vencida != 0,
                provision_total / cartera_vencida,
                0
            )

            depositos_cartera = np.where(
                cartera_total_bl != 0,
                depositos_g1 / cartera_total_bl * 100,
                0
            )

            df_bl = pd.DataFrame(
                {
                    "Periodo": periodos,
                    "Cartera_Activos": ratio_cartera_activos,
                    "Crecimiento_Mensual": crecimiento_mensual.values,
                    "Crecimiento_Anual": crecimiento_anual.values,
                    "Libranza": lib_share,
                    "No_Libranza": nolib_share,
                    "A": a_pct,
                    "B": b_pct,
                    "C": c_pct,
                    "D": d_pct,
                    "E": e_pct,
                    "Cartera_Nueva": new_share,
                    "Cobertura_Total": cobertura_total,
                    "Cobertura_Vencida": cobertura_vencida,
                    "Cartera_Total": cartera_total_bl.values,
                    "Activos": activos_g1.values,
                    "Depositos": depositos_g1.values,
                    "Depositos_Cartera": depositos_cartera
                }
            )

        st.success("Tablero generado correctamente.")

        ultimo = df_bl.iloc[-1]

        st.markdown("### Resumen ejecutivo")

        k1, k2, k3, k4, k5 = st.columns(5)

        with k1:
            kpi_card(
                "Cartera / Activos",
                format_pct(ultimo["Cartera_Activos"]),
                "Participación de cartera dentro del activo",
                status_badge(ultimo["Cartera_Activos"], green_max=68, amber_max=75)
            )

        with k2:
            kpi_card(
                "Crecimiento anual cartera",
                format_pct(ultimo["Crecimiento_Anual"]),
                "Variación 12 meses",
                status_badge(abs(ultimo["Crecimiento_Anual"]) if pd.notna(ultimo["Crecimiento_Anual"]) else 0, green_max=20, amber_max=35)
            )

        with k3:
            kpi_card(
                "Cobertura total",
                format_pct(ultimo["Cobertura_Total"]),
                "Provisión sobre cartera total",
                status_badge(ultimo["Cobertura_Total"], green_max=4, amber_max=8, inverse=True)
            )

        with k4:
            kpi_card(
                "Cobertura vencida",
                f"{ultimo['Cobertura_Vencida']:.2f}x",
                "Provisión sobre cartera vencida",
                status_badge(ultimo["Cobertura_Vencida"], green_max=1.0, amber_max=0.7, inverse=True)
            )

        with k5:
            kpi_card(
                "Depósitos / Cartera",
                format_pct(ultimo["Depositos_Cartera"]),
                "Cobertura de cartera con fondeo",
                status_badge(ultimo["Depositos_Cartera"], green_max=100, amber_max=80, inverse=True)
            )

        tab1, tab2, tab3, tab4, tab5 = st.tabs(
            [
                "Estructura de cartera",
                "Calidad crediticia",
                "Deterioro y provisiones",
                "Concentración",
                "Liquidez y fondeo"
            ]
        )

        # =====================================================
        # TAB 1
        # =====================================================

        with tab1:

            st.markdown("#### Estructura de cartera")

            c1, c2 = st.columns(2)

            with c1:
                fig = professional_line(
                    df_bl,
                    "Periodo",
                    "Cartera_Activos",
                    "Cartera sobre activos",
                    "Cartera / activos",
                    color=PRIMARY,
                    reference=68,
                    reference_label="Referencia 68%"
                )
                st.plotly_chart(fig, use_container_width=True)

            with c2:
                fig = professional_multi_line(
                    df_bl,
                    "Periodo",
                    [
                        {"col": "Crecimiento_Mensual", "name": "Crecimiento mensual"},
                        {"col": "Crecimiento_Anual", "name": "Crecimiento anual"}
                    ],
                    "Crecimiento de cartera",
                    yaxis_title="%"
                )
                st.plotly_chart(fig, use_container_width=True)

            c3, c4 = st.columns(2)

            with c3:
                fig = professional_stacked_bar(
                    df_bl,
                    "Periodo",
                    ["Libranza", "No_Libranza"],
                    "Composición libranza y no libranza",
                    yaxis_title="%"
                )
                st.plotly_chart(fig, use_container_width=True)

            with c4:
                fig = professional_stacked_bar(
                    df_bl,
                    "Periodo",
                    ["A", "B", "C", "D", "E"],
                    "Composición de cartera por calificación",
                    yaxis_title="%"
                )
                st.plotly_chart(fig, use_container_width=True)

            fig = professional_line(
                df_bl,
                "Periodo",
                "Cartera_Nueva",
                "Cartera nueva sobre cartera total",
                "Cartera nueva",
                color=ACCENT
            )

            st.plotly_chart(fig, use_container_width=True)

        # =====================================================
        # TAB 2
        # =====================================================

        with tab2:

            st.markdown("#### Calidad crediticia")

            if cartera is None:
                st.warning("Para esta sección debes cargar archivos CSV de cartera.")
            else:
                cartera["Saldo_Vencido_90"] = cartera["SaldoCapital"].where(
                    cartera["Morosidad"] > 90,
                    0
                )

                resumen_icv = (
                    cartera
                    .groupby("FECHA_CORTE")
                    .agg(
                        Saldo_Vencido_Total=("Saldo_Vencido_90", "sum"),
                        Saldo_Capital_Total=("SaldoCapital", "sum")
                    )
                    .reset_index()
                )

                resumen_icv["ICV_90_Total"] = np.where(
                    resumen_icv["Saldo_Capital_Total"] != 0,
                    resumen_icv["Saldo_Vencido_Total"] / resumen_icv["Saldo_Capital_Total"] * 100,
                    0
                )

                fig_icv = go.Figure()

                fig_icv.add_trace(
                    go.Scatter(
                        x=resumen_icv["FECHA_CORTE"],
                        y=resumen_icv["ICV_90_Total"],
                        mode="lines+markers",
                        name="ICV 90+",
                        line=dict(color=PRIMARY, width=3),
                        marker=dict(size=7, line=dict(width=1, color="white")),
                        fill="tozeroy",
                        fillcolor="rgba(11,31,58,0.08)"
                    )
                )

                fig_icv.add_hline(
                    y=5,
                    line_dash="dash",
                    line_color=ACCENT,
                    annotation_text="Referencia 5%"
                )

                fig_icv = plot_layout(
                    fig_icv,
                    title="Evolución del ICV 90+",
                    yaxis_title="%"
                )

                st.plotly_chart(fig_icv, use_container_width=True)

                patronales_no_libranza = ["ASOCIADO EXTERNO", "EX-ASOCIADOS"]

                cartera["Tipo_Cartera"] = np.where(
                    cartera["NombrePatronal"].isin(patronales_no_libranza),
                    "No Libranza",
                    "Libranza"
                )

                resumen_modalidad = (
                    cartera
                    .groupby(["FECHA_CORTE", "Tipo_Cartera"])
                    .agg(
                        Saldo_Vencido_Total=("Saldo_Vencido_90", "sum"),
                        Saldo_Capital_Total=("SaldoCapital", "sum")
                    )
                    .reset_index()
                )

                resumen_modalidad["ICV_90"] = np.where(
                    resumen_modalidad["Saldo_Capital_Total"] != 0,
                    resumen_modalidad["Saldo_Vencido_Total"] / resumen_modalidad["Saldo_Capital_Total"] * 100,
                    0
                )

                fig_mod = px.line(
                    resumen_modalidad,
                    x="FECHA_CORTE",
                    y="ICV_90",
                    color="Tipo_Cartera",
                    markers=True,
                    color_discrete_map={
                        "Libranza": PRIMARY,
                        "No Libranza": ACCENT
                    }
                )

                fig_mod = plot_layout(
                    fig_mod,
                    title="ICV 90+ por modalidad de cartera",
                    yaxis_title="%"
                )

                st.plotly_chart(fig_mod, use_container_width=True)

                rangos = [-np.inf, 30, 60, 90, 120, 150, 180, np.inf]
                etiquetas = ["A", "B", "C", "D", "D", "D", "E"]

                cartera["Calificacion_Mora"] = pd.cut(
                    cartera["Morosidad"],
                    bins=rangos,
                    labels=etiquetas,
                    right=True,
                    include_lowest=True,
                    ordered=False
                )

                comp_cal = (
                    cartera
                    .groupby(["FECHA_CORTE", "Calificacion_Mora"])["SaldoCapital"]
                    .sum()
                    .reset_index()
                )

                total_mes = comp_cal.groupby("FECHA_CORTE")["SaldoCapital"].transform("sum")

                comp_cal["Participacion"] = np.where(
                    total_mes != 0,
                    comp_cal["SaldoCapital"] / total_mes * 100,
                    0
                )

                fig_rating = px.bar(
                    comp_cal,
                    x="FECHA_CORTE",
                    y="Participacion",
                    color="Calificacion_Mora",
                    color_discrete_sequence=[PRIMARY, SECONDARY, "#9CA3AF", ACCENT, RED]
                )

                fig_rating.update_layout(barmode="stack")

                fig_rating = plot_layout(
                    fig_rating,
                    title="Distribución de cartera por calificación de mora",
                    yaxis_title="%"
                )

                st.plotly_chart(fig_rating, use_container_width=True)

        # =====================================================
        # TAB 3
        # =====================================================

        with tab3:

            st.markdown("#### Deterioro y provisiones")

            c1, c2 = st.columns(2)

            with c1:
                fig = professional_line(
                    df_bl,
                    "Periodo",
                    "Cobertura_Total",
                    "Cobertura de cartera total",
                    "Cobertura total",
                    color=PRIMARY
                )
                st.plotly_chart(fig, use_container_width=True)

            with c2:
                fig = professional_line(
                    df_bl,
                    "Periodo",
                    "Cobertura_Vencida",
                    "Cobertura de cartera vencida",
                    "Cobertura vencida",
                    color=ACCENT
                )
                fig.update_yaxes(title="Veces")
                st.plotly_chart(fig, use_container_width=True)

            df_deterioro = df_bl.copy()
            df_deterioro["Provision_Cartera"] = df_deterioro["Cobertura_Total"]

            fig = professional_multi_line(
                df_deterioro,
                "Periodo",
                [
                    {"col": "Cartera_Activos", "name": "Cartera / activos"},
                    {"col": "Provision_Cartera", "name": "Provisión / cartera"}
                ],
                "Relación entre exposición y cobertura",
                yaxis_title="%"
            )

            st.plotly_chart(fig, use_container_width=True)

        # =====================================================
        # TAB 4
        # =====================================================

        with tab4:

            st.markdown("#### Concentración")

            if cartera is None:
                st.warning("Para esta sección debes cargar archivos CSV de cartera.")
            else:
                top_deudores = (
                    cartera
                    .groupby("NIT")["SaldoCapital"]
                    .sum()
                    .reset_index()
                    .sort_values("SaldoCapital", ascending=False)
                    .head(20)
                )

                total_cartera = cartera["SaldoCapital"].sum()

                top_deudores["Participacion"] = np.where(
                    total_cartera != 0,
                    top_deudores["SaldoCapital"] / total_cartera * 100,
                    0
                )

                fig_deudores = professional_bar(
                    top_deudores,
                    "NIT",
                    "Participacion",
                    "Top 20 deudores por concentración",
                    yaxis_title="%"
                )

                st.plotly_chart(fig_deudores, use_container_width=True)

                st.dataframe(
                    top_deudores,
                    use_container_width=True,
                    hide_index=True
                )

                if "AportesSociales" in cartera.columns:

                    top_ahorro = (
                        cartera
                        .groupby("NIT")["AportesSociales"]
                        .sum()
                        .reset_index()
                        .sort_values("AportesSociales", ascending=False)
                        .head(20)
                    )

                    total_ahorro = cartera["AportesSociales"].sum()

                    top_ahorro["Participacion"] = np.where(
                        total_ahorro != 0,
                        top_ahorro["AportesSociales"] / total_ahorro * 100,
                        0
                    )

                    fig_ahorro = professional_bar(
                        top_ahorro,
                        "NIT",
                        "Participacion",
                        "Top 20 asociados por ahorro y aportes",
                        yaxis_title="%"
                    )

                    st.plotly_chart(fig_ahorro, use_container_width=True)

                    st.dataframe(
                        top_ahorro,
                        use_container_width=True,
                        hide_index=True
                    )

        # =====================================================
        # TAB 5
        # =====================================================

        with tab5:

            st.markdown("#### Liquidez y fondeo")

            c1, c2 = st.columns(2)

            with c1:
                fig = professional_line(
                    df_bl,
                    "Periodo",
                    "Depositos_Cartera",
                    "Depósitos sobre cartera",
                    "Depósitos / cartera",
                    color=PRIMARY,
                    reference=100,
                    reference_label="Referencia 100%"
                )
                st.plotly_chart(fig, use_container_width=True)

            with c2:
                fig = professional_multi_line(
                    df_bl,
                    "Periodo",
                    [
                        {"col": "Crecimiento_Mensual", "name": "Crecimiento cartera mensual"},
                        {"col": "Crecimiento_Anual", "name": "Crecimiento cartera anual"}
                    ],
                    "Dinámica de crecimiento de cartera",
                    yaxis_title="%"
                )
                st.plotly_chart(fig, use_container_width=True)

            st.markdown(
                """
                <div class="section-card">
                    <b>Próximas extensiones del módulo.</b><br>
                    Activos líquidos sobre depósitos, brechas de liquidez, IRL, estabilidad del fondeo, concentración de captaciones y dimensión L del modelo CAMEL.
                </div>
                """,
                unsafe_allow_html=True
            )

        st.markdown("### Información procesada")

        with st.expander("Ver base procesada del Balance BL"):
            st.dataframe(df_bl, use_container_width=True, hide_index=True)

        if cartera is not None:
            with st.expander("Ver base procesada de cartera"):
                st.dataframe(cartera.head(1000), use_container_width=True, hide_index=True)


# =====================================================
# OTROS MODULOS
# =====================================================

elif st.session_state.modulo == "SARC":

    page_header(
        "SARC",
        "Sistema de Administración de Riesgo de Crédito"
    )

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            """
            <div class="module-card">
                <div class="module-title">Pérdida esperada</div>
                <div class="module-text">
                Cálculo de pérdida esperada bajo la estructura PD, LGD y EAD, con segmentación por línea, producto, modalidad y perfil de riesgo.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            """
            <div class="module-card">
                <div class="module-title">Calidad crediticia</div>
                <div class="module-text">
                Seguimiento del ICV, cosechas, transición de mora, concentración, deterioro y alertas tempranas de cartera.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


elif st.session_state.modulo == "SARL":

    page_header(
        "SARL",
        "Sistema de Administración de Riesgo de Liquidez"
    )

    st.markdown(
        """
        <div class="section-card">
            Módulo diseñado para análisis de brechas de liquidez, IRL, escenarios de estrés, concentración de fondeo y estabilidad de depósitos.
        </div>
        """,
        unsafe_allow_html=True
    )


elif st.session_state.modulo == "SARM":

    page_header(
        "SARM",
        "Sistema de Administración de Riesgo de Mercado"
    )

    st.markdown(
        """
        <div class="section-card">
            Módulo diseñado para medición de VaR, sensibilidad a tasas, duración, convexidad, backtesting y simulaciones de mercado.
        </div>
        """,
        unsafe_allow_html=True
    )


elif st.session_state.modulo == "SARO":

    page_header(
        "SARO",
        "Sistema de Administración de Riesgo Operacional"
    )

    st.markdown(
        """
        <div class="section-card">
            Módulo diseñado para eventos de riesgo operativo, KRIs, matriz de probabilidad e impacto, controles, planes de acción y pérdidas operacionales.
        </div>
        """,
        unsafe_allow_html=True
    )


# =====================================================
# FOOTER
# =====================================================

st.markdown(
    """
    <div class="footer">
        SolidRisk 1.0 | Enterprise Risk Intelligence Platform | By PwC - Analfe
    </div>
    """,
    unsafe_allow_html=True
)
