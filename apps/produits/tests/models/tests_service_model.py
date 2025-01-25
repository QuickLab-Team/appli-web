from django.test import TestCase
from produits.models import Service

class ServiceModelTest(TestCase):

    def setUp(self):
        self.service = Service.objects.create(nom='Service 1')

    def test_service_creation(self):
        self.assertEqual(self.service.nom, "Service 1")

    def test_service_suppression(self):
        self.service.delete()
        self.assertEqual(Service.objects.count(), 0)

    def test_service_modification(self):
        self.service.nom = "Service 2"
        self.service.save()
        self.assertEqual(self.service.nom, "Service 2")