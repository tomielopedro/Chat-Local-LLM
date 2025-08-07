from typing import Optional, List
import requests
from langchain.llms.base import LLM


class CustomLLMLangChain(LLM):
    model: str
    base_url: str

    def __init__(self, model: str, base_url: str, **kwargs):
        super().__init__(model=model, base_url=base_url, **kwargs)

    def _call(self, prompt: str, stop: Optional[List[str]] = None, run_manager=None) -> str:
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False
        }
        try:
            response = requests.post(self.base_url, json=payload, timeout=60)
            response.raise_for_status()
            return response.json().get("response", "").strip()
        except requests.exceptions.ConnectionError:
            return "[Erro]: Não foi possível conectar ao servidor Ollama. Verifique se o Ollama está rodando em localhost:11434"
        except requests.exceptions.Timeout:
            return "[Erro]: Timeout na requisição. O modelo pode estar demorando para responder."
        except Exception as e:
            return f"[Erro na chamada ao modelo]: {str(e)}"

    @property
    def _llm_type(self) -> str:
        return "ollama"



