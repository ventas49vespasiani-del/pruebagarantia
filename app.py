import streamlit as st
import pandas as pd
from datetime import datetime

# Configuración de la página
st.set_page_config(page_title="Carga de Garantías", layout="wide")

st.title("Seguimiento de Órdenes de Garantía")
st.info("Los datos se mantienen mientras la pestaña esté abierta. Descarga el reporte antes de cerrar.")

# --- DEFINICIÓN DEL ORDEN DE COLUMNAS (Tal cual se carga en la ficha) ---
COLUMNAS_ORDENADAS = [
    "N° Orden", "Asesor", "Cliente", "Sucursal", "Estado",  # Grupo 1 (col1)
    "Apertura", "Cierre", "Codigo", "Descripcion",           # Grupo 2 (col2)
    "Cargo", "Tiempo/Cantidad", "Venta Neta", "Costo Neto", # Grupo 3 (col3)
    "Venta Total", "Costo Total", "Utilidad", "Mes", "Año"  # Calculados
]

# Inicialización del almacenamiento temporal
if 'tabla_garantias' not in st.session_state:
    st.session_state.tabla_garantias = pd.DataFrame(columns=COLUMNAS_ORDENADAS)

# --- FORMULARIO DE CARGA ---
with st.form("formulario_registro", clear_on_submit=True):
    st.subheader("📝 Ficha de Carga")
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
        v_neta = st.number_input("Venta Neta (Repuestos)", min_value=0.0)
        c_neto = st.number_input("Costo Neto", min_value=0.0)

    submit = st.form_submit_button("Añadir a la lista")

    if submit:
        if n_orden:
            # Cálculos automáticos (siguiendo tu estructura de auditoría)
            v_total = v_neta * 1.21
            c_total = c_neto * 1.10
            utilidad = v_total - c_total
            
            nueva_fila = {
                "N° Orden": n_orden,
                "Asesor": asesor,
                "Cliente": cliente,
                "Sucursal": sucursal,
                "Estado": estado,
                "Apertura": str(apertura),
                "Cierre": str(cierre),
                "Codigo": codigo,
                "Descripcion": descripcion,
                "Cargo": cargo,
                "Tiempo/Cantidad": cantidad,
                "Venta Neta": v_neta,
                "Costo Neto": c_neto,
                "Venta Total": round(v_total, 2),
                "Costo Total": round(c_total, 2),
                "Utilidad": round(utilidad, 2),
                "Mes": cierre.strftime("%B"),
                "Año": cierre.year
            }
            
            # Guardar en la memoria
            st.session_state.tabla_garantias = pd.concat([
                st.session_state.tabla_garantias, 
                pd.DataFrame([nueva_fila])
            ], ignore_index=True)
            st.success(f"✅ Orden {n_orden} agregada.")
        else:
            st.error("El número de orden es obligatorio.")

# --- VISTA PREVIA Y EXPORTACIÓN ---
st.divider()
if not st.session_state.tabla_garantias.empty:
    st.subheader("📋 Vista Previa del Reporte")
    
    # Reordenar las columnas antes de mostrar y descargar (por seguridad)
    df_export = st.session_state.tabla_garantias[COLUMNAS_ORDENADAS]
    
    st.dataframe(df_export, use_container_width=True)
    
    # Botón para descargar Excel (formato CSV compatible)
    csv = df_export.to_csv(index=False).encode('utf-8-sig')
    st.download_button(
        label="📥 Descargar Reporte en Columnas Ordenadas",
        data=csv,
        file_name=f"garantias_ficha_{datetime.now().strftime('%H%M')}.csv",
        mime="text/csv",
    )
    
    if st.button("🗑️ Vaciar lista actual"):
        st.session_state.tabla_garantias = pd.DataFrame(columns=COLUMNAS_ORDENADAS)
        st.rerun()
else:
    st.info("Aún no has ingresado datos.")
