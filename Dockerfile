# Utiliser une image de base officielle de Python
FROM python:3.11

# Définir le répertoire de travail dans le conteneur
WORKDIR /code

# Copier le fichier requirements.txt dans le répertoire de travail
COPY requirements.txt /code/

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copier le reste du code de l'application dans le répertoire de travail
COPY . /code/

# Exposer le port que l'application Django utilise
EXPOSE 8000

# Définir la commande par défaut pour exécuter l'application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]