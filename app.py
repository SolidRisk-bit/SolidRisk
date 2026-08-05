
import streamlit as st

st.title("🛡️ SolidRisk")

usuario = st.text_input("Usuario")
password = st.text_input("Contraseña", type="password")

if st.button("Ingresar"):
    if usuario == "admin" and password == "1234":
        st.success("Bienvenido a SolidRisk")
    else:
        st.error("Credenciales incorrectas")
