import streamlit as st
import pandas as pd
from pathlib import Path

# -----------------------------------------------------
# Paths (ajusta si usas otros nombres/ubicaciones)
# -----------------------------------------------------
DATA_DIR = Path(__file__).resolve().parent.parent / "data"

# Archivos generados en el notebook
histogram_path = DATA_DIR / "histograma_tmin.png"
map_path = DATA_DIR / "mapa_tmin_distritos.png"
ranking_cold_csv = DATA_DIR / "ranking_distritos_mas_frios.csv"
ranking_hot_csv = DATA_DIR / "ranking_distritos_mas_calidos.csv"

# -----------------------------------------------------
# Cargar datos
# -----------------------------------------------------
@st.cache_data
def load_data():
    top_cold = pd.read_csv(ranking_cold_csv)
    top_hot = pd.read_csv(ranking_hot_csv)
    return top_cold, top_hot

top_cold, top_hot = load_data()

# -----------------------------------------------------
# Sidebar – navegación
# -----------------------------------------------------
st.sidebar.title("Peru Tmin Dashboard")
page = st.sidebar.radio("Ir a:", [
    "📑 Data description",
    "📊 Raster data analysis",
    "🏛️ Public policy proposals"
])

# -----------------------------------------------------
# 1. Data description
# -----------------------------------------------------
if page == "📑 Data description":
    st.title("Peru Minimum Temperature (Tmin) Dashboard")
    st.markdown("""
    **Fuentes de datos:**
    - Raster Tmin: Servicio Nacional de Meteorología e Hidrología del Perú (SENAMHI) / Google Drive del curso.
    - Shapefile distritos: INEI – Cartografía distrital EPSG:4326.
    
    **Contexto:**
    Este panel analiza temperaturas mínimas en distritos del Perú 
    (Band 1 = 2020, Band 2 = 2021, etc.).  
    Se calculan estadísticas zonales (mean, min, max, std, p10, p90) 
    para identificar riesgos de friaje y heladas.

    **Estructura del repositorio:**  
    - `/app/app.py` (esta aplicación)  
    - `/data/` (archivos PNG y CSV)  
    - `/notebooks/code.ipynb` (cálculos y EDA)  
    """)

# -----------------------------------------------------
# 2. Raster data analysis
# -----------------------------------------------------
elif page == "📊 Raster data analysis":
    st.title("Raster Data Analysis – Zonal Statistics")

    st.subheader("Distribución de Tmin por distrito")
    st.image(histogram_path, caption="Histograma de Tmin", use_container_width=True)

    st.subheader("Top 15 distritos más fríos")
    st.dataframe(top_cold)
    st.download_button(
        "📥 Descargar ranking distritos más fríos CSV",
        data=top_cold.to_csv(index=False),
        file_name="ranking_distritos_mas_frios.csv",
        mime="text/csv"
    )

    st.subheader("Top 15 distritos más cálidos")
    st.dataframe(top_hot)
    st.download_button(
        "📥 Descargar ranking distritos más cálidos CSV",
        data=top_hot.to_csv(index=False),
        file_name="ranking_distritos_mas_calidos.csv",
        mime="text/csv"
    )

    st.subheader("Mapa cloroplético de Tmin por distrito")
    st.image(map_path, caption="Mapa Tmin por distrito (PNG)", use_container_width=True)

# -----------------------------------------------------
# 3. Public policy proposals
# -----------------------------------------------------
elif page == "🏛️ Public policy proposals":
    st.title("Public Policy Proposals")

    st.markdown("""
    **Diagnóstico:**  
    - En distritos altoandinos (Puno, Cusco, Ayacucho, Huancavelica, Pasco), 
      temperaturas mínimas bajo 0 °C generan riesgo de heladas, enfermedades respiratorias 
      y pérdidas agrícolas/ganaderas.  
    - En distritos amazónicos (Loreto, Ucayali, Madre de Dios), 
      friajes estacionales impactan salud pública y logística escolar.

    **Medidas priorizadas:**
    """)

    st.markdown("""
    1. **Mejora de infraestructura térmica (ISUR / Viviendas Saludables)**  
       - **Objetivo:** Reducir ARI y mortalidad infantil.  
       - **Población objetivo:** Distritos con Tmin ≤ p10.  
       - **Costo estimado:** S/ 5,000 por vivienda.  
       - **KPI:** -20% de casos ARI en ESSALUD/MINSA.

    2. **Kits antiheladas y cobertizos para ganado**  
       - **Objetivo:** Disminuir mortalidad de alpacas y ovinos.  
       - **Población objetivo:** Productores altoandinos.  
       - **Costo estimado:** S/ 1,500 por unidad productiva.  
       - **KPI:** -25% mortalidad alpaca.

    3. **Calendarios agrícolas adaptados y alertas tempranas**  
       - **Objetivo:** Ajustar fechas de siembra y cosecha frente a friajes.  
       - **Población objetivo:** Distritos amazónicos y andinos vulnerables.  
       - **Costo estimado:** S/ 2 millones anuales para SENAMHI/AGRORURAL.  
       - **KPI:** +15% de adopción de calendarios climáticamente inteligentes.
    """)

    st.info("💡 Estas propuestas son ejemplos y deben ser ajustadas con datos reales de población y costos.")

# -----------------------------------------------------
# Footer
# -----------------------------------------------------
st.sidebar.markdown("---")
st.sidebar.markdown("Desarrollado para la tarea de Python Data Science")
