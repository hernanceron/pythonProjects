from django.test import TestCase
from django.urls import reverse
from catalog import models
import datetime

# Create your tests here.
class TestPage(TestCase):
    def test_about_us_page_works(self):
        response = self.client.get(reverse("about-us"))
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'about_us.html')
        self.assertContains(response, 'BabyPromo')

    def test_active_manager_works(self):
        models.Store.objects.create(
            name="METRO",
            status="inactivo"
        )
        m = models.Store.objects.get(name="METRO")

        models.Store.objects.create(
            name="VEA",
            status="activo"            
        )
        v = models.Store.objects.get(name="VEA")

        models.Product.objects.create(
            name="Pañales para Bebé HUGGIES Natural Care Talla XG Paquete 42un",
            published_date = datetime.datetime.today(),
            code = "20148267",
            brandName = "HUGGIES",
            image_url = "https://plazavea.vteximg.com.br/arquivos/ids/203493-450-450/20148267.jpg?v=636754612854530000",
            price = "S/ 46.90",
            discount_price = "S/ 39.90",
            store = v,
            principalCode = "2000036"
        )

        models.Product.objects.create(
            name="Pañales para Bebé Pampers Confort Sec Talla P Paquete 46 unid",
            published_date = datetime.datetime.today(),
            code = "570584",
            brandName = "PAMPERS",
            image_url = "https://wongfood.vteximg.com.br/arquivos/ids/261723-750-750/frontal-118598.jpg?v=636796296844330000",
            price = "S/. 26.50",
            discount_price = "S/. 25.50",
            store = m,
            principalCode = "2000007"
        )

        self.assertEqual(len(models.Product.objects.active()),1)