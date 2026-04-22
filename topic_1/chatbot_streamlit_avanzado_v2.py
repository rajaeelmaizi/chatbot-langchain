# ==========================================
# 1: IMPORTACIONES
# ==========================================
try:
    from langchain_google_genai import ChatGoogleGenerativeAI
except ImportError:
    ChatGoogleGenerativeAI = None

try:
    from langchain_openai import ChatOpenAI
except ImportError:
    ChatOpenAI = None

try:
    from langchain_anthropic import ChatAnthropic
except ImportError:
    ChatAnthropic = None

import os

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
import streamlit as st


# ==========================================
# 2: INTERFAZ
# ==========================================
st.set_page_config(page_title="ChatBot TiTi v2", page_icon="🚀")
st.title("ChatBot TiTi v2 🚀")
st.markdown("Versión con **ChatPromptTemplate** + **streaming** (el texto aparece letra a letra).")


# ==========================================
# 2.1: CONTROLES DEL SIDEBAR
# ==========================================
with st.sidebar:
    st.header("🤖 Modelo")

    catalogo = {
        "Google Gemini":    ["gemini-2.5-flash", "gemini-2.5-pro", "gemini-2.0-flash"],
        "OpenAI":           ["gpt-4o-mini", "gpt-4o", "gpt-4-turbo", "gpt-3.5-turbo"],
        "Anthropic Claude": ["claude-sonnet-4-20250514", "claude-3-5-sonnet-latest", "claude-3-5-haiku-latest"],
    }

    proveedor = st.selectbox("Proveedor", list(catalogo.keys()))
    nombre_modelo = st.selectbox("Modelo", catalogo[proveedor])

    env_var = {
        "Google Gemini":    "GOOGLE_API_KEY",
        "OpenAI":           "OPENAI_API_KEY",
        "Anthropic Claude": "ANTHROPIC_API_KEY",
    }[proveedor]

    api_key = os.environ.get(env_var) or st.text_input(
        f"{env_var} (no detectada en entorno)", type="password"
    )

    temperatura = st.slider("🎨 Creatividad (temperatura)", 0.0, 1.0, 0.7, 0.1)

    st.divider()
    st.header("🎛️ Ajustes del prompt")

    estilo = st.selectbox(
        "Estilo de respuesta",
        ["sarcástico", "formal y serio", "infantil"]
    )

    longitud = st.selectbox(
        "Longitud de la respuesta",
        ["muy corta (1-2 frases)", "media (un párrafo)", "larga y detallada"]
    )

    idioma = st.selectbox(
        "Idioma",
        ["español", "inglés", "francés", "catalán"]
    )


# ==========================================
# 2.2: INSTANCIAMOS EL MODELO ELEGIDO
# ==========================================
def construir_modelo(proveedor: str, modelo: str, key: str, temp: float):
    if proveedor == "Google Gemini":
        if ChatGoogleGenerativeAI is None:
            st.error("Falta el paquete: pip install langchain-google-genai")
            st.stop()
        return ChatGoogleGenerativeAI(model=modelo, temperature=temp, google_api_key=key)

    if proveedor == "OpenAI":
        if ChatOpenAI is None:
            st.error("Falta el paquete: pip install langchain-openai")
            st.stop()
        return ChatOpenAI(model=modelo, temperature=temp, api_key=key)

    if proveedor == "Anthropic Claude":
        if ChatAnthropic is None:
            st.error("Falta el paquete: pip install langchain-anthropic")
            st.stop()
        return ChatAnthropic(model=modelo, temperature=temp, api_key=key)

    raise ValueError(f"Proveedor desconocido: {proveedor}")


if not api_key:
    st.warning(f"Introduce una {env_var} en el sidebar para empezar a chatear.")
    st.stop()

chat_model = construir_modelo(proveedor, nombre_modelo, api_key, temperatura)


# ==========================================
# 4: PLANTILLA DE PROMPT (ChatPromptTemplate)
# ==========================================

plantilla_prompt = ChatPromptTemplate.from_messages([
    ("system",
     "Eres TiTi, un asistente conversacional.\n"
     "REGLAS ESTRICTAS (obligatorias, no las rompas):\n"
     "- Responde SIEMPRE en {idioma}.\n"
     "- Usa un tono {estilo} en toda la respuesta.\n"
     "- La respuesta debe ser {longitud}. No te pases.\n"
     "- No uses emojis salvo que el usuario te los pida.\n"
     "- Si la pregunta es ambigua, pide una aclaración breve en vez de inventar."),
    MessagesPlaceholder("historial"),
    ("human", "{pregunta_usuario}")
])


# ==========================================
# 5: CADENA LCEL (el operador | conecta componentes)
# ==========================================

cadena = plantilla_prompt | chat_model


# ==========================================
# 6: MEMORIA
# ==========================================
if "mensajes" not in st.session_state:
    st.session_state.mensajes = []


# ==========================================
# 7: DIBUJAR MENSAJES PREVIOS
# ==========================================
for msg in st.session_state.mensajes:

    if isinstance(msg, SystemMessage):
        continue

    role = "assistant" if isinstance(msg, AIMessage) else "user"

    with st.chat_message(role):
        st.markdown(msg.content)


# ==========================================
# 8: INPUT DEL USUARIO + STREAMING
# ==========================================
pregunta = st.chat_input("Escribe tu mensaje: ")

if pregunta:

    # Pintamos la burbuja del usuario al instante
    with st.chat_message("user"):
        st.markdown(pregunta)

    # Guardamos la pregunta en el historial
    st.session_state.mensajes.append(HumanMessage(content=pregunta))

    # Preparamos la burbuja del asistente y la iremos rellenando con cada fragmento
    with st.chat_message("assistant"):

        contenedor = st.empty()        # hueco vacío donde iremos repintando
        respuesta_completa = ""        # acumulador del texto que ya ha llegado

        for fragmento in cadena.stream({
            "pregunta_usuario": pregunta,
            "historial": st.session_state.mensajes,
            "estilo": estilo,
            "longitud": longitud,
            "idioma": idioma
        }):
            respuesta_completa += fragmento.content
            # El cursor "▌" indica visualmente que sigue escribiendo
            contenedor.markdown(respuesta_completa + "▌")

        # Cuando acaba el stream, quitamos el cursor
        contenedor.markdown(respuesta_completa)

    # Guardamos la respuesta completa en el historial
    st.session_state.mensajes.append(AIMessage(content=respuesta_completa))
