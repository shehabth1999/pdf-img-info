from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()

router.register(r'images', views.ImgFileViewSet, basename='images')
router.register(r'pdfs', views.PdfFileViewSet, basename='pdfs')


urlpatterns = [
    path('upload/', views.FileUploadView.as_view(), name='file.upload'),
    path('rotate/', views.RotateImageView.as_view(), name='image.rotate'),
    path('convert-pdf-to-image/', views.ConvertPdfToSingleImage.as_view(), name='pdf.convert_to_image'),
    path('', include(router.urls)),
]