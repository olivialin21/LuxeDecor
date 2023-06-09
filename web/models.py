from django.db import models
from django.utils.text import slugify
from django.urls import reverse

# Create your models here.
class Category(models.Model):
    title = models.CharField(max_length=255, default="")

    def __str__(self):
        return self.title

# class Tag(models.Model):
#     title = models.CharField(max_length=255, default="")

#     def __str__(self):
#         return self.title
class SubCategory(models.Model):
    title = models.CharField(max_length=255, default="")
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Product(models.Model):
    title = models.CharField(max_length=255, default="")
    price = models.DecimalField(default=0, decimal_places=2, max_digits=7)
    width = models.DecimalField(default=0, decimal_places=2, max_digits=7)
    depth = models.DecimalField(default=0, decimal_places=2, max_digits=7)
    height = models.DecimalField(default=0, decimal_places=2, max_digits=7)
    description = models.TextField(default="")
    fabric = models.CharField(max_length=255, blank=True, default="")
    finish = models.CharField(max_length=255, blank=True, default="")
    slug = models.SlugField(blank=True, default="")
    category = models.ForeignKey(Category, null=True, on_delete=models.PROTECT)
    sub_category = models.ForeignKey(SubCategory, null=True, on_delete=models.PROTECT)
    image = models.ImageField(default="", blank=True, upload_to="images")
    image1 = models.ImageField(default="", blank=True, upload_to="images")
    image2 = models.ImageField(default="", blank=True, upload_to="images")
    image3 = models.ImageField(default="", blank=True, upload_to="images")
    image4 = models.ImageField(default="", blank=True, upload_to="images")

    shipping_time = models.CharField(max_length=255, blank=True, default="")
    shipping_price = models.CharField(max_length=255, blank=True, default="")
    # tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Product, self).save()

    def get_absolute_url(self):
        return reverse("detail", args=[str(self.slug)])

