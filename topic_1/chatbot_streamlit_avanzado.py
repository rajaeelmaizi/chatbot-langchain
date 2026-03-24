# ==========================================
# 1. IMPORTACIONES (Cargamos las librerías necesarias)
# ==========================================
# IMPORT: Cargamos toda la librería entera, y le damos el apodo 'st' para construir la interfaz gráfica
import streamlit as st

# ALTERNATIVA OPENAI: (Descomentar si se usa OpenAI en vez de Gemini)
# from langchain_openai import ChatOpenAI

# FROM: Busca dentro del paquete (langchain_google_genai)
# IMPORT: Extrae sólo la clase exacta que necesitamos (ChatGoogleGenerativeAI)
from langchain_google_genai import ChatGoogleGenerativeAI

# Extraemos las 3 etiquetas de mensajes que entiende el modelo:
# AIMessage (BOT), HumanMessage (USUARIO), SystemMessage (REGLAS INTERNAS)
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

# PromptTemplate: Permite definir una plantilla de texto con variables que se rellenan dinámicamente
from langchain_core.prompts import PromptTemplate

# ==========================================
# 2. CONFIGURACIÓN VISUAL (La interfaz gráfica)
# ==========================================
# st.set_page_config: Configuración de la interfaz del chatbot
st.set_page_config(page_title="GeminiBot 9000", page_icon="🧠")

# st.title / st.markdown: Dibuja los textos principales en la pantalla
st.title("🧠 GeminiBot 9000")
st.markdown("El chatbot más chulo del barrio, alimentado con **Google Gemini + LangChain**. ¡Pregúntame lo que quieras, que para eso estoy! 😎")

# ==========================================
# 3. CONFIGURACIÓN DEL MODELO DE IA (Panel lateral)
# ==========================================
# st.sidebar: Agrupa los controles de configuración en un panel lateral
# Esto permite al usuario ajustar el modelo sin recargar la página
with st.sidebar:
    st.header("🎛️ Centro de mando")

    # st.slider: Control deslizante para ajustar la creatividad del modelo
    # nivel_creatividad=0 → respuestas exactas y repetibles
    # nivel_creatividad=1 → respuestas más creativas e impredecibles
    nivel_creatividad = st.slider("🎨 Creatividad (temperatura)", 0.0, 1.0, 0.5, 0.1)

    # ==========================================
    # ALTERNATIVA OPENAI: (Descomentar si se usa OpenAI en vez de Gemini)
    # nombre_modelo = st.selectbox("Modelo", ["gpt-3.5-turbo", "gpt-4", "gpt-4o-mini"])
    # modelo_chat = ChatOpenAI(model=nombre_modelo, temperature=nivel_creatividad)
    # ==========================================

    # st.selectbox: Lista desplegable para elegir qué versión de Gemini usar
    # flash = más rápido y ligero, pro = más potente y preciso
    nombre_modelo = st.selectbox("🤖 Elige tu Gemini", ["gemini-2.5-flash", "gemini-2.5-pro", "gemini-2.0-flash"])

    # Instanciamos el modelo de Gemini con el modelo y la creatividad seleccionados
    # La GOOGLE_API_KEY se lee automáticamente de la variable de entorno
    modelo_chat = ChatGoogleGenerativeAI(model=nombre_modelo, temperature=nivel_creatividad)

# ==========================================
# 4. GESTIÓN DE LA MEMORIA (El Historial)
# ==========================================
# Streamlit borra todas las variables cada vez que pulsas un botón.
# 'st.session_state' es como un "disco duro temporal": guarda el historial
# entre interacciones para que el modelo mantenga el contexto de la conversación
if "historial_mensajes" not in st.session_state:
    st.session_state.historial_mensajes = []

# ==========================================
# 5. PLANTILLA DE PROMPT (Instrucciones al modelo)
# ==========================================
# PromptTemplate es una clase de LangChain que separa el TEXTO FIJO del texto VARIABLE.
#
# Sin PromptTemplate, tendrías que construir el string manualmente cada vez:
#   prompt = "Eres un bot. Historial: " + str(historial) + " Pregunta: " + pregunta
#
# Con PromptTemplate declaras el esqueleto una sola vez:
#   - input_variables: lista de los nombres de las variables que usará la plantilla
#   - template: el texto completo con marcadores {variable} donde irán los valores reales
#
# En cada llamada, LangChain sustituye automáticamente:
#   {historial_conversacion} → la lista de mensajes anteriores de session_state
#   {pregunta_usuario}       → el texto que acaba de escribir el usuario
#
# El resultado es el prompt final (texto completo) que se envía al modelo.
plantilla_prompt = PromptTemplate(
    input_variables=["pregunta_usuario", "historial_conversacion"],
    template="""Eres GeminiBot 9000, el asistente más inteligente y con más personalidad del universo conocido.
Eres útil, directo y tienes un toque de humor cuando la situación lo permite.

Historial de conversación:
{historial_conversacion}

Responde de manera clara y concisa a la siguiente pregunta: {pregunta_usuario}"""
)

