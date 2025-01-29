# appli-web

### Lancement des tests

```bash
python manage.py test apps

coverage run --source='apps/produits' manage.py test apps/produits

coverage report
```

### Données de test

```bash
python3 manage.py setdata
```

### Lancement sur puce intel

```bash
docker compose up --build -d
```

### Lancement sur puce ARM

```bash
docker compose -f docker-compose-arm.yml up --build -d
```

### Lancement en production

```bash
docker compose -d -f docker-compose-prod.yml --env-file .env-production up --build
```

Dans le terminal du container web

```bash
python3 manage.py migrate
python3 manage.py createsuperuser
```

### Création de l'image et push sur docker Hub

```bash
docker build -t quentin1591/quicklab:latest .
docker push quentin1591/quicklab:latest
```


## Accès a phpmyadmin

http://localhost:8080/

User : root
Password : rootpassword