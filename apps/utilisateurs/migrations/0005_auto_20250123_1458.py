from django.db import migrations
from utilisateurs.models import Utilisateur
import os

def create_admin_user(apps, schema_editor):
    Utilisateur.objects.create_superuser(
        email=os.environ.get('ADMIN_EMAIL'),
        password=os.environ.get('ADMIN_PASSWORD'),
        role='administrateur',
    )

class Migration(migrations.Migration):

    dependencies = [
        ('utilisateurs', '0004_alter_utilisateur_annee_alter_utilisateur_groupe'),
    ]

    operations = [
        migrations.RunPython(create_admin_user),
    ]
