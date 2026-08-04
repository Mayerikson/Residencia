import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

def main():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Erro: OPENAI_API_KEY não encontrada. Configure o arquivo .env.")
        return

    client = OpenAI(api_key=api_key)
    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    print("\n--- Teste de Interação com LLM ---")
    print(f"Modelo utilizado: {model}")

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "Você é um assistente prestativo e conciso."},
                {"role": "user", "content": "Olá, qual é a capital da França?"}
            ],
            temperature=0.7,
            max_tokens=50
        )
        print("\nResposta do LLM:")
        print(response.choices[0].message.content)
    except Exception as e:
        print(f"Ocorreu um erro ao chamar a API da OpenAI: {e}")

if __name__ == "__main__":
    main()
