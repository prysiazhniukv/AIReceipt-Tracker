import easyocr

reader = easyocr.Reader(['en'], gpu=False)
result = reader.readtext("images/fred_meyer_1.jpg", detail=0)
