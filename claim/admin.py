from django.contrib import admin

from .models import Question, KV, Claim

# Register your models here.

admin.site.register(Question)
admin.site.register(KV)
admin.site.register(Claim)
