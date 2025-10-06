# Étape 1 : construire l'image Python
FROM python:3.12-slim

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers de dépendances et installer
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier le reste du projet
COPY . .

# Appliquer les migrations de la base de données
RUN python manage.py migrate

# Collecter les fichiers statiques
RUN python manage.py collectstatic --noinput

# Exposer le port
EXPOSE 8000

# Commande de lancement
CMD ["gunicorn", "dms_cccm.wsgi:application", "--bind", "0.0.0.0:8000"]
