from django.db import models
from DjangoMainECommerce.models import BaseModel
from django.utils.text import slugify
from django.core.exceptions import ValidationError

# Create your models here.
class Products(BaseModel):
    name = models.CharField(max_length=40)
    quantity = models.PositiveIntegerField(default=0)
    sale = models.PositiveIntegerField(default=0)
    warranty = models.CharField(max_length=170, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    additional_info = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    is_active = models.BooleanField(default=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='products')
    subcategory = models.ForeignKey('SubCategory', on_delete=models.CASCADE, blank=True, null=True)
    
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
        
    def is_main_image(self):
        main = self.images.filter(is_main=True).first()
        if main:
            return main.image.url
        first = self.images.first()
        if first:
            return first.image.url
        return None
        
    @property
    def discount(self):
        if self.sale:
            return self.price - (self.price * self.sale / 100)
        return self.price
    
    @property
    def average_rating(self):
        reviews = self.reviews.all()
        if not reviews:
            return 0
        total = 0
        for r in reviews:
            total += r.rating
        return round(total / len(reviews), 1)

    @property
    def total_rating(self):
        return len(self.reviews.all())
        
    @property
    def in_stock(self):
        return self.quantity > 0
    
    
class ProductImage(BaseModel):
    product = models.ForeignKey('Products', on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/')
    is_main = models.BooleanField(default=False)
    
        
class ProductFeature(models.Model):
    product = models.ForeignKey('Products', on_delete=models.CASCADE, related_name='features')
    text = models.CharField(max_length=175)

    def __str__(self):
        return self.text
    
    
class ProductReview(BaseModel):
    product = models.ForeignKey('Products', on_delete=models.CASCADE, related_name='reviews')
    name = models.CharField(max_length=45)
    title = models.CharField(max_length=45)
    review = models.TextField()
    rating = models.PositiveIntegerField(default=1)
    
    def __str__(self):
        return f'{self.product.name} {self.title} {self.rating}'
    
    def clean(self):
        if self.rating < 1 or self.rating > 5:
            raise ValidationError('rating b/w 1 to 5 stars allowed') 
        
       
class Category(models.Model):
    name = models.CharField(max_length=40)
    description = models.TextField(blank=True, null=True)
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
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    slug = models.SlugField(unique=True, blank=True)
    
    def save(self, *args, **kwargs):
      self.slug = self.slug or slugify(self.name)
      super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    