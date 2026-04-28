import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# Configuración de la página
st.set_page_config(page_title="Seguimiento de Garantías", layout="wide")

st.title("Gestión de Órdenes de Garantía")

# 1. CONEXIÓN A GOOGLE SHEETS
# Se usa st.connection para vincular con los Secrets de Streamlit
conn = st.connection("gsheets", type=GSheetsConnection)

# Intentar leer los datos actuales (ttl=0 para que no use memoria caché y siempre esté actualizado)
try:
    df_existente = conn.read(ttl=0)
except Exception:
    # Si la hoja está vacía o hay error, definimos las columnas base
    columnas = [
        "N° Orden", "Apertura", "Cierre", "Asesor", "Cliente", 
        "Codigo", "Descripcion", "Cargo", "Tiempo/Cantidad", 
        "Venta Neta", "Venta Total", "Costo neto", "Costo Total", 
        "Utilidad", "Sucursal", "Mes", "Año", "Estado"
    ]
    df_existente = pd.DataFrame(columns=columnas)

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
            cargo = st.text_input("Cargo")
        
        with col3:
            cantidad = st.number_input("Tiempo / Cantidad", min_value=0.0, step=0.1)
            v_neta = st.number_input("Venta Neta", min_value=0.0)
            c_neto = st.number_input("Costo Neto", min_value=0.0)

        submit = st.form_submit_button("Registrar Orden")

        if submit:
            if n_orden and cliente:
                # Cálculos automáticos (siguiendo tu lógica de auditoría)
                v_total = v_neta * 1.21
                c_total = c_neto * 1.10
                utilidad = v_total - c_total
                mes_nombre = cierre.strftime("%B")
                anio_num = cierre.year

                # Crear nueva fila de datos
                nueva_fila = pd.DataFrame([{
                    "N° Orden": n_orden,
                    "Apertura": str(apertura),
                    "Cierre": str(cierre),
                    "Asesor": asesor,
                    "Cliente": cliente,
                    "Codigo": codigo,
                    "Descripcion": descripcion,
                    "Cargo": cargo,
                    "Tiempo/Cantidad": cantidad,
                    "Venta Neta": v_neta,
                    "Venta Total": v_total,
                    "Costo neto": c_neto,
                    "Costo Total": c_total,
                    "Utilidad": utilidad,
                    "Sucursal": sucursal,
                    "Mes": mes_nombre,
                    "Año": anio_num,
                    "Estado": estado
                }])

                # Concatenar con los datos anteriores y subir a Google Sheets
                df_actualizado = pd.concat([df_existente, nueva_fila], ignore_index=True)
                conn.update(data=df_actualizado)
                
                st.success("✅ Orden guardada exitosamente en la nube.")
                st.rerun()
            else:
                st.warning("Por favor completa los campos obligatorios.")

# 3. VISUALIZACIÓN DE TABLA
st.subheader("📋 Historial de Órdenes Registradas")
st.dataframe(df_existente, use_container_width=True)
