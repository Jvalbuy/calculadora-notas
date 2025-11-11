import streamlit as st
import pandas as pd

st.set_page_config(page_title="NOTAS SSAA", page_icon="💪", layout="wide")

# === CSS PERSONALIZADO PARA CAMPOS PEQUEÑOS ===
st.markdown("""
    <style>
    .block-container {
        padding-top: 1rem;
        padding-bottom: 0rem;
    }
    input[type="number"], input[type="text"] {
        width: 90px !important;  /* ≈ 3 cm */
        text-align: center;
    }
    .metric-box {
        background-color: #f8f9fa;
        padding: 10px;
        border-radius: 10px;
        border: 1px solid #ddd;
        margin-bottom: 5px;
    }
    </style>
""", unsafe_allow_html=True)

# === SELECCIÓN DE SEXO ===
sexo = st.radio("QUE TIENES?:", ["PITO", "PITA"])

# === FUNCIÓN PARA BUSCAR NOTA ===
def buscar_nota(valor, tabla, invertido=False):
    tabla_ordenada = sorted(tabla.items(), key=lambda x: float(x[0]), reverse=not invertido)
    for k, v in tabla_ordenada:
        if (not invertido and valor >= float(k)) or (invertido and valor <= float(k)):
            return v
    return min(tabla.values())

# === BAREMOS COMPLETOS ===
baremos = {
    "PITO": {
        "Salto": {
            71: 10, 70: 9.7, 69: 9.4, 68: 9.1, 67: 8.9, 66: 8.7, 65: 8.4, 64: 8.2, 63: 8.0,
            62: 7.8, 61: 7.6, 60: 7.4, 59: 7.2, 58: 7.0, 57: 6.8, 56: 6.6, 55: 6.4, 54: 6.2,
            53: 6.0, 52: 5.8, 51: 5.6, 50: 5.4, 49: 5.2, 48: 5.0
        },

        "Flexiones": {
            70: 10, 69: 9.8, 68: 9.6, 67: 9.4, 66: 9.2, 65: 9.1, 64: 9.0, 63: 8.9, 62: 8.8,
            61: 8.7, 60: 8.6, 59: 8.5, 58: 8.4, 57: 8.3, 56: 8.2, 55: 8.1, 54: 8.0, 53: 7.9,
            52: 7.8, 51: 7.7, 50: 7.6, 49: 7.5, 48: 7.4, 47: 7.3, 46: 7.2, 45: 7.1, 44: 7.0,
            43: 6.9, 42: 6.8, 41: 6.7, 40: 6.6, 39: 6.5, 38: 6.4, 37: 6.3, 36: 6.2, 35: 6.1,
            34: 6.0, 33: 5.9, 32: 5.8, 31: 5.7, 30: 5.6, 29: 5.5, 28: 5.4, 27: 5.3, 26: 5.2,
            25: 5.1, 24: 5.0
        },

        "Velocidad": {
            6.3: 10, 6.4: 9.6, 6.5: 9.2, 6.6: 8.8, 6.7: 8.4, 6.8: 8.0, 6.9: 7.6, 7.0: 7.2,
            7.1: 6.8, 7.2: 6.5, 7.3: 6.2, 7.4: 5.9, 7.5: 5.6, 7.6: 5.3, 7.7: 5.0
        },

        "1000m": {
            2.50: 10.0, 2.55: 9.5, 3.00: 9.0, 3.05: 8.5, 3.10: 8.0, 3.15: 7.5, 3.20: 7.0,
            3.25: 6.5, 3.30: 6.0, 3.31: 5.9, 3.32: 5.8, 3.33: 5.7, 3.34: 5.6, 3.35: 5.5,
            3.36: 5.4, 3.37: 5.3, 3.38: 5.2, 3.39: 5.1, 3.40: 5.0
        },

        "Natación": {
            28: 10, 29: 9.8, 30: 9.6, 31: 9.4, 32: 9.2, 33: 9.0, 34: 8.8, 35: 8.6, 36: 8.4,
            37: 8.2, 38: 8.0, 39: 7.8, 40: 7.6, 41: 7.4, 42: 7.2, 43: 7.0, 44: 6.8, 45: 6.6,
            46: 6.4, 47: 6.2, 48: 6.0, 49: 5.8, 50: 5.6, 51: 5.5, 52: 5.4, 53: 5.3, 54: 5.2,
            55: 5.1, 56: 5.0
        },

        # ✅ 6000m hombres completo
        "6000m": {
            21.00: 10.0, 22.00: 9.0, 23.00: 8.0, 24.00: 7.0, 25.00: 6.8, 26.00: 6.5,
            26.20: 6.45, 26.30: 6.40, 26.40: 6.35, 26.50: 6.30, 27.00: 6.25, 27.10: 6.20,
            27.20: 6.15, 27.30: 6.10, 27.40: 6.05, 27.50: 6.00, 28.00: 5.95, 28.10: 5.90,
            28.20: 5.85, 28.30: 5.80, 28.40: 5.75, 28.50: 5.70, 29.00: 5.65, 29.10: 5.60,
            29.20: 5.55, 29.30: 5.50, 29.40: 5.45, 29.50: 5.40, 30.00: 5.35, 30.10: 5.30,
            30.20: 5.25, 30.30: 5.20, 30.40: 5.20, 30.50: 5.15, 31.00: 5.15, 31.10: 5.10,
            31.20: 5.10, 31.30: 5.05, 31.40: 5.05, 31.50: 5.00, 32.00: 5.00
        }
    },

    "PITA": {
        "Salto": {56: 10, 55: 9.6, 54: 9.2, 53: 8.8, 52: 8.4, 51: 8.0, 50: 7.6, 49: 7.2,
                  48: 6.8, 47: 6.5, 46: 6.2, 45: 5.9, 44: 5.6, 43: 5.3, 42: 5.0},
        "Flexiones": {45: 10, 44: 9.8, 43: 9.6, 42: 9.4, 41: 9.2, 40: 9.0, 39: 8.8, 38: 8.6,
                      37: 8.4, 36: 8.2, 35: 8.0, 34: 7.8, 33: 7.6, 32: 7.4, 31: 7.2, 30: 7.0,
                      29: 6.8, 28: 6.6, 27: 6.4, 26: 6.2, 25: 6.0, 24: 5.8, 23: 5.6, 22: 5.4,
                      21: 5.3, 20: 5.2, 19: 5.1, 18: 5.0},
        "Velocidad": {7.2: 10, 7.3: 9.6, 7.4: 9.2, 7.5: 8.8, 7.6: 8.4, 7.7: 8.0, 7.8: 7.6,
                      7.9: 7.2, 8.0: 6.8, 8.1: 6.4, 8.2: 6.0, 8.3: 5.6, 8.4: 5.3, 8.5: 5.0},

        # ✅ 1000m mujeres completo
        "1000m": {
            3.20: 10, 3.30: 9, 3.40: 8, 3.50: 7, 3.60: 6, 3.70: 5,
            4.01: 5.9, 4.02: 5.8, 4.03: 5.7, 4.04: 5.6, 4.05: 5.5, 4.06: 5.4,
            4.07: 5.3, 4.08: 5.2, 4.09: 5.1, 4.10: 5.0
        },

        "Natación": {33: 10, 34: 9.8, 35: 9.6, 36: 9.4, 37: 9.2, 38: 9.0, 39: 8.8, 40: 8.6,
                     41: 8.4, 42: 8.2, 43: 8.0, 44: 7.8, 45: 7.6, 46: 7.4, 47: 7.2, 48: 7.0,
                     49: 6.8, 50: 6.6, 51: 6.4, 52: 6.2, 53: 6.1, 54: 6.0, 55: 5.9, 56: 5.8,
                     57: 5.7, 58: 5.6, 59: 5.5, 60: 5.4, 61: 5.3, 62: 5.2, 63: 5.1, 64: 5.0},

        # ✅ 6000m mujeres completo
        "6000m": {
            24: 10, 25: 9, 26: 8, 27: 7, 28: 6.5, 29: 6,
            30.00: 6.25, 30.10: 6.20, 30.20: 6.15, 30.30: 6.10, 30.40: 6.05, 30.50: 6.00,
            31.00: 5.95, 31.10: 5.90, 31.20: 5.85, 31.30: 5.80, 31.40: 5.75, 31.50: 5.70,
            32.00: 5.65, 32.10: 5.60, 32.20: 5.55, 32.30: 5.50, 32.40: 5.45, 32.50: 5.40,
            33.00: 5.35, 33.10: 5.30, 33.20: 5.30, 33.30: 5.25, 33.40: 5.25, 33.50: 5.20,
            34.00: 5.20, 34.10: 5.15, 34.20: 5.15, 34.30: 5.10, 34.40: 5.10, 34.50: 5.10,
            35.00: 5.05, 35.10: 5.05, 35.20: 5.05, 35.30: 5.00, 35.40: 5.00, 35.50: 5.00,
            36.00: 5.00
        }
    }
}

