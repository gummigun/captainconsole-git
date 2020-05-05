from django.db import models

# Create your models here.
<<<<<<< HEAD
=======

"""These are test models. They will be replaced later (or ignored)."""
class ProductCategoriesTest(models.Model):
    name = models.CharField(max_length=255)
    def __str__(self):
        return self.name

class ProductsTest(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=999, blank=True)
    category = models.ForeignKey(ProductCategoriesTest, on_delete=models.CASCADE)
    price = models.FloatField()
    on_sale = models.BooleanField()

    def __str__(self):
        return self.name

class ProductImageTest(models.Model):
    image = models.CharField(max_length=999)
    product = models.ForeignKey(ProductsTest, on_delete=models.CASCADE)

    def __str__(self):
        return self.image

"""Add final models here."""

# Products
# ProductCategories
# ProductImages
# ProductReviews
# Add more models
>>>>>>> project_setup
