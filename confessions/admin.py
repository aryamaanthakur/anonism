from django.contrib import admin
from .models import Confession, ConfessionReport, ConfessionRequest

admin.site.register(Confession)
admin.site.register(ConfessionRequest)
admin.site.register(ConfessionReport)