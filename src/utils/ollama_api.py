import requests


def listar_modelos_ollama():
    try:
        response = requests.get("http://localhost:11434/api/tags")
        response.raise_for_status()
        data = response.json()
        modelos = [model["name"] for model in data.get("models", [])]
        return modelos
    except Exception as e:
        print("Erro ao listar modelos:", e)
        return []


def test_ollama_connection(url):
    try:
        test_response = requests.get(url, timeout=5)
        return test_response.status_code == 200
    except:
        return False
