
import streamlit as st

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Configurar título
st.title("📊 Dashboard de Datos Aleatorios")

# Generar datos aleatorios
np.random.seed(42)  # Para resultados reproducibles
data = pd.DataFrame({
    'Fecha': pd.date_range(start='2024-01-01', periods=100),
    'Ventas': np.random.randint(100, 1000, size=100),
    'Usuarios': np.random.randint(10, 100, size=100),
    'País': np.random.choice(['México', 'Colombia', 'Chile', 'Perú'], size=100)
})

# Mostrar tabla completa
if st.checkbox("Mostrar tabla de datos"):
    st.dataframe(data)

# Selección de país para filtrar
paises = data['País'].unique()
pais_seleccionado = st.selectbox("Filtrar por país:", ["Todos"] + list(paises))

if pais_seleccionado != "Todos":
    data = data[data['País'] == pais_seleccionado]

# Diseño en dos columnas
col1, col2 = st.columns(2)

# Gráfico de líneas
with col1:
    st.subheader("📈 Ventas a lo largo del tiempo")
    st.line_chart(data.set_index('Fecha')['Ventas'])

# Histograma de usuarios
with col2:
    st.subheader("📊 Distribución de usuarios")
    fig, ax = plt.subplots()
    ax.hist(data['Usuarios'], bins=10, color='skyblue', edgecolor='black')
    st.pyplot(fig)
