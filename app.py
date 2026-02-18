import streamlit as st
from st_clickable_images import clickable_images
from pyairtable import Api
from datetime import datetime
import base64
import os
import time

# --- 1. CONFIGURACIÓN ---
st.set_page_config(page_title="Evaluación Aromatex", page_icon="🌸", layout="wide")

# --- 2. CSS ---
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&display=swap');
        html, body, [class*="css"], h1, h2, h3, p, div {
            font-family: 'Montserrat', sans-serif !important;
        }
        .stApp { background-color: #026456; }
        #MainMenu, footer, header { visibility: hidden; }
        h1 { color: white !important; text-align: center; font-size: 3.5rem; margin-bottom: 20px; font-weight: 800; }
        .progreso { color: rgba(255,255,255,0.7); text-align: center; font-size: 1.2rem; margin-bottom: 30px; }
        iframe { border: none !important; }
    </style>
""", unsafe_allow_html=True)

# --- 3. CONEXIÓN AIRTABLE ---
api_key = st.secrets.get("AIRTABLE_API_KEY")
base_id = st.secrets.get("AIRTABLE_BASE_ID")
table_name = st.secrets.get("AIRTABLE_TABLE_NAME")

try:
    api = Api(api_key)
    table = api.table(base_id, table_name)
except:
    pass

# --- 4. CARGADOR IMÁGENES ---
def imagen_a_base64(nombre_archivo):
    ruta = os.path.join(os.path.dirname(os.path.abspath(__file__)), nombre_archivo)
    try:
        with open(ruta, "rb") as f:
            return f"data:image/png;base64,{base64.b64encode(f.read()).decode()}"
    except:
        return "" 

imagenes_b64 = [
    imagen_a_base64("malo.png"), imagen_a_base64("regular.png"),
    imagen_a_base64("bueno.png"), imagen_a_base64("excelente.png")
]

logo_url = "https://aromatex.mx/cdn/shop/files/Asset_1_300x_dcd8525f-0371-4ef2-8b9b-2c8c8437f727.png?v=1742396079&width=200"

# --- 5. LÓGICA MEMORIA ---
if 'paso' not in st.session_state:
    st.session_state.paso = 1
    st.session_state.respuestas = {} 

encuesta = {
    1: {"titulo": "¿Cómo calificaría la experiencia de aroma hoy?", "etiquetas": ["Malo", "Regular", "Bueno", "Excelente"], "columna": "Experiencia_Aroma"},
    2: {"titulo": "¿Cómo calificaría el ambiente de nuestra tienda hoy?", "etiquetas": ["Malo", "Regular", "Bueno", "Excelente"], "columna": "Ambiente"},
    3: {"titulo": "¿El aroma hizo que su visita fuera más placentera?", "etiquetas": ["Para nada", "Un poco", "Bastante", "Totalmente"], "columna": "Aroma_Placentero"},
    4: {"titulo": "¿Relacionaría este aroma con nuestra marca en el futuro?", "etiquetas": ["Definitivamente no", "Probablemente no", "Probablemente sí", "Definitivamente sí"], "columna": "Relacion_Marca"}
}

placeholder = st.empty()

# --- 6. INTERFAZ ---
paso_actual = st.session_state.paso

if paso_actual <= 4:
    pregunta = encuesta[paso_actual]
    with placeholder.container():
        st.markdown(f"<p class='progreso'>Pregunta {paso_actual} de 4</p>", unsafe_allow_html=True)
        st.markdown(f"<h1>{pregunta['titulo']}</h1>", unsafe_allow_html=True)
        
        clic = clickable_images(
            imagenes_b64, titles=pregunta["etiquetas"], key=f"q_{paso_actual}", 
            div_style={"display": "flex", "justify-content": "center", "gap": "20px", "flex-wrap": "wrap", "background-color": "#026456", "padding": "20px"},
            img_style={"margin": "10px", "height": "160px", "width": "160px", "cursor": "pointer", "transition": "transform 0.2s", "border-radius": "50%", "background-color": "white", "padding": "5px", "box-shadow": "0 10px 20px rgba(0,0,0,0.2)"},
        )

        if clic > -1:
            st.session_state.respuestas[pregunta["columna"]] = pregunta["etiquetas"][clic]
            
            if paso_actual == 4:
                try:
                    table.create({
                        "Fecha": datetime.now().isoformat(),
                        "Sucursal": "General",
                        "Experiencia_Aroma": st.session_state.respuestas.get("Experiencia_Aroma", ""),
                        "Ambiente": st.session_state.respuestas.get("Ambiente", ""),
                        "Aroma_Placentero": st.session_state.respuestas.get("Aroma_Placentero", ""),
                        "Relacion_Marca": st.session_state.respuestas.get("Relacion_Marca", "")
                    })
                    st.session_state.paso = 5
                    st.rerun()
                except Exception as e:
                    # SI AIRTABLE FALLA, AHORA TE LO GRITARÁ EN ROJO
                    st.error(f"❌ Error al guardar en Airtable: {e}")
            else:
                st.session_state.paso += 1
                st.rerun()
            
        st.write("")
        st.markdown(f"""<div style="display: flex; justify-content: center; width: 100%; margin-top: 20px;"><img src="{logo_url}" width="150" style="opacity: 0.9;"></div>""", unsafe_allow_html=True)

elif paso_actual == 5:
    with placeholder.container():
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("<h1 style='font-size: 80px;'>¡Gracias por tu tiempo!</h1>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center; color: white;'>Tus respuestas nos ayudan a crear mejores experiencias.</h3>", unsafe_allow_html=True)
        st.markdown(f"""<div style="display: flex; justify-content: center; width: 100%; margin-top: 40px;"><img src="{logo_url}" width="150" style="opacity: 0.9;"></div>""", unsafe_allow_html=True)
        time.sleep(3)
        st.session_state.paso = 1
        st.session_state.respuestas = {}
        st.rerun()
