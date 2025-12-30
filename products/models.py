from django.db import models
from DjangoMainECommerce.models import BaseModel
from django.utils.text import slugify

# Create your models here.
class Products(BaseModel):
    name = models.CharField(max_length=40)
    quantity = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    is_active = models.BooleanField(default=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='products')

    def __str__(self):
        return self.name
    
    def inc_stock(self, amount):
        self.quantity += amount
        self.save()
        
    def dec_stock(self, amount):
        if amount > self.quantity:
            raise ValueError("stock is less")
        self.quantity -= amount
        self.save()
        
        
class ProductImage(BaseModel):
    product = models.ForeignKey('Products', on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/')
    is_main = models.BooleanField(default=False)
    
    def save(self, *args, **kwargs):
        if self.is_main:
            extra_images = ProductImage.objects.filter(product=self.product, is_main=True).exclude(pk=self.pk)
            extra_images.update(is_main=False)
        super().save(*args, **kwargs)
       
       
class Category(models.Model):
    name = models.CharField(max_length=40)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    slug = models.SlugField(unique=True, blank=True)
    
    def save(self, *args, **kwargs):
      self.slug = self.slug or slugify(self.name)
      super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name
    
    
class SubCategory(models.Model):
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='subcategories')
    name = models.CharField(max_length=40)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    slug = models.SlugField(unique=True)
    
    def save(self, *args, **kwargs):
      self.slug = self.slug or slugify(self.name)
      super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    