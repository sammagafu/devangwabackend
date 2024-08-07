from django.contrib import admin
from . models import Category, Thread,   ThreadReply, ThreadLike, PostLike

# Register your models here.
admin.site.register(Thread)
admin.site.register(ThreadReply)
