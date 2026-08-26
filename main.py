import os
import requests
from dotenv import load_dotenv
from google import genai

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

PROMPT_CURADORIA = """
Atue como um especialista em curadoria de produtos de impressão 3D para e-commerce (foco na Shopee).
Gere uma curadoria com 5 modelos 3D com alto potencial de venda.

Critérios:
1. Viabilidade técnica: peças de fácil impressão (print-in-place ou sem suportes complexos).
2. Custo-benefício: baixo a médio consumo de filamento.
3. Nichos: setup gamer, utilidades domésticas, organizadores, decoração minimalista ou fidgets.

IMPORTANTE SOBRE OS LINKS:
Não invente URLs com IDs numéricos fictícios. Em vez disso, monte links diretos de busca oficial com o nome do termo em inglês codificado para URL (ex: `+` ou `%20` no lugar dos espaços):
- MakerWorld: https://makerworld.com/en/search/models?keyword=TERMO_EM_INGLES
- Printables: https://www.printables.com/search/models?q=TERMO_EM_INGLES

Para cada modelo, formate exatamente assim:
📦 *[Nome do Modelo]*
🔗 [Buscar no MakerWorld](https://makerworld.com/en/search/models?keyword=TERMO) | [Buscar no Printables](https://www.printables.com/search/models?q=TERMO)
🎯 *Nicho:* [Nicho]
💡 *Por que vende:* [Resumo direto da dor/apelo]
⚙️ *Dica de Produção:* [Filamento, infill e cores recomendadas]
🛒 *Título Shopee SEO:* [Sugestão de título com palavras-chave de busca]

Separe cada produto com: -------------------
"""

def gerar_curadoria() -> str:
    client = genai.Client(api_key=GEMINI_API_KEY)
    chat = client.chats.create(model="gemini-3.6-flash")
    response = chat.send_message(PROMPT_CURADORIA)
    return response.text

def enviar_telegram(texto: str):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    limite = 4000
    partes = [texto[i:i+limite] for i in range(0, len(texto), limite)]
    
    for parte in partes:
        payload = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": parte,
            "parse_mode": "Markdown",
            "disable_web_page_preview": True
        }
        res = requests.post(url, json=payload)
        
        if res.status_code != 200:
            payload.pop("parse_mode")
            res = requests.post(url, json=payload)
            
        if res.status_code == 200:
            print("Mensagem enviada com sucesso no Telegram!")
        else:
            print(f"Erro ao enviar: {res.status_code} - {res.text}")

if __name__ == "__main__":
    if not all([GEMINI_API_KEY, TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID]):
        print("Erro: Verifique as variáveis no arquivo .env")
        exit(1)
        
    print("Gerando curadoria...")
    conteudo = gerar_curadoria()
    print("Enviando para o Telegram...")
    enviar_telegram(conteudo)