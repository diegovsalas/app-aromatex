import streamlit as st
from st_clickable_images import clickable_images
from pyairtable import Api
from datetime import datetime
import base64
import os
import time

# --- 1. CONFIGURACIÓN ---
st.set_page_config(page_title="Evaluación Aromatex", page_icon="🌸", layout="wide")

# --- 2. CSS DE BLINDAJE EXTREMO (KIOSCO) ---
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&display=swap');
        
        /* 1. MATAR EL SCROLL DE RAÍZ Y EL EFECTO REBOTE */
        html, body {
            font-family: 'Montserrat', sans-serif !important;
            overflow: hidden !important;
            overscroll-behavior: none !important; /* Elimina el rebote del iPad */
            position: fixed !important; /* Fija la página por completo */
            width: 100vw !important;
            height: 100vh !important;
            margin: 0 !important;
            padding: 0 !important;
            touch-action: none !important; /* Bloquea gestos en el fondo verde */
        }

        /* 2. BLOQUEAR LOS CONTENEDORES OCULTOS DE STREAMLIT */
        .stApp, [data-testid="stAppViewContainer"], [data-testid="stMain"], [data-testid="stMainBlockContainer"] {
            overflow: hidden !important;
            overscroll-behavior: none !important;
            height: 100vh !important;
            touch-action: none !important;
        }

        /* 3. EVITAR SELECCIÓN Y ARRASTRE DE TEXTO/IMÁGENES */
        * {
            -webkit-user-select: none !important;
            user-select: none !important;
            -webkit-touch-callout: none !important;
        }
        
        img {
            -webkit-user-drag: none !important;
            user-drag: none !important;
            pointer-events: auto !important;
        }

        /* 4. DISEÑO BASE */
        .stApp { background-color: #026456 !important; }
        #MainMenu, footer, header, [data-testid="stHeader"] { display: none !important; }
        
        /* Ajuste de posición para que quede centrado sin poder hacer scroll */
        h1 { 
            color: white !important; 
            text-align: center; 
            font-size: 3.5rem; 
            margin-top: 8vh !important; 
            margin-bottom: 40px !important; 
            font-weight: 800; 
            font-family: 'Montserrat', sans-serif !important;
        }
        
        /* Asegurar que el iframe de las caritas pueda recibir clics */
        iframe { border: none !important; pointer-events: auto !important; }
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
    imagen_a_base64("malo.png"), 
    imagen_a_base64("regular.png"),
    imagen_a_base64("bueno.png"), 
    imagen_a_base64("excelente.png")
]

logo_url = "https://aromatex.mx/cdn/shop/files/Asset_1_300x_dcd8525f-0371-4ef2-8b9b-2c8c8437f727.png?v=1742396079&width=200"

# --- 5. INTERFAZ (PREGUNTA ÚNICA) ---
if 'enviado' not in st.session_state:
    st.session_state['enviado'] = False

placeholder = st.empty()

if not st.session_state['enviado']:
    with placeholder.container():
        st.markdown("<h1>¿Que le pareció el aroma de la tienda?</h1>", unsafe_allow_html=True)
        
        clic = clickable_images(
            imagenes_b64, 
            titles=["Malo", "Regular", "Bueno", "Excelente"], 
            div_style={
                "display": "flex", "justify-content": "center", "gap": "20px", 
                "flex-wrap": "wrap", "background-color": "#026456", "padding": "20px"
            },
            img_style={
                "margin": "10px", "height": "160px", "width": "160px", 
                "cursor": "pointer", "transition": "transform 0.2s", 
                "border-radius": "50%", "background-color": "white", 
                "padding": "5px", "box-shadow": "0 10px 20px rgba(0,0,0,0.2)"
            },
        )

        if clic > -1:
            try:
                table.create({
                    "Fecha": datetime.now().isoformat(),
                    "Sucursal": "General",
                    "Calificacion": [1, 2, 3, 4][clic],
                    "Etiqueta": ["Malo", "Regular", "Bueno", "Excelente"][clic]
                })
                st.session_state['enviado'] = True
                st.rerun()
            except Exception as e:
                st.error(f"❌ Error al guardar en Airtable: {e}")
            
        st.write("")
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
        st.markdown("<h3 style='text-align: center; color: white;'>Su opinión nos ayuda a mejorar.</h3>", unsafe_allow_html=True)
        st.markdown(f"""
            <div style="display: flex; justify-content: center; width: 100%; margin-top: 40px;">
                <img src="{logo_url}" width="150" style="opacity: 0.9;">
            </div>
        """, unsafe_allow_html=True)
        
        time.sleep(3)
        st.session_state['enviado'] = False
        st.rerun()
