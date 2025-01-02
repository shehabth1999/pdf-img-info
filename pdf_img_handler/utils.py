from PIL import Image
import PyPDF2, os

class ProcessImage:
    def process_file(self, file):
        """
        Process an image to get its width, height, and the number of channels.
        Returns: width, height, and channels number of the image.
        """
        # Open the image using Pillow
        image = Image.open(file)

        # Get image width and height
        width, height = image.size

        # Get number of channels (RGB has 3 channels, RGBA has 4 channels)
        if image.mode in ['RGB', 'RGBA']:
            channels_number = len(image.getbands())  # RGBA has 4 channels, RGB has 3 channels
        else:
            channels_number = 1  # Default to 1 channel for grayscale or others

        return {
                'width': width, 
                'height': height, 
                'channels_number': channels_number
        }
        

    
class ProcessPdf:
    def process_file(self, file):
        """
        Process a PDF file to get the page width, page height, and number of pages.
        Returns: page width, page height, and the number of pages of the PDF.
        """
        # Initialize PDF reader
        pdf_reader = PyPDF2.PdfReader(file)

        # Get the number of pages
        pages_number = len(pdf_reader.pages)

        # Get the first page to extract dimensions
        first_page = pdf_reader.pages[0]

        # Extract page dimensions (media box gives the dimensions)
        media_box = first_page.mediabox
        page_width = float(media_box.width)
        page_height = float(media_box.height)

        return {
                'page_width':page_width, 
                'page_height': page_height, 
                'pages_number':pages_number
            }



class ProcessFileData:
    """
    Process file data (image or PDF) and return relevant information.
    """

    def __init__(self, file):
        self.file = file
        self.allowed_extensions = self.get_allowed_extensions()
        self.allowed_process = self.get_allowed_process()

        

    def get_allowed_extensions(self):
        # file extension : file type
        return {
            'pdf': 'pdf',
            'png': 'img',
            'jpg': 'img',
            'jpeg': 'img',
            'webp': 'img',
            'jpe': 'img',
            'jif': 'img',
            'jpe': 'img',
            'jfif': 'img',
            'jfi': 'img',
        }
    
    def get_allowed_process(self):
        # every file type must use process class
        return {
            'pdf': ProcessPdf,
            'img': ProcessImage,
        }
    
    def check_file_support(self):
        # check the file is supported
        return self.get_file_extension() in self.allowed_extensions.keys()

    def valid(self):
        # check the file type is valid and supported
        return self.check_file_support() and self.get_file_type()

    def get_file_extension(self):
        # get the file extension from its name, and convert it to lower case
        file_name, file_extension = os.path.splitext(self.file.name)
        return file_extension[1:].lower()

    def get_file_type(self):
        # get the file type from its extension
        extension = self.get_file_extension()
        return self.allowed_extensions.get(extension)
    
    def get_process_class(self, file_type):
        # get the process class from its file type, if it exists
        return self.allowed_process.get(file_type)
    
    def get_file_data(self):
        if not self.valid():
            return None , None
        file_type = self.get_file_type()
        process_class = self.get_process_class(file_type)
        meta_info = process_class().process_file(self.file)
        return file_type , meta_info
