from django.contrib import admin
from . import models

admin.site.register(models.PdfFile)

admin.site.register(models.ImgFile)