# === ENTRADA DE DATOS ===
st.subheader("Introduce tus resultados:")
salto = st.number_input("Salto vertical (cm)", min_value=0.0)
flexiones = st.number_input("Flexiones válidas", min_value=0)
velocidad = st.number_input("Tiempo 50m (segundos)", min_value=0.0, step=0.1)
mil = st.text_input("Tiempo 1000m (min:seg)", value="0:00")
natacion = st.number_input("Tiempo 50m natación (segundos)", min_value=0.0, step=0.1)
seis_mil = st.text_input("Tiempo 6000m (min:seg)", value="0:00")

def tiempo_a_minutos(t):
    try:
        m, s = t.split(":")
        return float(m) + float(s)/60
    except:
        return 999

mil_t = tiempo_a_minutos(mil)
seis_t = tiempo_a_minutos(seis_mil)

# === CÁLCULO DE NOTAS ===
tabla = baremos[sexo]
notas = {
    "Salto": buscar_nota(salto, tabla["Salto"]),
    "Flexiones": buscar_nota(flexiones, tabla["Flexiones"]),
    "Velocidad": buscar_nota(velocidad, tabla["Velocidad"], invertido=True),
    "1000m": buscar_nota(mil_t, tabla["1000m"], invertido=True),
    "Natación": buscar_nota(natacion, tabla["Natación"], invertido=True),
    "6000m": buscar_nota(seis_t, tabla["6000m"], invertido=True)
}

df = pd.DataFrame(list(notas.items()), columns=["Prueba", "Nota"])
media = sum(notas.values()) / len(notas)
nota_final = media * 0.9

st.subheader("📊 Resultados")
st.dataframe(df, use_container_width=True)

st.markdown(f"**Media de pruebas:** {media:.2f}")
st.markdown(f"**Nota Final (×0.9):** 🟩 {nota_final:.2f}")

if st.button("📤 Exportar a Excel"):
    df.to_excel("resultados_fisicas.xlsx", index=False)
    st.success("Archivo 'resultados_fisicas.xlsx' guardado correctamente ✅")
