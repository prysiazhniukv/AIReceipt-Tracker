import easyocr

def receipt_to_text(photo_url: str):
    reader = easyocr.Reader(['en'], gpu=False)
    result = reader.readtext(photo_url, detail=0)
    return result

