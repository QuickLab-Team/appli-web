# appli-web


### Lancement sur puce intel

```bash
docker compose up
```

### Lancement sur puce ARM

```bash
docker compose -f  docker-compose-arm.yml up
```

Dans le terminal du container web

```bash
python3 manage.py migrate
python3 manage.py createsuperuser
```

## Accès a phpmyadmin

http://localhost:8080/

User : root
Password : rootpassword