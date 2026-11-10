# Use Python 3.11 slim como base
FROM python:3.11-slim

# Variáveis de ambiente para Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Diretório de trabalho
WORKDIR /site

# Instalar dependências do sistema necessárias para PostgreSQL
RUN apt-get update && apt-get install -y \
    postgresql-client \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements e instalar dependências Python
COPY requirements.txt /site/
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copiar código do projeto
COPY . /site/

# Criar diretório para arquivos estáticos e media
RUN mkdir -p /site/staticfiles /site/media

# Coletar arquivos estáticos (será executado no entrypoint)
# RUN python manage.py collectstatic --noinput

# Expor porta 8000
EXPOSE 8000

# Script de inicialização
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
