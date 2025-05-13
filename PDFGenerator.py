from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.lib.units import mm
from barcode import Code128
from barcode.writer import ImageWriter
from io import BytesIO

def generate_barcode(input_string):
    """Generate a barcode image in-memory for a given string."""
    writer = ImageWriter()
    settings = {
        "module_width": 0.32,
        "module_height": 15.0,
        "quiet_zone": 6.5,
        "font_path": "Arial Bold.ttf",
        "font_size": 25,
        "text_distance": 9,
        "background": 'white',
        "foreground": 'black',
        "center_text": True,
        "format": "png",
        "dpi": 600,
        "write_text": True
    }
    writer.set_options(settings)
    file_like = BytesIO()
    Code128(input_string, writer).write(file_like, options=settings)
    file_like.seek(0)
    return file_like

def generatePDF2(barcode_images):
    """Generate a PDF with 8 barcodes per 8.5x11" letter page and return BytesIO."""
    H, W = 230, 320
    L, R = 0, 290
    O, B = 180 + 16, 42

    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)

    while barcode_images:
        positions = [(L, O*3 - B), (R, O*3 - B),
                     (L, O*2 - B), (R, O*2 - B),
                     (L, O*1 - B), (R, O*1 - B),
                     (L, O*0 - B), (R, O*0 - B)]
        for x, y in positions:
            if barcode_images:
                c.drawImage(ImageReader(barcode_images.pop(0)), x, y, width=W, height=H)
        c.showPage()

    c.save()
    buffer.seek(0)
    return buffer

def generatePDF3(barcode_images):
    """Generate a PDF with 2 barcodes per 4x6" label page and return BytesIO."""
    L, T, B, W, H = -30, 180, -35, 350, 240
    page_size = (102 * mm, 152 * mm)

    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=page_size)

    while barcode_images:
        if barcode_images:
            c.drawImage(ImageReader(barcode_images.pop(0)), L, T, width=W, height=H)
        if barcode_images:
            c.drawImage(ImageReader(barcode_images.pop(0)), L, B, width=W, height=H)
        c.showPage()

    c.save()
    buffer.seek(0)
    return buffer


def generate_pdf(barcode_strings, mode='standard'):
    """
    Generate a barcode PDF and return as BytesIO stream.
    
    :param barcode_strings: List of strings to encode as barcodes.
    :param mode: 'standard' or 'label'.
    :return: BytesIO object of the generated PDF.
    """
    barcode_images = [generate_barcode(s) for s in barcode_strings]

    if mode == 'standard':
        return generatePDF2(barcode_images)
    elif mode == 'label':
        return generatePDF3(barcode_images)
    else:
        raise ValueError("Invalid mode. Use 'standard' or 'label'.")