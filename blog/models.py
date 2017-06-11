from django.db import models
from django.utils import timezone
from django.db.models.signals import pre_save

from django.utils.text import slugify


class Category(models.Model): 
    title = models.CharField(max_length=200) 
    slug = models.SlugField(max_length=40, unique=True) 
    description = models.TextField()
    
    class Meta: 
        verbose_name_plural = "Categories"

    def __str__(self):
        return '%s' % self.title

    def get_absolute_url(self):
        return "/categories/%s/" % self.slug

def upload_location(post, filename):
    return "%s/%s" %(post.slug, filename)
    

class Post(models.Model):
    author = models.ForeignKey('auth.User')
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to=upload_location,
                              null=True,
                              blank=True,
                              width_field="width_field",
                              height_field="height_field")
    height_field = models.IntegerField(default=0, null=True)
    width_field = models.IntegerField(default=0, null=True)    
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    categories = models.ManyToManyField(Category, blank=True, null=True, through='CategoryToPost')
    #tags = models.ManyToManyField(Category, blank=True, null=True, through='CategoryToPost')
    
    
    
    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):      
        return reverse("post:post_detail", kwargs={"slug": self.slug})

                       
class CategoryToPost(models.Model):
    post = models.ForeignKey(Post)
    category = models.ForeignKey(Category)
    

def create_slug(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = Post.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" %(slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug
    
def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)

    
pre_save.connect(pre_save_post_receiver, sender=Post)


class Comment(models.Model):
    post = models.ForeignKey('blog.Post', related_name='comments')
    author = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.text
