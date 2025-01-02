from django.db import models
from PIL import Image
from django.conf import settings
import os
import fitz  # PyMuPDF


class BaseFile(models.Model):
    """
    Abstract model for files with name and timestamps.
    """
    name = models.CharField(max_length=255)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name
    
    @property
    def get_file_location(self):
        return self.location.url
    
    
# ---------------------------------------------------------------- 

class ImgFile(BaseFile):
    """
    Model for image files with width, height, channels number.
    """
    location = models.ImageField(upload_to='img/')
    width = models.PositiveIntegerField(null=True)
    height = models.PositiveIntegerField(null=True)
    channels_number = models.PositiveIntegerField(null=True)

    def rotate(self):
        """
        Rotate the image by a fixed 90 degrees and save it back to its original location.

        :return: Rotated image
        """
        # Open the image
        image = Image.open(self.location.path)

        # Rotate the image by a fixed 90 degrees
        rotated_image = image.rotate(90, expand=True)  # expand=True ensures the entire image is visible

        # Save the rotated image back to the original file path
        rotated_image.save(self.location.path)

        # Update the width, height, and channels_number fields after rotation
        self.width, self.height = rotated_image.size
        self.channels_number = len(rotated_image.getbands()) 
        self.save()
        return rotated_image



class PdfFile(BaseFile):
    """
    Model for PDF files with page width, height, and number of pages.
    """
    location = models.FileField(upload_to='pdf/')
    page_width = models.PositiveIntegerField()
    page_height = models.PositiveIntegerField()
    pages_number = models.PositiveIntegerField(null=True)

    def convert_to_image(self, image_format="png"):
        """
        Convert the entire PDF to a single image by combining all pages.
        """
        pdf_path = self.location.path
        output_image_path = os.path.join(settings.MEDIA_ROOT, 'pdf_images', f'{self.id}.{image_format}')

        try:
            # Open the PDF file using PyMuPDF
            doc = fitz.open(pdf_path)

            # Create a list to hold the images of each page
            images = []

            # Loop through each page and convert it to an image
            for page_num in range(doc.page_count):
                page = doc.load_page(page_num)  # Load the page
                pix = page.get_pixmap(dpi=300)  # Create a pixmap (image) from the page

                # Convert the pixmap to a PIL image
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                images.append(img)

            # Combine all images into one (vertically in this case)
            total_height = sum(img.height for img in images)
            max_width = max(img.width for img in images)

            # Create a new blank image with the combined size
            combined_image = Image.new('RGB', (max_width, total_height))

            # Paste each image into the combined image
            y_offset = 0
            for img in images:
                combined_image.paste(img, (0, y_offset))
                y_offset += img.height

            # Ensure the output directory exists
            output_dir = os.path.dirname(output_image_path)
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)

            # Save the combined image
            combined_image.save(output_image_path, image_format.upper())

            # Normalize the output path for URLs (use forward slashes for URLs)
            output_url_path = os.path.join('pdf_images', f'{self.id}.{image_format}')
            output_url_path = output_url_path.replace("\\", "/")  # Ensure forward slashes for URLs

            return os.path.join(settings.MEDIA_URL, output_url_path)

        except Exception as e:
            print(f"Error during PDF conversion: {e}")
            return None