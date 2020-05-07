import requests
import pdfkit
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import BytesIO


TRANSLATION_CHUNKS = 10

SOURCE_FILE_PATH = 'path/to/source/file'
DEST_FILE_PATH = 'path/to/destination/file'

API_KEY = "YOUR-API-KEY"
TRANSLATE_API = "https://translate.yandex.net/api/v1.5/tr.json/"
FROM_TO_LANGUAGE = 'en-ru'


def pdf_to_text(pdf_file: str) -> str:
    """
    Takes path to pdf file and extracts its text content
    :param pdf_file: path-to-pdf (string)
    :return: text content
    """
    manager = PDFResourceManager()
    bytes_to_read = BytesIO()
    layout = LAParams(all_texts=True)
    device = TextConverter(manager, bytes_to_read, laparams=layout)

    with open(pdf_file, 'rb') as file:
        interpreter = PDFPageInterpreter(manager, device)
        for page in PDFPage.get_pages(file, check_extractable=True):
            interpreter.process_page(page)
        text = bytes_to_read.getvalue()

    device.close()
    bytes_to_read.close()
    return text.decode('utf-8')


def translate(text: str, lang: str) -> str:
    """
    Translates given text using a given language pattern
    :param text: any string with text for translation
    :param lang: target language for translation
    :return: translated text
    """
    params = {'key': API_KEY, 'text': text, 'lang': lang}
    response = requests.get(TRANSLATE_API + 'translate', params=params)
    return response.json()['text'][0]


def translate_to_html(original_text: str) -> None:
    """
    Gets text and creates .html document containing a table with 2 columns
    1st column is the source text split by paragraphs
    2nd column is the corresponding translation
    :param original_text: any string with text for translation
    :return: None
    """
    translation = ''
    step = len(original_text) // TRANSLATION_CHUNKS
    for i in range(TRANSLATION_CHUNKS - 1):
        translation += translate(original_text[i * step: (i + 1) * step], FROM_TO_LANGUAGE)
    translation += translate(original_text[(TRANSLATION_CHUNKS - 1) * step:], FROM_TO_LANGUAGE)

    split_text = original_text.split('\n\n')
    split_translation = translation.split('\n\n')

    with open(DEST_FILE_PATH + '.html', 'w') as f:
        f.write("""<html> <head> <meta charset="utf-8"> <title>Translation</title> </head>
         <body> <table border="1"> <caption>Translation</caption>""")

        for i in range(len(split_text)):
            f.write("<tr>\n")
            f.write("<td>{}</td>\n".format(split_text[i]))
            f.write("<td>{}</td>\n".format(split_translation[i]))
            f.write("</tr>\n")

        f.write("""</table> </body> </html>""")


if __name__ == "__main__":
    """
    Body of the tool
    1) get text content of pdf
    2) create an html document with translation
    3) convert html to pdf
    """
    text = pdf_to_text(SOURCE_FILE_PATH)
    translate_to_html(text)
    pdfkit.from_file(DEST_FILE_PATH + '.html', DEST_FILE_PATH)
