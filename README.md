# 🖨️ 3D Print AI Curator Bot

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![Google Gemini](https://img.shields.io/badge/AI-Google%20Gemini%20API-4285F4?style=flat&logo=google)](https://ai.google.dev/)
[![Telegram Bot API](https://img.shields.io/badge/Telegram-Bot%20API-2CA5E0?style=flat&logo=telegram&logoColor=white)](https://core.telegram.org/bots/api)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Sistema de automação e curadoria autônoma com Inteligência Artificial Generativa para prospecção de produtos 3D de alta liquidez para e-commerce (Shopee e Mercado Livre), com despacho diário via Telegram.

---

## 🎯 Problema de Negócio & Solução

* **O Problema:** A prospecção manual em repositórios 3D (MakerWorld e Printables) consome horas diárias e frequentemente esbarra em modelos complexos, caros de produzir ou sem apelo comercial validado.
* **A Solução:** Uma esteira autônoma que combina **Engenharia de Prompt estruturada** com o modelo `gemini-3.6-flash`, avaliando viabilidade técnica (print-in-place, sem suportes), estimativa de consumo de insumos e potencial de SEO para marketplace, entregando insights acionáveis todas as manhãs.

---

## 🏗️ Arquitetura e Engenharia

```text
[ Agendador de Tarefas / Cron ]
             │
             ▼ (Execução Silenciosa)
      [ main.py ]
             │
      ┌──────┴──────────────────────────┐
      ▼                                 ▼
[ Google GenAI SDK ]           [ Python-Dotenv ]
(LLM & Prompt Chaining)        (Gestão Segura de Credenciais)
      │                                 │
      └──────┬──────────────────────────┘
             ▼
[ Telegram Bot API (Requests) ]
(Payload Parsing & Fallback Handler)
             │
             ▼
[ Notificação no Mobile ]
```

### Principais Decisões Técnicas:
1. **Resiliência a Alucinações de Links:** Em vez de confiar em URLs com IDs numéricos fictícios gerados pela LLM, o sistema injeta URLs canônicas codificadas de busca (`Search Query URLs`), eliminando erros HTTP 404.
2. **Fallback de Formatação:** Mecanismo automático de retentativa em texto puro caso ocorram falhas de escape nos caracteres especiais da sintaxe Markdown da API do Telegram.
3. **Execução Headless & Não-Intrusiva:** Wrapper VBScript acoplado ao agendador do SO para garantir execução assíncrona em background sem intervenção do usuário ou abertura de janelas de terminal.

---

## 🚀 Como Executar Localmente

### 1. Clonar e preparar o ambiente
```bash
git clone [https://github.com/victorhugofcaetano/curadoria-3d-bot.git](https://github.com/victorhugofcaetano/curadoria-3d-bot.git)
cd curadoria-3d-bot
python -m venv venv

# Windows
.\venv\Scripts\Activate.ps1

# Linux / macOS
source venv/bin/activate

pip install -r requirements.txt
