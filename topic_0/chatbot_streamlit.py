# ==========================================
# 1. IMPORTACIONES (Cargamos las librerías necesarias)
# ==========================================
# FROM: Busca dentro de un paquete grande (langchain_google_genai) 
# IMPORT: Extrae sólo la clase exacta que necesitamos (ChatGoogleGenerativeAI)
from langchain_google_genai import ChatGoogleGenerativeAI

# ==========================================
# ALTERNATIVA OPENAI: (Descomentar si se usa OpenAI)
# from langchain_openai import ChatOpenAI
# ==========================================

# Extraemos las 3 etiquetas de mensajes que entiende el modelo:
# AIMessage (BOT), HumanMessage (USUARIO), SystemMessage (REGLAS INTERNAS)
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

# IMPORT: Cargamos toda la librería entera, y le damos el apodo 'st' para construir la interfaz gráfica
import streamlit as st

# ==========================================
# 2. CONFIGURACIÓN VISUAL (La interfaz gráfica)
# ==========================================
# st.set_page_config: Configuración de la interfaz del chatbot
st.set_page_config(page_title="ChatBot TiTi", page_icon="🤖")

# st.title / st.markdown: Dibuja los textos principales en la pantalla
st.title("ChatBot TiTi 🤖")
st.markdown("Este es un chatBot de TiTi, ¡Escribe tu mensaje abajo para poder ayudarte !")

# ==========================================
# 3. CONFIGURACIÓN DEL MODELO DE IA
# ==========================================
# Instanciamos el modelo de Gemini. 
# temperature=0.7 indica creatividad (0 = exacto, 1 = muy creativo)
# google_api_key indica la clave de API de Google, que la tienes que crear previamente en Google AI Studio

chat_model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.7,
    google_api_key="[GCP_API_KEY]"
)

# ==========================================
# ALTERNATIVA OPENAI: (Descomentar si se usa OpenAI en vez de Gemini)
# chat_model = ChatOpenAI(
#     model="gpt-4",  # o "gpt-3.5-turbo", "gpt-4o-mini"
#     temperature=0.7,
#     api_key="[TU_OPENAI_API_KEY_AQUI]"
# )
# ==========================================

# ==========================================
# 4. GESTIÓN DE LA MEMORIA (El Historial)
# ==========================================
# Streamlit borra todas las variables cada vez que pulsas un botón.
# 'st.session_state' es como un "disco duro temporal". Si la lista 'mensajes'
# la creamos en blanco al inicio
if "mensajes" not in st.session_state:
    st.session_state.mensajes = []

# ==========================================
# 5. DIBUJAR LOS MENSAJES ANTIGUOS
# ==========================================
# Recorremos la lista de mensajes que haya en memoria uno por uno para ver si existen mensajes previos.
for msg in st.session_state.mensajes:
    
    # Ignoramos (no mostramos en pantalla) si es un mensaje de configuración interna que es del tipo (SystemMessage)
    if isinstance(msg, SystemMessage): 
        continue
    
    # Asignamos el icono visual correcto ("assistant" para el Bot, "user" para ti) usamos AIMessage para mensajes de la IA
    role = "assistant" if isinstance(msg, AIMessage) else "user"
    
    # Construye la burbuja de chat e inyecta el texto dentro
    with st.chat_message(role):
        st.markdown(msg.content)

# ==========================================
# 6. ENVIAR MENSAJES (El cajón de texto)
# ==========================================
# Genera el cajón donde escribes en la parte inferior de la pantalla.
pregunta = st.chat_input("Escribe tu mensaje: ")

# Si el usuario escribió y pulsó Enter:
if pregunta:
   
    # 1. Dibuja INMEDIATAMENTE la burbuja con el mensaje del usuario
    with st.chat_message("user"):
       st.markdown(pregunta)
       
    # 2. Guarda ese texto del usuario en el historial de session_state
    st.session_state.mensajes.append(HumanMessage(content=pregunta))

    # 3. Le envía el historial ENTERO al modelo para que responda con contexto
    respuesta = chat_model.invoke(st.session_state.mensajes)

    # 4. Dibuja la burbuja con la respuesta producida por el modelo
    with st.chat_message("assistant"):
      st.markdown(respuesta.content)

    # 5. Guarda la respuesta del modelo en el historial de session_state
    st.session_state.mensajes.append(respuesta)