import streamlit as st
import os
from dotenv import load_dotenv
from CustomLLMLangChain import CustomLLMLangChain
from utils.ollama_api import test_ollama_connection, listar_modelos_ollama


# ─── Carregamento das variáveis de ambiente ─────────────────────────────
load_dotenv()
BASE_URL = os.getenv('BASE_URL')
OLLAMA_URL = os.getenv('OLLAMA_URL')
LLM_PROMPT = os.getenv('LLM_PROMPT')

# ─── Teste de conexão com Ollama ────────────────────────────────────────
ollama_connected = test_ollama_connection(OLLAMA_URL)

# ─── Interface ──────────────────────────────────────────────────────────
if ollama_connected:
    st.set_page_config(page_title="Chatbot com LangChain + Ollama", page_icon="🤖", layout="wide")

    # Inicializa estados de sessão
    st.session_state.ollama_models = st.session_state.get('ollama_models', listar_modelos_ollama())
    st.session_state.llm_prompt = st.session_state.get('llm_prompt', LLM_PROMPT)
    st.session_state.selected_model = st.session_state.get('selected_model', None)

    # ─── Sidebar ────────────────────────────────────────────────────────
    with st.sidebar:
        st.header("⚙️ Configurações")

        selected_model_name = st.selectbox("Selecione um modelo", st.session_state.ollama_models)

        # Apenas recria o modelo se mudou
        if (
            st.session_state.selected_model is None or
            st.session_state.selected_model.model != selected_model_name
        ):
            st.session_state.selected_model = CustomLLMLangChain(
                model=selected_model_name,
                base_url=BASE_URL
            )
    # === NAVEGAÇÃO ===
    pages = {
        "Pages": [
            st.Page("pages/chat_bot.py", title="💬️ Chat"),

        ]
    }

    pg = st.navigation(pages)
    pg.run()

else:
    st.error("❌ Ollama não conectado. Verifique se o servidor está ativo.")
