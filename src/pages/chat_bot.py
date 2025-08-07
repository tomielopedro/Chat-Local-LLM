import os
import re
import streamlit as st
from dotenv import load_dotenv
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from RAG import ChatPDF

# ─── CONFIGURAÇÕES INICIAIS ────────────────────────────────────────────────
load_dotenv()
BASE_URL = os.getenv('BASE_URL')
OLLAMA_URL = os.getenv('OLLAMA_URL')
LLM_MODEL = os.getenv('LLM_MODEL')
LLM_PROMPT = os.getenv('LLM_PROMPT')


# ─── FUNÇÕES AUXILIARES ────────────────────────────────────────────────────
def iniciar_chain():
    llm = st.session_state.selected_model
    custom_prompt = st.session_state.llm_prompt
    memory = ConversationBufferMemory()

    if custom_prompt and custom_prompt.strip():
        prompt_template = PromptTemplate(
            input_variables=["history", "input"],
            template=f"{custom_prompt}\n\nHistórico da conversa:\n{{history}}\n\nHumano: {{input}}\nAssistente:"
        )
        chain = ConversationChain(llm=llm, memory=memory, prompt=prompt_template)
    else:
        chain = ConversationChain(llm=llm, memory=memory)
    return chain


def get_chain():
    if st.session_state.chain is None:
        try:
            st.session_state.chain = iniciar_chain()
        except Exception as e:
            st.error(f"Erro ao inicializar a chain: {str(e)}")
            return None
    return st.session_state.chain

def get_rag():
    if "rag" not in st.session_state:
        try:
            st.session_state.rag = ChatPDF(llm_model=st.session_state.selected_model.model)
        except Exception as e:
            st.error(f"Erro ao inicializar o RAG: {str(e)}")
            return None
    return st.session_state.rag

# ─── CONFIGURAÇÃO DA INTERFACE ─────────────────────────────────────────────

st.title("🤖 Chatbot com LangChain + Ollama Local")
st.markdown("---")

# ─── INICIALIZAÇÃO DE ESTADO ──────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []

if "chain" not in st.session_state:
    st.session_state.chain = None

# ───SIDEBAR ───────────────────────────────────────────────────────────────
with st.sidebar:
    chat_model = st.selectbox('Selecione o tipo de chat', ['Chat Padrão', 'RAG Chat'])
    use_default_prompt = st.checkbox("Usar prompt padrão do LangChain", value=False)
    show_think = st.checkbox("AI Think", value=False)

    if chat_model == 'RAG Chat':
        st.markdown("### 📄 Carregar Documento PDF")
        uploaded_file = st.file_uploader("Escolha um arquivo PDF", type="pdf")

        if uploaded_file:
            with st.spinner("Processando o PDF..."):
                try:
                    temp_path = f"temp_{uploaded_file.name}"
                    with open(temp_path, "wb") as f:
                        f.write(uploaded_file.getvalue())

                    rag = get_rag()
                    rag.ingest(temp_path)
                    st.success("Documento carregado e processado com sucesso!")
                    os.remove(temp_path)
                except Exception as e:
                    st.error(f"Erro ao processar o PDF: {str(e)}")

    st.divider()
    if st.button("🗑️ Limpar Histórico"):
        st.session_state.messages = []
        st.session_state.chain = None
        st.rerun()


# ─── INTERFACE PRINCIPAL ───────────────────────────────────────────────────
col1, col2 = st.columns([3, 1])

# Conversa
with col1:
    st.subheader("💬 Conversa")
    messages_container = st.container(height=400)

    with messages_container:
        if st.session_state.messages:
            for message in st.session_state.messages:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])
        else:
            with st.chat_message("assistant"):
                st.markdown("Olá! Sou seu assistente de IA. Como posso ajudá-lo hoje?")

    st.markdown("---")

    # Campo de input
    if prompt := st.chat_input("Digite sua mensagem aqui..."):
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Obter a chain ou o RAG dependendo da escolha do usuário
        chain = None
        rag = None

        if chat_model == 'Chat Padrão':
            chain = get_chain()
        elif chat_model == 'RAG Chat':
            rag = get_rag()

        # Executar a resposta com base na escolha
        if chat_model == 'Chat Padrão' and chain:
            try:
                with st.spinner("🤔 Pensando..."):
                    response = chain.run(prompt)
                    if not show_think:
                        match = re.search(r"<think>(.*?)</think>", response, re.DOTALL)
                        response = match.group(1).strip() if match else response
                st.session_state.messages.append({"role": "assistant", "content": response})
                st.rerun()
            except Exception as e:
                error_msg = f"Erro ao obter resposta do Chat Padrão: {str(e)}"
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})
                st.rerun()

        elif chat_model == 'RAG Chat' and rag:
            try:
                with st.spinner("🔍 Buscando resposta no documento..."):
                    response = rag.ask(prompt)
                st.session_state.messages.append({"role": "assistant", "content": response})
                st.rerun()
            except Exception as e:
                error_msg = f"Erro ao responder com RAG: {str(e)}"
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})
                st.rerun()
        else:
            st.error("Não foi possível inicializar o modelo selecionado.")
            st.session_state.messages.append({
                "role": "assistant",
                "content": "Erro ao conectar ao modelo."
            })
            st.rerun()

# Coluna lateral de status
with col2:
    st.subheader("📊 Status")

    st.markdown("---")
    st.metric("Mensagens", len(st.session_state.messages))

    st.markdown("---")
    st.markdown("### 🔧 Modelo em Uso")
    st.code(f"Modelo: {st.session_state.selected_model.model}")

    if st.session_state.messages:
        user_msgs = len([m for m in st.session_state.messages if m["role"] == "user"])
        assistant_msgs = len([m for m in st.session_state.messages if m["role"] == "assistant"])

        st.markdown("---")
        st.markdown("### 📈 Estatísticas")
        st.metric("Mensagens do Usuário", user_msgs)
        st.metric("Respostas da IA", assistant_msgs)

# ─── FOOTER ────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center'>
        <p>Desenvolvido por Pedro Tomielo usando Streamlit + LangChain + Ollama</p>
        <p><small>v2.0 - Com prompt personalizado e layout otimizado</small></p>
    </div>
    """,
    unsafe_allow_html=True
)
