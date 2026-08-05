import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os

# =====================================================
# CONFIGURACIÓN GENERAL
# =====================================================

st.set_page_config(
    page_title="SolidRisk",
    page_icon="🛡️",
    layout="wide"
)

# =====================================================
# ESTILOS CORPORATIVOS
# =====================================================

st.markdown("""
<style>

.stApp {
    background-color: #f4f6f9;
}

.titulo {
    text-align:center;
    font-size:58px;
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

.card {
    background-color:white;
    padding:20px;
    border-radius:16px;
    box-shadow:0px 4px 14px rgba(0,0,0,0.08);
    border-left:6px solid #F37021;
    margin-bottom:16px;
}

.stButton > button {
    width:100%;
    border-radius:12px;
    height:55px;
    font-size:18px;
    font-weight:bold;
    background-color:#0B3C5D;
    color:white;
}

.stButton > button:hover {
    background-color:#F37021;
    color:white;
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# FUNCIONES AUXILIARES
# =====================================================

def safe_sum(df, codes):
    existing_codes = [c for c in codes if c in df.columns]
    if not existing_codes:
        return pd.Series(0, index=df.index)
    return df[existing_codes].sum(axis=1)


def limpiar_valor(x):
    if isinstance(x, str):
        return x.strip()
    return x


def procesar_balance_excel(archivo_excel):
    """
    Procesa el archivo Excel tipo INDICADORES FEMP 2025.xlsm.
    Lee la hoja BL y arma la tabla pivot_bl.
    """

    df_raw = pd.read_excel(
        archivo_excel,
        sheet_name="BL",
        header=None,
        engine="openpyxl"
    )

    df_raw = df_raw.apply(
        lambda col: col.map(limpiar_valor)
    )

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
            parsed_date = pd.to_datetime(
                val_str,
                errors="coerce",
                dayfirst=True
            )

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

                    data.append({
                        "FECHA": current_period,
                        "CÓDIGO CONTABLE": codigo_str,
                        "nuesal": nuesal_val
                    })

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
        columns="CÓDIGO CONTABLE",
        values="nuesal",
        aggfunc="sum"
    ).fillna(0)

    fecha_orden = (
        df_base[["FECHA", "FECHA_DT"]]
        .drop_duplicates()
        .set_index("FECHA")
    )

    pivot_bl = pivot_bl.join(fecha_orden, how="left")
    pivot_bl = pivot_bl.sort_values("FECHA_DT")
    pivot_bl = pivot_bl.drop(columns=["FECHA_DT"], errors="ignore")

    return pivot_bl


def leer_csv_subido(archivo):
    """
    Lee CSV de cartera con múltiples separadores y encodings.
    """

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
    """
    Procesa múltiples CSV de cartera.
    Cada archivo debería tener un nombre tipo 032026.csv.
    """

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

        df_procesado = df[cols_presentes].copy()
        df_procesado["FECHA_CORTE"] = fecha_eval

        dataframes.append(df_procesado)

    if not dataframes:
        return None

    cartera_total = pd.concat(dataframes, ignore_index=True)

    columnas_necesarias = [
        "NroCredito", "NIT", "CodigoContable",
        "Morosidad", "NITPatronal", "NombrePatronal"
    ]

    for col in columnas_necesarias:
        if col not in cartera_total.columns:
            cartera_total[col] = np.nan

    cartera_total = cartera_total[
        ~(
            cartera_total["NroCredito"].isna()
            & cartera_total["NIT"].isna()
            & cartera_total["CodigoContable"].isna()
            & cartera_total["Morosidad"].isna()
            & cartera_total["NITPatronal"].isna()
            & cartera_total["NombrePatronal"].isna()
        )
    ]

    columnas_numericas = [
        "SaldoCapital", "SaldoIntereses", "ValorMora",
        "Morosidad", "ValorPrestamo", "Provision", "AportesSociales"
    ]

    for col in columnas_numericas:
        if col not in cartera_total.columns:
            cartera_total[col] = 0

        cartera_total[col] = (
            cartera_total[col]
            .astype(str)
            .str.replace("$", "", regex=False)
            .str.replace(",", ".", regex=False)
            .str.replace(" ", "", regex=False)
        )

        cartera_total[col] = pd.to_numeric(
            cartera_total[col],
            errors="coerce"
        ).fillna(0)

    cartera_total["FECHA_CORTE"] = pd.to_datetime(
        cartera_total["FECHA_CORTE"],
        errors="coerce"
    )

    cartera_total["NombrePatronal"] = (
        cartera_total["NombrePatronal"]
        .astype(str)
        .str.strip()
    )

    return cartera_total


def grafico_linea(df, x, y, titulo, color="#0B3C5D"):
    fig = px.line(
        df,
        x=x,
        y=y,
        markers=True,
        title=titulo
    )
    fig.update_traces(
        line=dict(color=color, width=3),
        marker=dict(size=8)
    )
    fig.update_layout(
        template="plotly_white",
        title_font=dict(size=20, color="#0B3C5D"),
        hovermode="x unified",
        height=420
    )
    return fig


def grafico_barras_apiladas(df, x, y_cols, titulo):
    fig = go.Figure()

    colores = ["#0B3C5D", "#F37021", "#6C757D", "#00A6A6", "#A23E48"]

    for i, col in enumerate(y_cols):
        fig.add_trace(go.Bar(
            x=df[x],
            y=df[col],
            name=col,
            marker_color=colores[i % len(colores)]
        ))

    fig.update_layout(
        barmode="stack",
        template="plotly_white",
        title=titulo,
        title_font=dict(size=20, color="#0B3C5D"),
        height=420,
        hovermode="x unified"
    )

    return fig


# =====================================================
# VARIABLES DE SESIÓN
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
        "<div class='titulo'>🛡️ SolidRisk</div>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<div class='subtitulo'>Plataforma Integral de Gestión de Riesgos</div>",
        unsafe_allow_html=True
    )

    usuario = st.text_input("👤 Usuario")
    password = st.text_input("🔒 Contraseña", type="password")

    if st.button("Ingresar"):

        if usuario == "admin" and password == "1234":
            st.session_state.login = True
            st.rerun()
        else:
            st.error("❌ Credenciales incorrectas")

    st.markdown(
        "<div class='footer'>By PwC - Analfe</div>",
        unsafe_allow_html=True
    )


# =====================================================
# PLATAFORMA
# =====================================================

else:

    with st.sidebar:

        st.markdown("## 🛡️ SolidRisk")
        st.markdown("By PwC - Analfe")
        st.markdown("---")

        if st.button("📊 Dashboard Ejecutivo"):
            st.session_state.modulo = "Dashboard"

        if st.button("🏦 SARC"):
            st.session_state.modulo = "SARC"

        if st.button("💧 SARL"):
            st.session_state.modulo = "SARL"

        if st.button("📈 SARM"):
            st.session_state.modulo = "SARM"

        if st.button("⚙️ SARO"):
            st.session_state.modulo = "SARO"

        st.markdown("---")

        if st.button("🚪 Cerrar Sesión"):
            st.session_state.login = False
            st.session_state.modulo = None
            st.rerun()

    st.markdown(
        "<div class='titulo'>🛡️ SolidRisk</div>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<div class='subtitulo'>By PwC - Analfe</div>",
        unsafe_allow_html=True
    )

    st.markdown("---")

    # =====================================================
    # DASHBOARD EJECUTIVO
    # =====================================================

    if st.session_state.modulo == "Dashboard":

        st.markdown("## 📊 Dashboard Ejecutivo")

        st.markdown("""
        <div class='card'>
        En este módulo puedes cargar el archivo de indicadores financieros y, opcionalmente,
        los archivos CSV de cartera. La plataforma procesará la información y generará
        gráficos dinámicos de gestión financiera, cartera, deterioro, concentración,
        liquidez y calidad crediticia.
        </div>
        """, unsafe_allow_html=True)

        col_a, col_b = st.columns(2)

        with col_a:
            archivo_excel = st.file_uploader(
                "📂 Subir archivo Excel de indicadores",
                type=["xlsx", "xlsm"]
            )

        with col_b:
            archivos_csv = st.file_uploader(
                "📂 Subir archivos CSV de cartera",
                type=["csv"],
                accept_multiple_files=True
            )

        graficar = st.button("🚀 Graficar Dashboard")

        if graficar:

            if archivo_excel is None:
                st.error("Debes subir primero el archivo Excel de indicadores.")
                st.stop()

            with st.spinner("Procesando información financiera..."):

                pivot_bl = procesar_balance_excel(archivo_excel)

                if pivot_bl is None or pivot_bl.empty:
                    st.error("No fue posible procesar la hoja BL del archivo Excel.")
                    st.stop()

                cartera = procesar_archivos_cartera(archivos_csv)

            st.success("Información procesada correctamente.")

            st.markdown("### Resumen de carga")

            c1, c2, c3 = st.columns(3)

            c1.metric("Periodos BL", pivot_bl.shape[0])
            c2.metric("Códigos contables", pivot_bl.shape[1])

            if cartera is not None:
                c3.metric("Registros cartera", f"{len(cartera):,}")
            else:
                c3.metric("Registros cartera", "No cargado")

            periodos = pivot_bl.index.astype(str).tolist()

            # ==========================================
            # CÁLCULOS DESDE BALANCE BL
            # ==========================================

            cods_g1_num = [
                "1120", "12", "13", "141105",
                "141110", "144205", "144210"
            ]

            cartera_g1 = safe_sum(pivot_bl, cods_g1_num)

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
                "1120", "13", "141105",
                "141110", "144205", "144210"
            ] + [
                c for c in pivot_bl.columns
                if str(c).startswith("12")
            ]

            cartera_total_bl = safe_sum(pivot_bl, cods_cartera_total)

            crec_mensual = cartera_total_bl.pct_change(1) * 100
            crec_anual = cartera_total_bl.pct_change(12) * 100

            cods_14 = [
                c for c in pivot_bl.columns
                if str(c).startswith("14")
            ]

            cartera_bruta = safe_sum(pivot_bl, cods_14) + safe_sum(
                pivot_bl,
                ["146805", "146810"]
            )

            cods_1411 = [
                c for c in pivot_bl.columns
                if str(c).startswith("1411")
            ]

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

            diferencia_cartera = cartera_bruta.diff()
            cartera_nueva = diferencia_cartera.clip(lower=0)

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

            df_bl = pd.DataFrame({
                "Periodo": periodos,
                "Cartera_Activos": ratio_cartera_activos,
                "Crecimiento_Mensual": crec_mensual.values,
                "Crecimiento_Anual": crec_anual.values,
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
                "Depositos": depositos_g1.values
            })

            ultimo = df_bl.iloc[-1]

            st.markdown("### Indicadores principales")

            k1, k2, k3, k4, k5 = st.columns(5)

            k1.metric(
                "Cartera / Activos",
                f"{ultimo['Cartera_Activos']:.2f}%"
            )

            k2.metric(
                "Crec. Mensual Cartera",
                f"{ultimo['Crecimiento_Mensual']:.2f}%"
                if pd.notna(ultimo["Crecimiento_Mensual"])
                else "n/d"
            )

            k3.metric(
                "Crec. Anual Cartera",
                f"{ultimo['Crecimiento_Anual']:.2f}%"
                if pd.notna(ultimo["Crecimiento_Anual"])
                else "n/d"
            )

            k4.metric(
                "Cobertura Total",
                f"{ultimo['Cobertura_Total']:.2f}%"
            )

            k5.metric(
                "Cobertura Vencida",
                f"{ultimo['Cobertura_Vencida']:.2f} veces"
            )

            tab1, tab2, tab3, tab4, tab5 = st.tabs([
                "1. Estructura de cartera",
                "2. Calidad de cartera",
                "3. Deterioro",
                "4. Concentración",
                "5. Liquidez y CAMEL"
            ])

            # ==========================================
            # TAB 1
            # ==========================================

            with tab1:

                st.markdown("### Estructura de cartera")

                col1, col2 = st.columns(2)

                with col1:

                    fig_ca = grafico_linea(
                        df_bl,
                        "Periodo",
                        "Cartera_Activos",
                        "Cartera / Activos",
                        "#0B3C5D"
                    )

                    fig_ca.add_hline(
                        y=68,
                        line_dash="dash",
                        line_color="#F37021",
                        annotation_text="Referencia 68%"
                    )

                    st.plotly_chart(fig_ca, use_container_width=True)

                with col2:

                    fig_crec = go.Figure()

                    fig_crec.add_trace(go.Scatter(
                        x=df_bl["Periodo"],
                        y=df_bl["Crecimiento_Mensual"],
                        mode="lines+markers",
                        name="Crecimiento mensual",
                        line=dict(color="#0B3C5D", width=3)
                    ))

                    fig_crec.add_trace(go.Scatter(
                        x=df_bl["Periodo"],
                        y=df_bl["Crecimiento_Anual"],
                        mode="lines+markers",
                        name="Crecimiento anual",
                        line=dict(color="#F37021", width=3)
                    ))

                    fig_crec.update_layout(
                        template="plotly_white",
                        title="Crecimiento mensual y anual de cartera",
                        height=420,
                        hovermode="x unified"
                    )

                    st.plotly_chart(fig_crec, use_container_width=True)

                col3, col4 = st.columns(2)

                with col3:

                    fig_mix = grafico_barras_apiladas(
                        df_bl,
                        "Periodo",
                        ["Libranza", "No_Libranza"],
                        "Composición Libranza vs No Libranza"
                    )

                    st.plotly_chart(fig_mix, use_container_width=True)

                with col4:

                    fig_cal = grafico_barras_apiladas(
                        df_bl,
                        "Periodo",
                        ["A", "B", "C", "D", "E"],
                        "Cartera por calificación"
                    )

                    st.plotly_chart(fig_cal, use_container_width=True)

                fig_new = grafico_linea(
                    df_bl,
                    "Periodo",
                    "Cartera_Nueva",
                    "Cartera Nueva / Cartera Total",
                    "#F37021"
                )

                st.plotly_chart(fig_new, use_container_width=True)

            # ==========================================
            # TAB 2
            # ==========================================

            with tab2:

                st.markdown("### Calidad de cartera")

                if cartera is None:

                    st.warning(
                        "Para esta sección debes subir los archivos CSV de cartera."
                    )

                else:

                    cartera["Saldo_Vencido_90"] = cartera["SaldoCapital"].where(
                        cartera["Morosidad"] > 90,
                        0
                    )

                    resumen_icv = cartera.groupby("FECHA_CORTE").agg(
                        Saldo_Vencido_Total=("Saldo_Vencido_90", "sum"),
                        Saldo_Capital_Total=("SaldoCapital", "sum")
                    ).reset_index()

                    resumen_icv["ICV_90_Total"] = (
                        resumen_icv["Saldo_Vencido_Total"]
                        / resumen_icv["Saldo_Capital_Total"]
                    ) * 100

                    fig_icv = px.line(
                        resumen_icv,
                        x="FECHA_CORTE",
                        y="ICV_90_Total",
                        markers=True,
                        title="Evolución del ICV 90+"
                    )

                    fig_icv.add_hline(
                        y=5,
                        line_dash="dash",
                        line_color="#F37021",
                        annotation_text="Referencia 5%"
                    )

                    fig_icv.update_traces(
                        line=dict(color="#0B3C5D", width=3)
                    )

                    fig_icv.update_layout(
                        template="plotly_white",
                        height=420,
                        hovermode="x unified"
                    )

                    st.plotly_chart(fig_icv, use_container_width=True)

                    patronales_no_libranza = [
                        "ASOCIADO EXTERNO",
                        "EX-ASOCIADOS"
                    ]

                    cartera["Tipo_Cartera"] = np.where(
                        cartera["NombrePatronal"].isin(patronales_no_libranza),
                        "No Libranza",
                        "Libranza"
                    )

                    resumen_modalidad = cartera.groupby(
                        ["FECHA_CORTE", "Tipo_Cartera"]
                    ).agg(
                        Saldo_Vencido_Total=("Saldo_Vencido_90", "sum"),
                        Saldo_Capital_Total=("SaldoCapital", "sum")
                    ).reset_index()

                    resumen_modalidad["ICV_90"] = (
                        resumen_modalidad["Saldo_Vencido_Total"]
                        / resumen_modalidad["Saldo_Capital_Total"]
                    ) * 100

                    fig_icv_mod = px.line(
                        resumen_modalidad,
                        x="FECHA_CORTE",
                        y="ICV_90",
                        color="Tipo_Cartera",
                        markers=True,
                        title="ICV 90+ por modalidad"
                    )

                    fig_icv_mod.update_layout(
                        template="plotly_white",
                        height=420,
                        hovermode="x unified"
                    )

                    st.plotly_chart(fig_icv_mod, use_container_width=True)

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

                    comp_cal = cartera.groupby(
                        ["FECHA_CORTE", "Calificacion_Mora"]
                    )["SaldoCapital"].sum().reset_index()

                    total_mes = comp_cal.groupby("FECHA_CORTE")[
                        "SaldoCapital"
                    ].transform("sum")

                    comp_cal["Participacion"] = (
                        comp_cal["SaldoCapital"]
                        / total_mes
                    ) * 100

                    fig_rating = px.bar(
                        comp_cal,
                        x="FECHA_CORTE",
                        y="Participacion",
                        color="Calificacion_Mora",
                        title="Composición de cartera por calificación",
                    )

                    fig_rating.update_layout(
                        barmode="stack",
                        template="plotly_white",
                        height=420
                    )

                    st.plotly_chart(fig_rating, use_container_width=True)

            # ==========================================
            # TAB 3
            # ==========================================

            with tab3:

                st.markdown("### Deterioro y provisiones")

                col1, col2 = st.columns(2)

                with col1:

                    fig_cov_total = grafico_linea(
                        df_bl,
                        "Periodo",
                        "Cobertura_Total",
                        "Cobertura de Cartera Total",
                        "#0B3C5D"
                    )

                    st.plotly_chart(fig_cov_total, use_container_width=True)

                with col2:

                    fig_cov_vencida = grafico_linea(
                        df_bl,
                        "Periodo",
                        "Cobertura_Vencida",
                        "Cobertura de Cartera Vencida",
                        "#F37021"
                    )

                    st.plotly_chart(fig_cov_vencida, use_container_width=True)

            # ==========================================
            # TAB 4
            # ==========================================

            with tab4:

                st.markdown("### Concentración")

                if cartera is None:

                    st.warning(
                        "Para esta sección debes subir los archivos CSV de cartera."
                    )

                else:

                    top_deudores = (
                        cartera
                        .groupby(["NIT"])["SaldoCapital"]
                        .sum()
                        .reset_index()
                        .sort_values("SaldoCapital", ascending=False)
                        .head(20)
                    )

                    total_cartera = cartera["SaldoCapital"].sum()

                    top_deudores["Participacion"] = (
                        top_deudores["SaldoCapital"]
                        / total_cartera
                    ) * 100

                    fig_top_deudores = px.bar(
                        top_deudores,
                        x="NIT",
                        y="Participacion",
                        title="Top 20 deudores por concentración",
                        color="Participacion",
                        color_continuous_scale=["#0B3C5D", "#F37021"]
                    )

                    fig_top_deudores.update_layout(
                        template="plotly_white",
                        height=450
                    )

                    st.plotly_chart(
                        fig_top_deudores,
                        use_container_width=True
                    )

                    st.dataframe(
                        top_deudores,
                        use_container_width=True
                    )

                    if "AportesSociales" in cartera.columns:

                        top_ahorro = (
                            cartera
                            .groupby(["NIT"])["AportesSociales"]
                            .sum()
                            .reset_index()
                            .sort_values("AportesSociales", ascending=False)
                            .head(20)
                        )

                        total_ahorro = cartera["AportesSociales"].sum()

                        top_ahorro["Participacion"] = (
                            top_ahorro["AportesSociales"]
                            / total_ahorro
                        ) * 100

                        fig_top_ahorro = px.bar(
                            top_ahorro,
                            x="NIT",
                            y="Participacion",
                            title="Top 20 asociados por ahorro / aportes",
                            color="Participacion",
                            color_continuous_scale=["#0B3C5D", "#F37021"]
                        )

                        fig_top_ahorro.update_layout(
                            template="plotly_white",
                            height=450
                        )

                        st.plotly_chart(
                            fig_top_ahorro,
                            use_container_width=True
                        )

                        st.dataframe(
                            top_ahorro,
                            use_container_width=True
                        )

            # ==========================================
            # TAB 5
            # ==========================================

            with tab5:

                st.markdown("### Liquidez, fondeo y CAMEL")

                df_liq = df_bl.copy()

                df_liq["Depositos_Cartera"] = np.where(
                    df_liq["Cartera_Total"] != 0,
                    df_liq["Depositos"] / df_liq["Cartera_Total"] * 100,
                    0
                )

                df_liq["Activos_Liquidos_Depositos"] = 0

                col1, col2 = st.columns(2)

                with col1:

                    fig_dep_cart = grafico_linea(
                        df_liq,
                        "Periodo",
                        "Depositos_Cartera",
                        "Depósitos / Cartera",
                        "#0B3C5D"
                    )

                    fig_dep_cart.add_hline(
                        y=100,
                        line_dash="dash",
                        line_color="#F37021",
                        annotation_text="Referencia 100%"
                    )

                    st.plotly_chart(
                        fig_dep_cart,
                        use_container_width=True
                    )

                with col2:

                    fig_cartera_indice = grafico_linea(
                        df_liq,
                        "Periodo",
                        "Cartera_Total",
                        "Evolución de Cartera Total",
                        "#F37021"
                    )

                    st.plotly_chart(
                        fig_cartera_indice,
                        use_container_width=True
                    )

                st.info("""
                En esta sección podemos agregar después:
                
                • Activos líquidos / depósitos  
                • Brechas de liquidez  
                • IRL  
                • Dimensión L de CAMEL  
                • Alertas tempranas de fondeo  
                """)

            st.markdown("---")

            with st.expander("Ver tabla base procesada del Balance BL"):
                st.dataframe(df_bl, use_container_width=True)

            if cartera is not None:
                with st.expander("Ver tabla base procesada de cartera"):
                    st.dataframe(cartera.head(1000), use_container_width=True)

    # =====================================================
    # OTROS MÓDULOS
    # =====================================================

    elif st.session_state.modulo == "SARC":

        st.markdown("## 🏦 SARC")
        st.info("""
        Sistema de Administración de Riesgo de Crédito.

        Próximamente:
        • PD  
        • LGD  
        • EAD  
        • Pérdida Esperada  
        • NIIF 9  
        • Score de riesgo  
        """)

    elif st.session_state.modulo == "SARL":

        st.markdown("## 💧 SARL")
        st.info("""
        Sistema de Administración de Riesgo de Liquidez.

        Próximamente:
        • Brechas de liquidez  
        • IRL  
        • Stress testing  
        • Fondeo  
        """)

    elif st.session_state.modulo == "SARM":

        st.markdown("## 📈 SARM")
        st.info("""
        Sistema de Administración de Riesgo de Mercado.

        Próximamente:
        • VaR  
        • Duración  
        • Sensibilidades  
        • Monte Carlo  
        """)

    elif st.session_state.modulo == "SARO":

        st.markdown("## ⚙️ SARO")
        st.info("""
        Sistema de Administración de Riesgo Operacional.

        Próximamente:
        • Eventos de riesgo  
        • Matriz de probabilidad e impacto  
        • KRI  
        • Planes de acción  
        """)

    else:

        st.markdown("## Bienvenido a SolidRisk")

        st.markdown("""
        <div class='card'>
        Selecciona un módulo en el menú lateral para iniciar.
        </div>
        """, unsafe_allow_html=True)

    st.markdown(
        "<div class='footer'>© 2026 SolidRisk | By PwC - Analfe</div>",
        unsafe_allow_html=True
    )
