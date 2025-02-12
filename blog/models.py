from django.db import models
from django.utils.text import slugify
from django.db.models.signals import pre_save

class NewsUser(models.Model):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('editor', 'Editor'),
        ('viewer', 'Viewer'),
    ]
    role = models.CharField(max_length=50, choices=ROLE_CHOICES)

    def str(self):
        return self.role

class NewsTag(models.Model):
    name = models.CharField(max_length=100)

    def str(self):
        return self.name

class Article(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    main_image_url = models.URLField(max_length=500, blank=True, null=True)
    summary = models.TextField(blank=True, null=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)
    publish_at = models.DateTimeField(blank=True, null=True)

    def str(self):
        return self.title

class News(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    short_description = models.CharField(max_length=500, blank=True, null=True)
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(NewsUser, on_delete=models.SET_NULL, null=True)
    tags = models.ManyToManyField(NewsTag, blank=True)
    article = models.OneToOneField(Article, on_delete=models.CASCADE, null=True, blank=True)
    image = models.ImageField(upload_to='news_images/', blank=True, null=True)
    File = models.FileField(max_length=500, blank=True, null=True)

    def str(self):
        return self.title

def generate_unique_slug(instance, new_slug=None):
    slug = slugify(instance.title) if new_slug is None else new_slug
    Klass = instance.__class__
    qs = Klass.objects.filter(slug=slug).exclude(id=instance.id)
    if qs.exists():
        slug = f"{slug}-{qs.count()}"
        return generate_unique_slug(instance, slug)
    return slug

def pre_save_slug(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = generate_unique_slug(instance)

pre_save.connect(pre_save_slug, sender=News)
pre_save.connect(pre_save_slug, sender=Article)