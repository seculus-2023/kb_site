#!/bin/bash

# Esperar o PostgreSQL estar pronto
echo "Aguardando PostgreSQL iniciar..."
while ! nc -z db 5432; do
  sleep 0.1
done
echo "PostgreSQL iniciado!"

# Aplicar migrações
echo "Aplicando migrações do banco de dados..."
python manage.py migrate --noinput

# Coletar arquivos estáticos
echo "Coletando arquivos estáticos..."
python manage.py collectstatic --noinput --clear

# Criar superusuário se não existir (opcional)
# echo "Criando superusuário..."
# python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@exemplo.com', 'senha123')"

# Iniciar servidor
echo "Iniciando servidor Django..."
exec "$@"
