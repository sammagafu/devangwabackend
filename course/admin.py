from django.contrib import admin
from .models import Course,Module,Video,Document,Question,Quiz,Answer,Enrollment
# Register your models here.
admin.site.register(Course)
admin.site.register(Module)
admin.site.register(Video)
admin.site.register(Document)
admin.site.register(Question)
admin.site.register(Quiz)
admin.site.register(Answer)
admin.site.register(Enrollment)