# Chatbot com LangChain + Ollama v2.0

Este é um aplicativo Streamlit que implementa um chatbot usando LangChain e Ollama para interação com modelos de linguagem locais.

## 🚀 Funcionalidades

- Interface de chat intuitiva e responsiva
- Integração com Ollama para modelos locais
- Histórico de conversas persistente durante a sessão
- Configurações personalizáveis do modelo
- Status de conexão em tempo real
- Estatísticas da conversa




### 🎯 Prompt Personalizado
- **Opção de prompt padrão**: Alterne entre prompt personalizado e o padrão do LangChain

## 📋 Pré-requisitos

1. **Python 3.8+** instalado
2. **Ollama** instalado e rodando localmente
3. **Modelo DeepSeek R1 7B** (ou outro modelo de sua escolha) baixado no Ollama

### Instalação do Ollama

```bash
# No Linux/macOS
curl -fsSL https://ollama.ai/install.sh | sh

# No Windows, baixe o instalador do site oficial
```

### Download do modelo

```bash
ollama pull deepseek-r1:7b
```

## 🛠️ Instalação

1. Clone ou baixe os arquivos do projeto
2. Instale as dependências:

```bash
pip install -r requirements.txt
```

## 🎯 Como usar

1. **Inicie o Ollama** (se não estiver rodando):
```bash
ollama serve
```

2. **Execute o aplicativo Streamlit**:
```bash
streamlit run streamlit_chatbot.py
```

3. **Acesse o aplicativo** no navegador (geralmente `http://localhost:8501`)

5. **Comece a conversar** digitando mensagens no campo de entrada (agora posicionado abaixo das mensagens)

## ⚙️ Configurações

### Sidebar

#### 🔧 .env
    LLM_PROPMPT=Você é um assistente útil e amigável. Responda de forma clara e concisa.
    OLLAMA_URL=http://localhost:11434
    BASE_URL=http://localhost:11434/api/generate


#### 🎯 Opções
- **Usar prompt padrão do LangChain**: Checkbox para alternar entre prompt personalizado e padrão
- **AI Think**: Checkbox para mostrar o pensamento da AI até a resposta.

#### 🗑️ Controles
- **Limpar Histórico**: Remove todas as mensagens da conversa atual

### Status Avançado

#### 📊 Informações em Tempo Real
- **Contador de Mensagens**: Total de mensagens na conversa
- **Modelo Atual**: Exibe o modelo em uso

#### 📈 Estatísticas Detalhadas
- **Mensagens do Usuário**: Contador específico
- **Respostas da IA**: Contador específico
- **Informações do Modelo**: Detalhes técnicos

## 🔧 Estrutura do Código

### `CustomLLMLangChain`

Classe personalizada que herda de `LLM` do LangChain:

- **Campos**: `model` (nome do modelo) e `base_url` (URL do Ollama)
- **Método `_call`**: Faz requisições HTTP para o Ollama
- **Tratamento de Erros**: Captura erros de conexão, timeout e outros
- **Compatibilidade Pydantic**: Inicialização correta para validação


### `chat_bot`
Lógica e regras do chat com a llm
- **Configurações Dinâmicas**: Sidebar com opções personalizáveis
- **Interface de Chat**: Layout otimizado com `st.chat_message` e `st.chat_input`
- **Gerenciamento de Estado**: Usando `st.session_state` para persistência
- **Monitoramento**: Status de conexão e métricas detalhadas



## 📝 Personalização

### Exemplos de Prompts Personalizados

#### Assistente Técnico
```
Você é um especialista em programação e tecnologia. Responda de forma técnica e precisa, fornecendo exemplos de código quando apropriado.
```

#### Assistente Criativo
```
Você é um assistente criativo e inspirador. Use linguagem poética e imaginativa, sempre buscando soluções inovadoras e fora da caixa.
```

#### Assistente Formal
```
Você é um assistente profissional e formal. Use linguagem corporativa, seja conciso e objetivo em suas respostas.
```

### Adicionando Novos Modelos

1. Baixe o modelo no Ollama:
```bash
ollama pull nome-do-modelo
```

2. Altere o campo "Nome do Modelo" na sidebar

### Modificando a Interface

- **Cores e Tema**: Edite o CSS no final do arquivo
- **Layout**: Ajuste as colunas e containers
- **Funcionalidades**: Adicione novos widgets na sidebar

### Configurações Avançadas

- **Memory**: Modifique o tipo de memória do LangChain
- **Prompts**: Use templates mais complexos com variáveis
- **Streaming**: Implemente respostas em tempo real

## 🔄 Changelog

### v2.0
- ✅ Chat input movido para baixo das mensagens
- ✅ Indicador visual do prompt ativo
- ✅ Estatísticas detalhadas da conversa
- ✅ Layout otimizado e mais intuitivo
- ✅ Mensagem de boas-vindas personalizada

### v1.0
- ✅ Interface básica de chat
- ✅ Integração com Ollama
- ✅ Configurações de modelo
- ✅ Status de conexão
- ✅ Histórico de conversas

## 🤝 Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para:

- Reportar bugs
- Sugerir melhorias
- Enviar pull requests
- Compartilhar feedback

---



