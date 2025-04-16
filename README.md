# 🏀 NBA Bot API

API REST que fornece informações sobre jogos da NBA para uma data específica, incluindo horários, canais de transmissão e placares (quando disponíveis). Desenvolvida com FastAPI e Selenium, esta API é parte de um sistema maior que automatiza a coleta e distribuição desses dados.

## 📌 Funcionalidades

- **Endpoint `/scrape/{data}`**: Retorna uma lista em JSON dos jogos da NBA para a data fornecida.
- **Informações fornecidas**:
  - Horário do jogo
  - Canais de transmissão
  - Placar final (se o jogo já ocorreu)

## ⚙️ Tecnologias Utilizadas

- [FastAPI](https://fastapi.tiangolo.com/)
- [Selenium](https://www.selenium.dev/)
- [Docker](https://www.docker.com/)