# ==========================================
# 6. CADENA LCEL (LangChain Expression Language)
# ==========================================
# LCEL es la sintaxis oficial de LangChain para encadenar componentes.
# En lugar de llamar a cada paso manualmente, el operador | (pipe) los conecta
# en secuencia: la salida de uno se convierte automáticamente en la entrada del siguiente.
# Aquí: plantilla_prompt recibe los datos del usuario, genera el texto del prompt,
# y ese texto pasa directamente a modelo_chat para obtener la respuesta.
cadena_conversacion = plantilla_prompt | modelo_chat

# ==========================================
# 7. DIBUJAR LOS MENSAJES ANTIGUOS
# ==========================================
# Recorremos la lista de mensajes en memoria uno por uno para mostrar el historial previo
for mensaje in st.session_state.historial_mensajes:

    # Ignoramos (no mostramos en pantalla) los mensajes de configuración interna (SystemMessage)
    if isinstance(mensaje, SystemMessage):
        continue

    # Asignamos el icono visual correcto ("assistant" para el Bot, "user" para ti)
    rol = "assistant" if isinstance(mensaje, AIMessage) else "user"

    # Construye la burbuja de chat e inyecta el texto dentro
    with st.chat_message(rol):
        st.markdown(mensaje.content)

# ==========================================
# 8. BOTÓN PARA LIMPIAR LA CONVERSACIÓN
# ==========================================
# Vacía el historial y recarga la página para empezar desde cero
if st.button("🗑️ Empezar de cero"):
    st.session_state.historial_mensajes = []
    st.rerun()

# ==========================================
# 9. ENVIAR MENSAJES (El cajón de texto)
# ==========================================
# Genera el cajón donde el usuario escribe en la parte inferior de la pantalla
pregunta_usuario = st.chat_input("Dispara tu pregunta... 🎯")

# Si el usuario escribió y pulsó Enter:
if pregunta_usuario:

    # 1. Dibuja INMEDIATAMENTE la burbuja con el mensaje del usuario
    with st.chat_message("user"):
        st.markdown(pregunta_usuario)

    # 2. Genera y muestra la respuesta del asistente
    try:
        with st.chat_message("assistant"):

            # -------------------------------------------------------
            # OPCIÓN A — .invoke() (sin streaming)
            # El modelo genera TODA la respuesta internamente y solo
            # la devuelve cuando ha terminado. El usuario ve la pantalla
            # en blanco durante segundos y el texto aparece de golpe.
            # -------------------------------------------------------
            #respuesta = cadena_conversacion.invoke({
            #    "pregunta_usuario": pregunta_usuario,
            #    "historial_conversacion": st.session_state.historial_mensajes
            #})
            #respuesta_completa = respuesta.content
            #st.markdown(respuesta_completa)

            # -------------------------------------------------------
            # OPCIÓN B — .stream() (con streaming) — COMENTADO
            # El modelo devuelve la respuesta en fragmentos (tokens)
            # según los va generando. Cada iteración del bucle recibe
            # un fragmento pequeño que se acumula y muestra en pantalla
            # de forma progresiva, como si el bot estuviera escribiendo.
            #
            # El dict rellena las variables del PromptTemplate:
            #   "pregunta_usuario"       → texto escrito por el usuario
            #   "historial_conversacion" → mensajes anteriores de session_state
            # -------------------------------------------------------
            contenedor_respuesta = st.empty()
            respuesta_completa = ""
            for fragmento in cadena_conversacion.stream({
                "pregunta_usuario": pregunta_usuario,
                "historial_conversacion": st.session_state.historial_mensajes
            }):
                respuesta_completa += fragmento.content
                # El cursor "▌" indica visualmente que el modelo sigue escribiendo
                contenedor_respuesta.markdown(respuesta_completa + "▌")
            contenedor_respuesta.markdown(respuesta_completa)

        # 5. Guarda ambos mensajes en el historial de session_state
        st.session_state.historial_mensajes.append(HumanMessage(content=pregunta_usuario))
        st.session_state.historial_mensajes.append(AIMessage(content=respuesta_completa))

    except Exception as error:
        st.error(f"💥 Error al generar la respuesta: {str(error)}")
        st.info("Asegúrate de que la variable de entorno GOOGLE_API_KEY esté configurada correctamente.")
