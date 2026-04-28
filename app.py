import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# Configuración de página
st.set_page_config(page_title="Seguimiento de Garantías", layout="wide")

st.title("Gestión de Órdenes de Garantía (Conexión Google Sheets)")

# 1. ESTABLECER CONEXIÓN
# Nota: Debes configurar el archivo .streamlit/secrets.toml con el link de tu hoja
conn = st.connection("gsheets", type=GSheetsConnection)

# Leer datos existentes para visualización
df_existente = conn.read(ttl=0) # ttl=0 para que siempre traiga datos frescos

# Formulario de entrada
with st.expander("➕ Cargar Nueva Orden de Garantía", expanded=True):
    with st.form("formulario_carga"):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            n_orden = st.text_input("N° Orden")
            asesor = st.text_input("Asesor")
            cliente = st.text_input("Cliente")
            sucursal = st.selectbox("Sucursal", ["CHR CASA CENTRAL", "FIAT AZZURRA", "OTRA"])
            # NUEVA COLUMNA DE ESTADO
            estado = st.selectbox("Estado de la Orden", ["Iniciado", "Reclamado", "Pagado"])
        
        with col2:
            apertura = st.date_input("Fecha Apertura", datetime.now())
            cierre = st.date_input("Fecha Cierre", datetime.now())
            codigo = st.text_input("Código Repuesto/Servicio")
            descripcion = st.text_input("Descripción")
        
        with col3:
            cantidad = st.number_input("Tiempo / Cantidad Mano de Obra", min_value=0.0)
            venta_neta = st.number_input("Venta Neta Repuestos", min_value=0.0)
            costo_neto = st.number_input("Costo Neto", min_value=0.0)
            cargo = st.text_input("Cargo")

        submit = st.form_submit_button("Registrar en Google Sheets")

        if submit:
            # Cálculos automáticos
            venta_total = venta_neta * 1.21
            costo_total = costo_neto * 1.10
            utilidad = venta_total - costo_total
            mes = cierre.strftime("%B")
            anio = cierre.year

            # Crear el nuevo registro
            nueva_fila = pd.DataFrame([{
                "N° Orden": n_orden, "Apertura": str(apertura), "Cierre": str(cierre),
                "Asesor": asesor, "Cliente": cliente, "Codigo": codigo, 
                "Descripcion": descripcion, "Cargo": cargo, "Tiempo/Cantidad": cantidad,
                "Venta Neta": venta_neta, "Venta Total": venta_total, 
                "Costo neto": costo_neto, "Costo Total": costo_total, 
                "Utilidad": utilidad, "Sucursal": sucursal, "Mes": mes, 
                "Año": anio, "Estado": estado # Agregado al DataFrame
            }])

            # Combinar y actualizar la hoja
            df_actualizado = pd.concat([df_existente, nueva_fila], ignore_index=True)
            conn.update(data=df_actualizado)
            st.success("✅ Datos guardados permanentemente en Google Sheets.")
            st.rerun()

# Mostrar la tabla actualizada
st.subheader("📋 Historial de Garantías (Desde la Nube)")
st.dataframe(df_existente, use_container_width=True)
