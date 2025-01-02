from rest_framework import serializers
import magic
from pdf_img_handler.models import ImgFile, PdfFile
from pdf_img_handler.utils import ProcessFileData
import uuid, io, base64
from django.core.files.base import ContentFile


class Base64FileField(serializers.Field):
    """
    Custom serializer field to handle base64-encoded file input.
    This will decode the base64 string and return a file-like object.
    """
    def to_internal_value(self, data):
        """
        Convert the base64 string to a file-like object.
        """
        try:
            # Remove the base64 encoding prefix (data:image/png;base64,...)
            if isinstance(data, str):
                data = data.strip()
                if data.startswith('data:'):
                    # Find the comma separating metadata and the base64 string
                    base64_data = data.split(',', 1)[1]
                else:
                    base64_data = data
            else:
                raise serializers.ValidationError("Invalid file format")
            
            # Decode the base64 string to bytes
            file_data = base64.b64decode(base64_data)

            # Use python-magic to determine the MIME type of the file
            mime = magic.Magic(mime=True)
            mime_type = mime.from_buffer(file_data)

            # Validate file type: image or pdf only
            if not mime_type.startswith('image') and mime_type != 'application/pdf':
                raise serializers.ValidationError(f"Unsupported file type: {mime_type}. Only images and PDF files are allowed.")

            # Map MIME type to file extension
            if mime_type.startswith('image'):
                extension = mime_type.split('/')[1]  # e.g., 'jpeg', 'png'
            elif mime_type == 'application/pdf':
                extension = 'pdf'
            
            # Create a file name with the appropriate extension
            file_name = f"{uuid.uuid4()}.{extension}"

            # Wrap the byte data in a ContentFile and assign the file name
            content_file = ContentFile(file_data, name=file_name)
            
            return content_file
        except Exception as e:
            raise serializers.ValidationError(f"Error decoding base64 file: {str(e)}")

    def to_representation(self, value):
        """
        Convert the file-like object back to a base64 string.
        """
        return  base64.b64encode(value.read()).decode('utf-8')
    
# ---------------------------------------------------------------- 

class Base64FileUploadSerializer(serializers.Serializer):
    file = Base64FileField(write_only=True)

    def validate(self, attrs):
        file = attrs['file']
        
        # Process the file (img or pdf)
        file_processor = ProcessFileData(file)
        
        if not file_processor.valid():
            raise serializers.ValidationError(f"Invalid file format. Only supports {file_processor.allowed_extensions.keys()}")

        try :
            file_type , meta_data = file_processor.get_file_data()
        except Exception as e :
            raise serializers.ValidationError(f"Error processing file: {str(e)}")  

        if not file_type:
            raise serializers.ValidationError("Failed to process the file.") 
        
        model_class = self.get_model_class().get(file_type)

        if not model_class:
            raise serializers.ValidationError("Unsupported file type, only supported for images and PDFs.")
        
        attrs['model_class'] = model_class
        attrs['meta_data'] = meta_data

        return attrs

    # to auto get model from file type
    def get_model_class(self,):
        return {
            'pdf': PdfFile,
            'img': ImgFile,
        }

    def create(self, validated_data):
        file = validated_data.get('file')
        meta_data = validated_data.get('meta_data')
        model_class = validated_data.get('model_class')

        file_name = f"{uuid.uuid4()}.{file.name.split('.')[-1]}"
        instance = model_class.objects.create(location=file, name=file_name, **meta_data)

        return instance
    
    # override the default to_representation 
    def to_representation(self, instance):
        return {
            'id': instance.id,
            'name': instance.name,
            'location': instance.get_file_location,
        }


class PdfModelSerializer(serializers.ModelSerializer):
    """
    Serializer for view PDF files.
    """
    class Meta:
        model = PdfFile
        fields = '__all__'

class ImgModelSerializer(serializers.ModelSerializer):
    """
    Serializer for view image files.
    """
    class Meta:
        model = ImgFile
        fields = '__all__'


class PdfShortModelSerializer(serializers.ModelSerializer):
    """
    Serializer for view shortened PDF files.
    """
    class Meta:
        model = PdfFile
        fields = ('id', 'name')


class ImgShortModelSerializer(serializers.ModelSerializer):
    """
    Serializer for view shortened image files.
    """
    class Meta:
        model = ImgFile
        fields = ('id', 'name')


class RotateImageSerializer(serializers.Serializer):
    """
    Serializer for rotate image files.
    """
    image_id = serializers.PrimaryKeyRelatedField(queryset=ImgFile.objects.all())

    def validate(self, attrs):
        image = attrs['image_id']
        image.rotate()  # This will rotate the image and save it back
        return image 

    def to_representation(self, instance):
        return ImgModelSerializer(instance).to_representation(instance)

class ConvertPdfToImageSerializer(serializers.Serializer):
    """
    Serializer for convert PDF to image files.
    """
    pdf_id = serializers.PrimaryKeyRelatedField(queryset=PdfFile.objects.all())
    
    def validate(self, attrs):
        pdf = attrs['pdf_id']
        file_path = pdf.convert_to_image()
        return file_path
    
    def to_representation(self, instance):
        print(instance)
        return {
            'image_path' : instance
        }
