import streamlit as st
from st_clickable_images import clickable_images
import base64
import os
import time

# --- 1. CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Evaluación Aromatex", page_icon="🌸", layout="centered")

# --- 2. CSS PERSONALIZADO (DISEÑO DE TARJETA Y BLINDAJE) ---
st.markdown("""
    <style>
        /* Importar fuente limpia */
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap');

        /* --- BLINDAJE KIOSCO (Sin scroll ni zoom) --- */
        html, body {
            height: 100%;
            margin: 0;
            overflow: hidden !important; /* Adiós scroll */
            touch-action: none; /* Adiós zoom táctil */
            -webkit-user-select: none; /* No seleccionar texto */
            user-select: none;
        }
        
        /* --- ESTILOS GENERALES --- */
        .stApp {
            background-color: #6A4C9C; /* Color de fondo violeta */
            font-family: 'Poppins', sans-serif;
            display: flex;
            align-items: center; /* Centrado vertical */
            justify-content: center; /* Centrado horizontal */
        }

        /* Ocultar elementos de Streamlit */
        #MainMenu, header, footer, .stDeployButton {
            display: none !important;
        }

        /* --- DISEÑO DE LA TARJETA BLANCA --- */
        .card-container {
            background-color: white;
            padding: 40px;
            border-radius: 20px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.2);
            text-align: center;
            width: 90%;
            max-width: 500px; /* Ancho máximo de la tarjeta */
        }

        /* Título pequeño AROMATEX */
        .card-title {
            color: #888;
            font-size: 14px;
            font-weight: 600;
            letter-spacing: 1px;
            margin-bottom: 10px;
        }

        /* Pregunta principal */
        .card-question {
            color: #333;
            font-size: 22px;
            font-weight: 700;
            line-height: 1.3;
            margin-bottom: 30px;
        }

        /* Contenedor de las etiquetas debajo de los emojis */
        .labels-container {
            display: flex;
            justify-content: space-between;
            padding: 0 10px;
            margin-top: -10px;
            color: #888;
            font-size: 14px;
            font-weight: 500;
        }

        /* Ajuste para el componente de imágenes clickeables */
        .stClickableImages {
            justify-content: center;
        }
    </style>
""", unsafe_allow_html=True)

# --- 3. FUNCIÓN PARA CARGAR IMÁGENES ---
def cargar_imagen(nombre):
    """Carga una imagen local y la convierte a base64."""
    try:
        ruta = os.path.join(os.path.dirname(os.path.abspath(__file__)), nombre)
        with open(ruta, "rb") as image_file:
            encoded = base64.b64encode(image_file.read()).decode()
        return f"data:image/png;base64,{encoded}"
    except FileNotFoundError:
        return f"https://via.placeholder.com/150/cccccc/ffffff?text={nombre}" # Placeholder si falla

# --- 4. CARGAR LOS 5 EMOJIS ---
# NOTA: Reemplaza estos nombres con los de tus 5 imágenes de emojis nuevas.
# Deben ser 5 para coincidir con el diseño del ejemplo.
imagenes = [
    cargar_imagen("malo.png"),      # Emoji 1 (Rojo/Terrible)
    cargar_imagen("regular.png"),   # Emoji 2
    cargar_imagen("bueno.png"),     # Emoji 3 (Neutro)
    cargar_imagen("excelente.png"), # Emoji 4
    cargar_imagen("excelente.png")  # Emoji 5 (Verde/Excelente) - Repetido temporalmente
]

# --- 5. LÓGICA DE LA APLICACIÓN ---
if 'enviado' not in st.session_state:
    st.session_state['enviado'] = False

contenedor_principal = st.empty()

if not st.session_state['enviado']:
    # --- PANTALLA DE PREGUNTA ---
    with contenedor_principal.container():
        # Inicia la tarjeta blanca
        st.markdown('<div class="card-container">', unsafe_allow_html=True)
        
        # Título y Pregunta
        st.markdown('<div class="card-title">AROMATEX</div>', unsafe_allow_html=True)
        st.markdown('<div class="card-question">¿Cómo fue tu experiencia con el aroma de esta sucursal?</div>', unsafe_allow_html=True)
        
        # Emojis clickeables
        clic = clickable_images(
            imagenes,
            titles=["Terrible", "Malo", "Regular", "Bueno", "Excelente"],
            div_style={"display": "flex", "justify-content": "space-between", "gap": "10px"},
            img_style={"width": "60px", "height": "60px", "cursor": "pointer", "transition": "transform 0.2s"},
            key="emojis"
        )
        
        # Etiquetas debajo
        st.markdown("""
            <div class="labels-container">
                <span>Terrible</span>
                <span>Excelente</span>
            </div>
        """, unsafe_allow_html=True)
        
        # Cierra la tarjeta blanca
        st.markdown('</div>', unsafe_allow_html=True)

        # Lógica al hacer clic
        if clic > -1:
            # Aquí iría tu lógica de guardado en Airtable
            # Por ahora, solo simulamos el envío
            st.session_state['enviado'] = True
            st.rerun()

else:
    # --- PANTALLA DE GRACIAS ---
    with contenedor_principal.container():
        st.markdown('<div class="card-container">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">AROMATEX</div>', unsafe_allow_html=True)
        # Icono de check gigante
        st.markdown('<div style="font-size: 80px; color: #4CAF50; margin: 20px 0;">✅</div>', unsafe_allow_html=True)
        st.markdown('<div class="card-question">¡Gracias por tu opinión!</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Esperar y reiniciar
        time.sleep(3)
        st.session_state['enviado'] = False
        st.rerun()
