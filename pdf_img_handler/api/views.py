from rest_framework.generics import CreateAPIView, DestroyAPIView
from .serializers import Base64FileUploadSerializer, ImgModelSerializer, PdfModelSerializer, ImgShortModelSerializer, PdfShortModelSerializer, RotateImageSerializer, ConvertPdfToImageSerializer
from pdf_img_handler.models import ImgFile, PdfFile
from rest_framework.viewsets import ReadOnlyModelViewSet



class BaseFileMVC(ReadOnlyModelViewSet, DestroyAPIView):
    """Base class for retrieving, listing, and deleting"""
    pass

# ----------------------------------------------------


class FileUploadView(CreateAPIView):
    """
    API endpoint for uploading a base64-encoded file and saving it as file in server and location to the database.
    """
    serializer_class = Base64FileUploadSerializer


class ImgFileViewSet(BaseFileMVC):
    """
    API endpoint for 
    1: get all images from the database
    2: get image by id with more details
    3: delete image from database by id
    """
    queryset = ImgFile.objects.all()
    serializer_class = ImgModelSerializer

    def get_serializer_class(self):
        if self.action == 'list':
            self.serializer_class = ImgShortModelSerializer
        return super().get_serializer_class()


class PdfFileViewSet(BaseFileMVC):
    """
    API endpoint for 
    1: get all pdfs from the database
    2: get pdf by id with more details
    3: delete image from database by id
    """
    queryset = PdfFile.objects.all()
    serializer_class = PdfModelSerializer

    def get_serializer_class(self):
        if self.action == 'list':
            self.serializer_class = PdfShortModelSerializer
        return super().get_serializer_class()

        
class RotateImageView(CreateAPIView):
    """
    API endpoint for rotating an image by 90 degrees clockwise.
    """
    serializer_class = RotateImageSerializer
    def perform_create(self, serializer):
        pass

    
class ConvertPdfToSingleImage(CreateAPIView):
    """
    API for converting an pdf to a single image file
    """
    serializer_class = ConvertPdfToImageSerializer
    def perform_create(self, serializer):
        pass