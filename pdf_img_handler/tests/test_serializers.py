import pytest
import base64
import os
from pdf_img_handler.api.serializers import Base64FileUploadSerializer



@pytest.mark.django_db
def test_serializer_valid_data():
    # Paths for the test files
    test_path = os.path.dirname(os.path.abspath(__file__))
    pdf = os.path.join(test_path, 'test.pdf')
    img = os.path.join(test_path, 'test.webp')
    # Read the PDF file and encode it as Base64
    with open(pdf, "rb") as file:
        file_data = file.read()
        base64_pdf = base64.b64encode(file_data).decode("utf-8")


    # Read the image file and encode it as Base64
    with open(img, "rb") as file:
        file_data = file.read()
        base64_img = base64.b64encode(file_data).decode("utf-8")

    # Test with PDF Base64 data
    serializer_pdf = Base64FileUploadSerializer(data={'file': str(base64_pdf)})
    assert serializer_pdf.is_valid() is True

    # Test with image Base64 data
    serializer_img = Base64FileUploadSerializer(data={'file': str(base64_img)})
    assert serializer_img.is_valid() is True

    # Test with invalid string data
    serializer_somedata = Base64FileUploadSerializer(data={'file': 'invalid_base64_string'})
    assert serializer_somedata.is_valid() is False



