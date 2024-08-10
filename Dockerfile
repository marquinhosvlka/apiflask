# Use uma imagem base oficial do Python
FROM python:3.10-slim

# Defina variáveis de ambiente para evitar prompts interativos durante a instalação
ENV DEBIAN_FRONTEND=noninteractive

# Crie e defina o diretório de trabalho
WORKDIR /app

# Copie o arquivo de requisitos e o script do aplicativo para o contêiner
COPY requirements.txt requirements.txt
COPY app4.py app4.py
COPY conteudo.txt conteudo.txt

# Instale as dependências do aplicativo
RUN pip install --no-cache-dir -r requirements.txt

# Exponha a porta padrão para a aplicação Flask
EXPOSE 8080

# Defina a variável de ambiente para o Flask
ENV FLASK_APP=app4.py
ENV FLASK_RUN_PORT=8080
ENV FLASK_RUN_HOST=0.0.0.0

# Comando para iniciar o servidor Flask
CMD ["flask", "run"]
