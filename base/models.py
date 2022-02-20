import uuid
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from PIL import Image
from mptt.models import MPTTModel, TreeForeignKey
from django.contrib.auth.models import User


class BaseManager(models.Manager):# some objects can be accesible
    def get_queryset(self):         # only from admin pannel
        return super(BaseManager, self).get_queryset().\
                              exclude(is_admin_only=True)

class Base(models.Model):
    id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False,db_index=True)
    name=models.CharField(max_length=20,unique=True,db_index=True)
    slug=models.SlugField(max_length=40,unique=True,db_index=True)
    is_admin_only=models.BooleanField(default=False)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    objects=BaseManager()


    class Meta:
        abstract = True
        ordering = ['-updated','-created']

    def __str__(self):
        return self.name

    def save(self,*a,**k):
        self.slug=slugify(self.name)
        super().save(*a,**k)

    def get_absolute_url(self):
        cls_name=self.__class__.__name__.lower()
        return reverse("base:"+cls_name,args=[self.slug])


class Subject(Base):
    is_tech = models.BooleanField(blank=True,default=False)


class Users(User):
    CHOICES = (
        ("good", "good"),
        ("normal", "normal"),
        ("bad", "bad")
    )
    behavior = models.CharField(choices=CHOICES,null=True, blank=True,max_length=20)
    picture = models.ImageField(default='pictures/default_student_pic.jpg',
                                upload_to='pictures', blank=True)
    updated = models.DateTimeField(auto_now=True)
    is_admin_only = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural='UserTable'
        ordering = ['-updated','-date_joined']

    def save(self, *a, **k):
        self.slug = slugify(self.username)
        super().save(*a, **k)

        img = Image.open(self.picture.path)
        if img.height > 900 or img.width > 800:
            img.thumbnail((900, 800))
            img.save(self.picture.path)


class ClsManager(models.Manager):
    def get_queryset(self):
        return super(ClsManager, self).get_queryset().\
                              exclude(is_admin_only=True).\
                              select_related('teacher','subject').\
                              prefetch_related('students')

class Classroom(Base):
     teacher=models.ForeignKey(User,on_delete=models.PROTECT)
     students = models.ManyToManyField(User,related_name='students')
     subject = models.ForeignKey(Subject, on_delete=models.PROTECT)
     description=models.CharField(max_length=100)
     entries=models.PositiveSmallIntegerField(default=0)
     objects=ClsManager()

     class Meta:
         unique_together=(('teacher','subject'),('name','subject'))


class CmtManager(models.Manager):
    def get_queryset(self):
        return super(CmtManager, self).get_queryset().\
                          exclude(is_admin_only=True).\
                          select_related('sender', 'classroom')

class Comment(MPTTModel):
    id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False,db_index=True)
    is_admin_only=models.BooleanField(default=False)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    text = models.TextField(max_length=50)
    parent = TreeForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, related_name="children")
    objects = CmtManager()

    def __str__(self):
        return str(self.id)

    class MPTTMeta:
        order_insertion_by = ["id"]

