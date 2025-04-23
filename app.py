import streamlit as st
import pandas as pd
import numpy as np

st.title("📊 Comparador de Tiendas")

# Subida del archivo Excel
archivo = st.file_uploader("Sube el archivo Excel con los datos", type=["xlsx"])

if archivo is not None:
    df = pd.read_excel(archivo)
    df.columns = df.columns.map(str)

    # Crear columnas promedio mensual
    cols_acum = [col for col in df.columns if col.endswith("Acum")]
    for col in cols_acum:
        nueva_col = col.replace("Acum", "PromMes")
        df[nueva_col] = df[col] / 3

    # Selección de tiendas
    tiendas = df["Cebe"].unique()
    tienda1 = st.selectbox("Selecciona la Tienda 1", tiendas)
    tienda2 = st.selectbox("Selecciona la Tienda 2", tiendas, index=1 if len(tiendas) > 1 else 0)

    if tienda1 == tienda2:
        st.warning("Selecciona tiendas diferentes para comparar.")
    else:
        df1 = df[df["Cebe"] == tienda1].iloc[0]
        df2 = df[df["Cebe"] == tienda2].iloc[0]

        campos_gasto = [col for col in df.columns if col.endswith("PromMes")]
        campos_ingreso = ["Flujo PromMes", "Vta PromMes", "Venta_Ppto_Mes"]

        resultados = []

        for campo in campos_gasto:
            val1 = df1[campo]
            val2 = df2[campo]

            if pd.isna(val1) or pd.isna(val2):
                continue

            diferencia = val1 - val2
            perc_dif = ((val1 - val2) / val2 * 100) if val2 != 0 else np.nan

            if campo in campos_ingreso:
                if perc_dif > 10:
                    sugerencia = f"✅ {campo} en {tienda1} es {perc_dif:.1f}% mayor que en {tienda2}"
                elif perc_dif < -10:
                    sugerencia = f"⚠️ {campo} en {tienda1} es {abs(perc_dif):.1f}% menor que en {tienda2}"
                else:
                    sugerencia = f"👌 {campo} similar entre ambas tiendas (±{perc_dif:.1f}%)"
            else:
                if perc_dif > 10:
                    sugerencia = f"⚠️ {campo} en {tienda1} es {perc_dif:.1f}% más alto (gasto mayor)"
                elif perc_dif < -10:
                    sugerencia = f"✅ {campo} en {tienda1} es {abs(perc_dif):.1f}% más bajo (gasto controlado)"
                else:
                    sugerencia = f"👌 {campo} similar entre ambas tiendas (±{perc_dif:.1f}%)"

            resultados.append({
                "Tienda 1": tienda1,
                "Tienda 2": tienda2,
                "Tipo 1": df1["Tipo"],
                "Tipo 2": df2["Tipo"],
                "M2 Tienda 1": df1["M2"],
                "M2 Tienda 2": df2["M2"],
                "Plantilla Tienda 1": df1["Plantilla"],
                "Plantilla Tienda 2": df2["Plantilla"],
                "Indicador": campo,
                f"Monto {tienda1} ($)": round(val1, 2),
                f"Monto {tienda2} ($)": round(val2, 2),
                "Diferencia ($)": round(diferencia, 2),
                "Diferencia %": f"{perc_dif:.1f}%",
                "Sugerencia": sugerencia
            })

        df_comparacion = pd.DataFrame(resultados)

        # Mostrar resultados
        st.subheader("📋 Comparación entre tiendas")
        st.dataframe(df_comparacion)

        # Descargar archivo Excel
        from io import BytesIO
        buffer = BytesIO()
        df_comparacion.to_excel(buffer, index=False, engine='openpyxl')
        buffer.seek(0)

        st.download_button(
            label="📥 Descargar Excel",
            data=buffer,
            file_name=f"comparacion_{tienda1}_vs_{tienda2}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
