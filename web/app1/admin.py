from django.contrib import admin

from .models import Video, Client, Emotion, Statistics
# Register your models here.

admin.site.register(Video)
admin.site.register(Client)
admin.site.register(Emotion)
admin.site.register(Statistics)
