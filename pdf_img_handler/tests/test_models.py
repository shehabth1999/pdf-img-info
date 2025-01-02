import pytest
from pdf_img_handler.models import ImgFile, PdfFile
import os

@pytest.mark.django_db
def test_models_file():
    # Paths for the test files
    test_path = os.path.dirname(os.path.abspath(__file__))
    pdf = os.path.join(test_path, 'test.pdf')
    img = os.path.join(test_path, 'test.webp')

    img_file = ImgFile.objects.create(name="test_img", location=img, width=100, height=200, channels_number=3)
    assert img_file.name == "test_img"
    assert img_file.width == 100
    assert img_file.height == 200

    img_pdf = PdfFile.objects.create(name="test_pdf", location=pdf, page_width= 100, page_height= 200, pages_number=2)
    assert img_pdf.name == "test_pdf"
    assert img_pdf.page_width == 100
    assert img_pdf.page_height == 200
    assert img_pdf.pages_number == 2

