# Configuración Inicial (Setup)

Instrucciones y requisitos previos para configurar el entorno de desarrollo y ejecutar la aplicación del chatbot avanzado.

## 0. Tecnologías Utilizadas
Antes de empezar, este proyecto se construye sobre las siguientes bases tecnológicas:

*   **Python:** El *lenguaje de programación* que vertebra todo el código. Usamos Python por su inmenso ecosistema orientado a la Inteligencia Artificial.
*   **LangChain:** Es un *Framework* (marco de trabajo). Actúa como el "cerebro orquestador" que nos permite conectar nuestro código con modelos de IA, manejar la memoria del chat y definir cómo preguntarle al modelo usando un estándar aplicable a cualquier IA.
*   **LCEL (LangChain Expression Language):** Es la sintaxis oficial de LangChain para encadenar componentes mediante el operador `|` (pipe). Permite conectar la plantilla del prompt con el modelo de forma declarativa y con soporte nativo de streaming.
*   **Streamlit:** Es una *Librería / Micro-framework*. Se usa para construir la interfaz gráfica (UI) de la aplicación web directamente en código Python puro, sin necesidad de saber HTML, CSS o Javascript.
*   **langchain-google-genai:** Es una *Librería integradora*. Actúa como el "enchufe" específico que traduce el formato estándar de LangChain al formato propietario que entiende la API de Google (Gemini).

***

## 1. Instalación de Python
Python es el intérprete requerido para ejecutar los scripts del proyecto.

*   **Descarga:** [Página oficial de Python (python.org)](https://www.python.org/downloads/)
*   **Verificación:** Abre la terminal y ejecuta `python3 --version`. Se recomienda Python 3.10 o superior.

***

## 2. Entornos Virtuales (`virtual_env`)
Un entorno virtual es un directorio aislado que contiene su propia instalación de Python y un gestor de paquetes (`pip`).

*   **Propósito:** Aislar las dependencias del proyecto actual respecto al entorno global del sistema operativo u otros proyectos. Esto evita conflictos de versiones.
*   **Creación:** Ejecutar en el directorio raíz del proyecto:
    ```bash
    python3 -m venv virtual_env
    ```
*   **Activación:** Antes de instalar dependencias o ejecutar código, el entorno debe activarse:
    *   *macOS/Linux:* `source virtual_env/bin/activate`
    *   *Windows:* `.\virtual_env\Scripts\activate`

*(Al activarlo, la terminal mostrará el prefijo `(virtual_env)`).*

***

## 3. Instalación de Dependencias
Con el entorno virtual activado, instala los paquetes requeridos mediante `pip`:

*   **langchain:** Framework principal para orquestar la lógica del LLM.
*   **langchain-core:** Núcleo de LangChain. Incluye los tipos de mensajes (`AIMessage`, `HumanMessage`, `SystemMessage`) y `PromptTemplate`.
*   **langchain-google-genai:** Proveedor oficial de LangChain para conectar con la API de modelos Gemini de Google.
*   **langchain-openai:** Proveedor para conectar con la API de OpenAI (alternativa comentada en el código).
*   **streamlit:** Librería para el desarrollo ágil de interfaces gráficas directamente en Python.

**Comando de instalación:**
```bash
pip install langchain langchain-core langchain-google-genai langchain-openai streamlit
```

***

## 4. Configuración de la API Key de Google
Este chatbot usa Google Gemini como proveedor de IA. Necesitas una API Key gratuita.

1. Genera una clave en [Google AI Studio](https://aistudio.google.com/app/apikey).
2. Configura la variable de entorno en tu terminal **antes** de ejecutar la app:
    ```bash
    export GOOGLE_API_KEY="tu_clave_aqui"
    ```
3. Para que sea permanente (no tener que repetirlo cada vez), añádela a tu perfil de shell:
    ```bash
    echo 'export GOOGLE_API_KEY="tu_clave_aqui"' >> ~/.zshrc
    source ~/.zshrc
    ```

*   **Para usar OpenAI (Alternativa):**
    1. Genera una clave en [OpenAI Developer Platform](https://platform.openai.com/api-keys).
    2. En `chatbot_streamlit_avanzado.py`, descomenta el bloque etiquetado como `ALTERNATIVA OPENAI` y comenta el bloque de Google Gemini.

***

## 5. Modelos Gemini Disponibles
El chatbot permite seleccionar entre los siguientes modelos desde el panel lateral:

| Modelo | Características |
|---|---|
| `gemini-2.5-flash` | Rápido y equilibrado. Recomendado para uso general. |
| `gemini-2.5-pro` | Más potente y preciso. Ideal para tareas complejas. |
| `gemini-2.0-flash` | Versión anterior, ligera y eficiente. |

***

## 6. Ejecución de la Aplicación
Una vez configurado y con el entorno virtual activo, dirígete a la carpeta correspondiente y arranca el servidor web local:

```bash
cd topic_1
streamlit run chatbot_streamlit_avanzado.py
```

***

## 7. Interfaz Gráfica (Navegador)
Al ejecutar el comando anterior, pasará lo siguiente:

1. El terminal mostrará dos URLs: una `Network URL` y una `Local URL`.
2. Automáticamente se abrirá una nueva pestaña en tu navegador predeterminado (suele apuntar a **`http://localhost:8501`**).
3. Si la ventana no se abre sola, puedes copiar y pegar ese enlace en el navegador.

A partir de ahí, puedes interactuar con la interfaz del chatbot directamente desde la web.

### Funcionalidades del chatbot avanzado
*   **Panel lateral:** Ajusta la creatividad del modelo (temperatura) y selecciona la versión de Gemini.
*   **Historial de conversación:** El bot recuerda los mensajes anteriores dentro de la misma sesión.
*   **Streaming:** Las respuestas se muestran token a token en tiempo real.
*   **Botón "Empezar de cero":** Limpia el historial y reinicia la conversación.
