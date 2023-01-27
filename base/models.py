from django.db import models
from django.contrib.auth.models import AbstractUser
from django.template.defaultfilters import slugify
import random


class User(AbstractUser):
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(null=True, unique=True)
    bio = models.TextField(null=True, blank=True)

    # avatar = models.ImageField(null=True, default="avatar.svg")
    avatar = models.ImageField(null=True)

    pic = models.CharField(max_length=200)

    def getPicture(self):
        if len(self.name) % 10 == 1:
            return "images/icon1.png"
        elif len(self.name) % 10 == 2:
            return "images/icon2.png"
        elif len(self.name) % 10 == 3:
            return "images/icon3.png"
        elif len(self.name) % 10 == 4:
            return "images/icon4.png"
        elif len(self.name) % 10 == 5:
            return "images/icon5.png"
        else:
            return "images/icon6.png"

    def save(self, *args, **kwargs):
        if not self.pic:
            self.pic = self.getPicture()
        super(User, self).save(*args, **kwargs)

    # def activate(request, uidb64, token, backend='django.contrib.auth.backends.ModelBackend'):
    #     try:
    #         uid = force_text(urlsafe_base64_decode(uidb64))
    #         user = User.objects.get(pk=uid)
    #     except (TypeError, ValueError, OverflowError, User.DoesNotExist):
    #         user = None

    #     if user is not None and account_activation_token.check_token(user, token):
    #         user.is_active = True
    #         user.profile.email_confirmed = True
    #         user.save()
    #         login(request, user, backend='django.contrib.auth.backends.ModelBackend')
    #         return redirect('home')
    #     else:
    #         return render(request, 'account_activation_invalid.html')


class Topic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    participants = models.ManyToManyField(User, related_name="participants", blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    slug = models.SlugField(unique=True, null=True)

    class Meta:
        ordering = ["-updated", "-created"]  # dash reverses order

    def __str__(self):
        return self.name

    # slug -> inherited save method overriten to slugify url
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.body[0:50]

    class Meta:
        ordering = ["-updated", "-created"]  # dash reverses order
