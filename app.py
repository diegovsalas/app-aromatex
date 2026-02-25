import streamlit as st
import streamlit.components.v1 as components
from st_clickable_images import clickable_images
from pyairtable import Api
from datetime import datetime
import base64
import os
import time

# --- 1. CONFIGURACIÓN ---
st.set_page_config(page_title="Evaluación Aromatex", page_icon="🌸", layout="centered")

# --- 2. ESCUDO ANTI-ZOOM (JAVASCRIPT) ---
js_lockdown = """
<script>
    const doc = window.parent.document;
    doc.addEventListener('touchmove', function (event) {
        if (event.scale !== 1 || event.touches.length > 1) { event.preventDefault(); }
    }, { passive: false });
    let lastTouchEnd = 0;
    doc.addEventListener('touchend', function (event) {
        const now = (new Date()).getTime();
        if (now - lastTouchEnd <= 300) { event.preventDefault(); }
        lastTouchEnd = now;
    }, false);
</script>
"""
components.html(js_lockdown, height=0, width=0)

# --- 3. CSS (EL TRUCO DE LA TARJETA) ---
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap');
        
        /* BLINDAJE KIOSCO TOTAL */
        html, body {
            font-family: 'Poppins', sans-serif !important;
            overflow: hidden !important;
            overscroll-behavior: none !important;
            position: fixed !important;
            width: 100vw !important;
            height: 100vh !important;
            margin: 0 !important; padding: 0 !important;
            touch-action: none !important; 
            -webkit-user-select: none !important; user-select: none !important;
        }
        
        /* 1. EL FONDO DE LA PANTALLA (VIOLETA) */
        .stApp {
            background-color: #6A4C9C !important; 
        }

        /* 2. LA TARJETA BLANCA */
        [data-testid="stMainBlockContainer"] {
            background-color: white !important;
            border-radius: 20px !important;
            padding: 40px !important;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3) !important;
            max-width: 600px !important;
            margin: 15vh auto !important;
        }

        /* OCULTAR ELEMENTOS EXTRA */
        #MainMenu, footer, header, [data-testid="stHeader"] { display: none !important; }
        iframe { border: none !important; pointer-events: auto !important; }

        /* TEXTOS DENTRO DE LA TARJETA */
        .card-title {
            color: #888;
            font-size: 14px;
            font-weight: 600;
            letter-spacing: 2px;
            text-align: center;
            margin-bottom: 10px;
        }
        .card-question {
            color: #333;
            font-size: 24px;
            font-weight: 700;
            line-height: 1.3;
            text-align: center;
            margin-bottom: 30px;
        }
        .labels-container {
            display: flex;
            justify-content: space-between;
            padding: 0 15px;
            margin-top: -10px;
            color: #888;
            font-size: 14px;
            font-weight: 600;
        }
    </style>
""", unsafe_allow_html=True)

# --- 4. CONEXIÓN AIRTABLE ---
api_key = st.secrets.get("AIRTABLE_API_KEY")
base_id = st.secrets.get("AIRTABLE_BASE_ID")
table_name = st.secrets.get("AIRTABLE_TABLE_NAME")
try:
    api = Api(api_key); table = api.table(base_id, table_name)
except: pass

# --- 5. CARGADOR IMÁGENES ---
def cargar_imagen(nombre):
    ruta = os.path.join(os.path.dirname(os.path.abspath(__file__)), nombre)
    try:
        with open(ruta, "rb") as f: return f"data:image/png;base64,{base64.b64encode(f.read()).decode()}"
    except: return "" 

# RECUERDA: Tienes que subir 5 imágenes a GitHub para que queden los 5 botones perfectos.
imagenes = [
    cargar_imagen("malo.png"), 
    cargar_imagen("malo.png"),      
    cargar_imagen("regular.png"),   
    cargar_imagen("bueno.png"), 
    cargar_imagen("excelente.png")
]

# --- 6. INTERFAZ ---
if 'enviado' not in st.session_state: st.session_state['enviado'] = False
placeholder = st.empty()

if not st.session_state['enviado']:
    with placeholder.container():
        # Título y Pregunta
        st.markdown('<div class="card-title">AROMATEX</div>', unsafe_allow_html=True)
        st.markdown('<div class="card-question">¿Cómo fue tu experiencia con el aroma de esta sucursal?</div>', unsafe_allow_html=True)
        
        # Emojis 
        clic = clickable_images(
            imagenes, 
            titles=["Terrible", "Malo", "Regular", "Bueno", "Excelente"], 
            div_style={
                "display": "flex", 
                "justify-content": "space-between", 
                "gap": "10px", 
                "background-color": "white", 
                "padding": "10px"
            },
            img_style={
                "width": "65px", "height": "65px", 
                "cursor": "pointer", "transition": "transform 0.2s"
            }
        )

        # Etiquetas (Terrible - Excelente)
        st.markdown("""
            <div class="labels-container">
                <span>Terrible</span>
                <span>Excelente</span>
            </div>
        """, unsafe_allow_html=True)

        # Lógica de Airtable
        if clic > -1:
            try:
                table.create({
                    "Fecha": datetime.now().isoformat(), "Sucursal": "General",
                    "Calificacion": [1, 2, 3, 4, 5][clic], 
                    "Etiqueta": ["Terrible", "Malo", "Regular", "Bueno", "Excelente"][clic]
                })
            except Exception as e: st.error(f"❌ Error en Airtable: {e}")
            st.session_state['enviado'] = True; st.rerun()

else:
    # PANTALLA DE GRACIAS
    with placeholder.container():
        st.markdown('<div class="card-title">AROMATEX</div>', unsafe_allow_html=True)
        st.markdown('<div style="font-size: 80px; text-align: center; color: #4CAF50; margin: 20px 0;">✅</div>', unsafe_allow_html=True)
        st.markdown('<div class="card-question">¡Gracias por tu opinión!</div>', unsafe_allow_html=True)
        time.sleep(3); st.session_state['enviado'] = False; st.rerun()
