# Usar a imagem base do Python 3.12
FROM python:3.12-slim

# Definir o diretório de trabalho
WORKDIR /app

# Copiar os arquivos de requisitos e instalar as dependências
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o código da aplicação e o arquivo de conteúdo
COPY app4.py /app/
COPY conteudo.txt /app/

# Expor a porta em que a aplicação será executada
EXPOSE 8080

# Comando para iniciar a aplicação Flask
CMD ["python", "app4.py"]
