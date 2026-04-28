import streamlit as st
import pandas as pd
from datetime import datetime

# Configuración de la página
st.set_page_config(page_title="Carga de Garantías", layout="wide")

st.title("Seguimiento de Órdenes de Garantía")
st.write("Registra las órdenes aquí y descarga el reporte al finalizar.")

# --- INICIALIZACIÓN DEL ALMACENAMIENTO TEMPORAL ---
# Esto crea una tabla vacía en la memoria del navegador
if 'tabla_garantias' not in st.session_state:
    columnas = [
        "N° Orden", "Apertura", "Cierre", "Asesor", "Cliente", 
        "Codigo", "Descripcion", "Cargo", "Tiempo/Cantidad", 
        "Venta Neta", "Venta Total", "Costo neto", "Costo Total", 
        "Utilidad", "Sucursal", "Mes", "Año", "Estado"
    ]
    st.session_state.tabla_garantias = pd.DataFrame(columns=columnas)

# --- FORMULARIO DE CARGA ---
with st.form("formulario_registro", clear_on_submit=True):
    st.subheader("📝 Nueva Entrada")
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
        cargo = st.text_input("Cargo")
        cantidad = st.number_input("Tiempo / Cantidad", min_value=0.0, step=0.1)
        v_neta = st.number_input("Venta Neta", min_value=0.0)
        c_neto = st.number_input("Costo Neto", min_value=0.0)

    # Botón para añadir a la tabla
    submit = st.form_submit_button("Añadir a la lista")

    if submit:
        if n_orden:
            # Cálculos automáticos para que el Excel sea profesional
            v_total = v_neta * 1.21
            c_total = c_neto * 1.10
            utilidad = v_total - c_total
            
            nueva_fila = {
                "N° Orden": n_orden, "Apertura": str(apertura), "Cierre": str(cierre),
                "Asesor": asesor, "Cliente": cliente, "Codigo": codigo, 
                "Descripcion": descripcion, "Cargo": cargo, "Tiempo/Cantidad": cantidad,
                "Venta Neta": v_neta, "Venta Total": v_total, "Costo neto": c_neto,
                "Costo Total": c_total, "Utilidad": utilidad, "Sucursal": sucursal,
                "Mes": cierre.strftime("%B"), "Año": cierre.year, "Estado": estado
            }
            
            # Guardar en la memoria de la sesión
            st.session_state.tabla_garantias = pd.concat([
                st.session_state.tabla_garantias, 
                pd.DataFrame([nueva_fila])
            ], ignore_index=True)
            st.success(f"Orden {n_orden} añadida a la tabla.")
        else:
            st.error("Debes poner un número de orden.")

# --- VISTA PREVIA Y DESCARGA ---
st.divider()
st.subheader("📋 Órdenes Cargadas en esta Sesión")

if not st.session_state.tabla_garantias.empty:
    # Mostrar tabla
    st.dataframe(st.session_state.tabla_garantias, use_container_width=True)
    
    # Botón para descargar Excel
    csv = st.session_state.tabla_garantias.to_csv(index=False).encode('utf-8-sig')
    st.download_button(
        label="📥 Descargar todo como Excel (CSV)",
        data=csv,
        file_name=f"reporte_garantias_{datetime.now().strftime('%d_%m_%Y')}.csv",
        mime="text/csv",
    )
    
    if st.button("🗑️ Borrar toda la tabla"):
        st.session_state.tabla_garantias = st.session_state.tabla_garantias.iloc[0:0]
        st.rerun()
else:
    st.info("Aún no has cargado ninguna orden.")
