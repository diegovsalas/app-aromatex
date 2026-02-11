import streamlit as st
from st_clickable_images import clickable_images
from pyairtable import Api
from datetime import datetime
import base64
import os
import time

# --- 1. CONFIGURACIÓN ---
st.set_page_config(page_title="Evaluación Aromatex", page_icon="🌸", layout="wide")

# --- 2. CSS DE MAQUILLAJE ---
st.markdown("""
    <style>
        /* Fondo Verde Global */
        .stApp { background-color: #026456; }
        
        /* Ocultar elementos molestos */
        #MainMenu, footer, header { visibility: hidden; }
        
        /* Título */
        h1 {
            color: white !important;
            text-align: center;
            font-family: sans-serif;
            font-size: 3.5rem;
            margin-bottom: 20px;
            font-weight: 800;
        }
        
        /* Hack para quitar bordes del componente */
        iframe { border: none !important; }
    </style>
""", unsafe_allow_html=True)

# --- 3. CONEXIÓN AIRTABLE ---
try:
    api = Api(st.secrets["AIRTABLE_API_KEY"])
    table = api.table(st.secrets["AIRTABLE_BASE_ID"], st.secrets["AIRTABLE_TABLE_NAME"])
except:
    pass

# --- 4. CARGADOR DE IMÁGENES ---
def imagen_a_base64(nombre_archivo):
    ruta = os.path.join(os.path.dirname(os.path.abspath(__file__)), nombre_archivo)
    try:
        with open(ruta, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
        return f"data:image/png;base64,{encoded_string}"
    except FileNotFoundError:
        return "" 

imagenes_b64 = [
    imagen_a_base64("malo.png"),
    imagen_a_base64("regular.png"),
    imagen_a_base64("bueno.png"),
    imagen_a_base64("excelente.png")
]

logo_url = "https://aromatex.mx/cdn/shop/files/Asset_1_300x_dcd8525f-0371-4ef2-8b9b-2c8c8437f727.png?v=1742396079&width=200"

# --- 5. INTERFAZ ---
if 'enviado' not in st.session_state:
    st.session_state['enviado'] = False

placeholder = st.empty()

if not st.session_state['enviado']:
    with placeholder.container():
        st.markdown("<h1>¿Cómo calificas la experiencia de aroma hoy?</h1>", unsafe_allow_html=True)
        
        # --- SOLUCIÓN AL CUADRO NEGRO ---
        clic = clickable_images(
            imagenes_b64, 
            titles=["No me gusta", "No es bueno", "Me gusta", "Me encanta"],
            div_style={
                "display": "flex", 
                "justify-content": "center", 
                "align-items": "center",
                "gap": "20px",
                "flex-wrap": "wrap",
                "background-color": "#026456",
                "padding": "20px"
            },
            img_style={
                "margin": "10px", 
                "height": "160px",
                "width": "160px",
                "cursor": "pointer", 
                "transition": "transform 0.2s", 
                "border-radius": "50%", 
                "background-color": "white", 
                "padding": "5px",
                "box-shadow": "0 10px 20px rgba(0,0,0,0.2)"
            },
        )

        if clic > -1:
            calificaciones = [1, 2, 3, 4]
            etiquetas = ["Malo", "Regular", "Bueno", "Excelente"]
            try:
                table.create({
                    "Fecha": datetime.now().isoformat(),
                    "Sucursal": "General",
                    "Calificacion": calificaciones[clic],
                    "Etiqueta": etiquetas[clic]
                })
            except:
                pass
            st.session_state['enviado'] = True
            st.rerun()
            
        st.write("")
        st.write("")

        # --- SOLUCIÓN LOGO CENTRADO (HTML PURO) ---
        st.markdown(f"""
            <div style="display: flex; justify-content: center; width: 100%; margin-top: 20px;">
                <img src="{logo_url}" width="150" style="opacity: 0.9;">
            </div>
        """, unsafe_allow_html=True)

else:
    # PANTALLA DE GRACIAS
    with placeholder.container():
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("<h1 style='font-size: 80px;'>¡Gracias!</h1>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center; color: white;'>Tu opinión nos ayuda a mejorar.</h3>", unsafe_allow_html=True)
        
        st.write("")
        
        # Logo también centrado aquí
        st.markdown(f"""
            <div style="display: flex; justify-content: center; width: 100%; margin-top: 40px;">
                <img src="{logo_url}" width="150" style="opacity: 0.9;">
            </div>
        """, unsafe_allow_html=True)
        
        time.sleep(2.5)
        st.session_state['enviado'] = False
        st.rerun()