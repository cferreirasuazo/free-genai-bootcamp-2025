from manga_ocr import MangaOcr


def ocr_image(image):
    mocr = MangaOcr()
    """function for analyze image using MangaOCR"""
    return mocr(image)