# appli-web

### Lancement des tests

```bash
python manage.py test apps
```

### Données de test

```bash
python3 manage.py setdata
```

### Lancement sur puce intel

```bash
docker compose up
```

### Lancement sur puce ARM

```bash
docker compose -f docker-compose-arm.yml up
```

Dans le terminal du container web

```bash
python3 manage.py migrate
python3 manage.py createsuperuser
```

### Création de l'image et push sur docker Hub

```bash
docker build -t <nom_utilisateur>/quicklab:latest .
docker push <nom_utilisateur>/quicklab:latest
```


## Accès a phpmyadmin

http://localhost:8080/

User : root
Password : rootpassword