from django.db import models


# Create your models here.
class ProductCategories(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class ShippingCodes(models.Model):
    code_name = models.CharField(max_length=255)

    def __str__(self):
        return self.code_name


class ConditionCodes(models.Model):
    condition = models.CharField(max_length=255)

    def __str__(self):
        return self.condition


class Products(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(ProductCategories, on_delete=models.CASCADE)
    console = models.CharField(max_length=255)
    manufacturer = models.CharField(max_length=255)
    price = models.FloatField()
    shpping_code = models.ForeignKey(ShippingCodes, on_delete=models.CASCADE)
    condition = models.ForeignKey(ConditionCodes, on_delete=models.CASCADE)
    description = models.CharField(max_length=4999, blank=True)

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    images = models.CharField(max_length=999)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)

    def __str__(self):
        return self.images


class ProductRating(models.Model):
    rating = models.FloatField()
    product = models.ForeignKey(Products, on_delete=models.CASCADE)

    def __str__(self):
        return self.rating


class ProductReview(models.Model):
    review = models.CharField(max_length=999)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)

    def __str__(self):
        return self.review
