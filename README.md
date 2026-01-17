# 🕸️ Deep Harvester - Universal PDF Scraper

> Ferramenta de automação desktop para extração massiva e arquivamento de documentos (PDFs) em sites complexos.

![Python](https://img.shields.io/badge/Python-3.11-blue.svg)
![Web Scraping](https://img.shields.io/badge/Focus-Data_Mining-orange.svg)

## 📖 O que é?

O **Deep Harvester** é um "Crawler de Bolso" projetado para pesquisadores, arquivistas de dados e estudantes que precisam baixar grandes volumes de documentos de sites que dificultam a automação.

Diferente de scripts simples que só funcionam em links diretos, esta ferramenta consegue navegar, fazer login (manter sessão), resolver captchas manualmente e explorar páginas internas ("Deep Scan") para encontrar o botão de download real.

### 🎯 Casos de Uso

* **📚 Acadêmico:** Baixar teses e dissertações de repositórios universitários que exigem múltiplos cliques.
* **🏛️ Transparência:** Coletar Diários Oficiais e Editais de prefeituras/governos.
* **📈 Financeiro:** Baixar relatórios anuais e balanços em sites de Relações com Investidores (RI).
* **💾 Data Hoarding:** Arquivar manuais, revistas antigas ou documentos técnicos de sites legados.

## ✨ Funcionalidades

* **🛡️ Stealth Mode:** Usa `undetected-chromedriver` para navegar como um humano, evitando bloqueios de WAF.
* **🧠 Sessão Persistente:** Salva seu login. Você loga uma vez no site (ex: Portal Capes, Jusbrasil, LinkedIn) e o robô lembra nas próximas vezes.
* **⚓ Deep Scan:** O robô não olha apenas a página atual; ele entra nos links da lista para buscar o arquivo na página de detalhes.
* **🚫 Anti-Paywall Básico:** Detecta se o site redirecionou para uma página de vendas/bloqueio e ignora o arquivo, focando apenas no conteúdo acessível.
* **🖥️ GUI Moderna:** Interface gráfica completa, sem necessidade de tocar no terminal.

## 🛠️ Tecnologias

* **Python 3.x**
* **Undetected-Chromedriver**
* **CustomTkinter** (UI)
* **Threading**

## 🚀 Como Usar

1.  **Instalação:**
    Clone o repositório ou baixe o ZIP.
    Execute o arquivo `INICIAR_INVESTIGACAO.bat` (Windows). Ele configura tudo sozinho.

2.  **Na Interface:**
    * **URL Alvo:** Cole o link da página que contém a lista de arquivos.
    * **Modo Profundo:** Marque se os PDFs não estiverem visíveis na primeira página (se precisar clicar no item para ver o download).
    * **Iniciar:** O navegador abrirá. Faça login se o site exigir.
    * **Confirmar:** Clique em "JÁ ESTOU LOGADO" e deixe o robô trabalhar.

## ⚠️ Aviso

Ferramenta desenvolvida para automação de tarefas repetitivas em dados públicos ou aos quais o usuário possui acesso legítimo.

---
**Desenvolvido por [Seu Nome]**