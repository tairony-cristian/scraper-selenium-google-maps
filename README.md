# Google Maps Scraper Adaptado com Selenium

Este repositório contém dois scripts adaptados para realizar raspagem de dados no Google Maps utilizando Selenium. Os scripts permitem coletar informações de empresas com base em um segmento e cidade informados pelo usuário. O primeiro script salva os resultados em um arquivo Excel (.xlsx), enquanto o segundo permite a execução através de uma API, retornando os dados em formato JSON.

## Objetivo

Realizar a coleta automatizada de dados de empresas no Google Maps, com base no segmento (por exemplo, "restaurantes", "hotéis") e na cidade informada, e fornecer os resultados de forma organizada em um arquivo ou como resposta via API.

## Scripts

## 1. Coleta de dados com salvamento em Excel
Este script permite ao usuário informar o segmento e a cidade, e realiza a busca no Google Maps. Ele coleta informações como nome da empresa, número de telefone, link do Google Maps, site, avaliação (estrelas) e quantidade de avaliações. Os dados são salvos em Excel (.xlsx) e em Json.

**Execução**
O usuário deve inserir o segmento e a cidade quando solicitado.
Os resultados serão salvos em um arquivo chamado results.xlsx.

**Exemplo de uso**
1.Execute o script no seu ambiente Python.
2.Informe o segmento e a cidade quando solicitado, por exemplo:
3.Aguarde a coleta dos dados.
4.Os resultados serão salvos em um arquivo Excel chamado results.xlsx.

**Dependências**
* pandas
* selenium
* webdriver_manager
* re (expressões regulares)
* json

## 2. API de coleta de dados via URL
Este segundo script é uma aplicação Flask que permite realizar a coleta de dados através de uma URL. Ao acessar o endpoint da API, é possível informar o segmento e a cidade na URL e obter os resultados em formato JSON.

**Execução**
1.Execute o script Flask no seu ambiente Python.
2.No navegador ou via um cliente de API, acesse o seguinte formato de URL:
http://localhost:5000/api/collect_data/<segmento>/<cidade>

Substitua <segmento> e <cidade> pelos valores desejados, por exemplo:

http://localhost:5000/api/collect_data/restaurantes/Sao%20Paulo

3.O resultado será exibido no navegador em formato JSON, contendo os dados das empresas encontradas.

**Dependências**
* Flask
* selenium
* webdriver_manager
* re (expressões regulares)
* json

## Fontes
Este projeto foi inspirado no repositório original de Michael Kitas: https://github.com/michaelkitas/Google-Maps-Leads-Scraper-Selenium.
Fiz adaptações para incluir novas funcionalidades, como a coleta de dados em formato Excel e a integração com Flask para API.

## Problemas Comuns
Se o script parar de funcionar, é possível que seja necessário limpar o cache do ChromeDriver. Para resolver:

1.Apague a pasta que se encontra no caminho C:\Users\User\.wdm\drivers\chromedriver.
2.Execute o sistema novamente.

### Passos para Instalação

1. **Clone o repositório:**

   ```bash
   git clone https://github.com/tairony-cristian/scraper-selenium-google-maps.git
   
2. **Instale as dependências:**

pip install -r requirements.txt

Como Executar

Após a instalação, você pode executar a aplicação com o comando: python main.py
