from django.test import TestCase
from .models import Organization

class OrganizationModelTest(TestCase):
    def test_create_org(self):
        org = Organization.objects.create(
            name="Test Org",
            slug="test-org",
            contact_email="test@example.com"
        )
        self.assertEqual(org.slug, "test-org")
