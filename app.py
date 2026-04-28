import streamlit as st
import pandas as pd
from datetime import datetime

# Configuración de la página
st.set_page_config(page_title="Seguimiento de Garantías", layout="wide")

st.title("Gestión de Órdenes de Garantía")

# URL de tu Google Sheet (formato export para que sea fácil de leer)
SHEET_ID = "1ieWebTpvY9Xmxiu8unftwgGUPk2x-3gWKWLPgjWP1ec"
SHEET_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv"

# 1. CARGAR DATOS (Lectura simple)
@st.cache_data(ttl=10) # Se actualiza cada 10 segundos
def cargar_datos():
    try:
        return pd.read_csv(SHEET_URL)
    except:
        return pd.DataFrame(columns=[
            "N° Orden", "Apertura", "Cierre", "Asesor", "Cliente", 
            "Codigo", "Descripcion", "Cargo", "Tiempo/Cantidad", 
            "Venta Neta", "Venta Total", "Costo neto", "Costo Total", 
            "Utilidad", "Sucursal", "Mes", "Año", "Estado"
        ])

df_existente = cargar_datos()

# 2. FORMULARIO DE CARGA
with st.expander("➕ Cargar Nueva Orden de Garantía", expanded=True):
    with st.form("formulario_carga"):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            n_orden = st.text_input("N° Orden")
            asesor = st.text_input("Asesor")
            cliente = st.text_input("Cliente")
            sucursal = st.selectbox("Sucursal", ["CHR CASA CENTRAL", "FIAT AZZURRA", "OTRA"])
            estado = st.selectbox("Estado", ["Iniciado", "Reclamado", "Pagado"])
        
        with col2:
            apertura = st.date_input("Fecha Apertura", datetime.now())
            cierre = st.date_input("Fecha Cierre", datetime.now())
            codigo = st.text_input("Código")
            descripcion = st.text_input("Descripción")
        
        with col3:
            cantidad = st.number_input("Tiempo / Cantidad", min_value=0.0)
            v_neta = st.number_input("Venta Neta", min_value=0.0)
            c_neto = st.number_input("Costo Neto", min_value=0.0)

        submit = st.form_submit_button("Registrar Orden")

        if submit:
            # Aquí generamos el link para que tú mismo pegues el dato si falla la conexión automática
            st.info("Para guardar de forma segura sin Google Cloud, descarga el archivo y súbelo al Drive, o usa el botón de abajo.")
            
            # Cálculo de datos
            v_total = v_neta * 1.21
            c_total = c_neto * 1.10
            utilidad = v_total - c_total
            
            nueva_fila = pd.DataFrame([{
                "N° Orden": n_orden, "Apertura": str(apertura), "Cierre": str(cierre),
                "Asesor": asesor, "Cliente": cliente, "Codigo": codigo, 
                "Descripcion": descripcion, "Tiempo/Cantidad": cantidad,
                "Venta Neta": v_neta, "Venta Total": v_total, "Costo neto": c_neto,
                "Costo Total": c_total, "Utilidad": utilidad, "Sucursal": sucursal,
                "Mes": cierre.strftime("%B"), "Año": cierre.year, "Estado": estado
            }])
            
            df_final = pd.concat([df_existente, nueva_fila], ignore_index=True)
            
            # Opción de descarga inmediata para no perder el dato
            csv = df_final.to_csv(index=False).encode('utf-8')
            st.download_button("💾 Haz clic aquí para descargar tu Excel actualizado", data=csv, file_name="reporte_garantias.csv")
            st.success("¡Datos procesados! Descarga el archivo y reemplázalo en tu Drive para mantener el orden.")

# 3. VISUALIZACIÓN
st.subheader("📋 Vista Previa del Excel")
st.dataframe(df_existente, use_container_width=True)
