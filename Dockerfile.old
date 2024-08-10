# Usar a imagem base do Python 3.12
FROM python:3.12-slim

# Definir o diretório de trabalho
WORKDIR /

# Copiar os arquivos de requisitos e instalar as dependências
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o restante do código da aplicação
COPY . .

# Expor a porta em que a aplicação será executada
EXPOSE 5000

# Comando para iniciar a aplicação Flask
CMD ["python", "main.py"]
