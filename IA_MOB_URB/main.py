import webview
import sys
import os
from ia_mobilidade_oop import IAMobilidade

class API:
    def __init__(self):
        self.ia = IAMobilidade()

    def analisar(self, lista_problemas):
        return self.ia.analisar(lista_problemas)

api = API()

# Caminho para HTML
if getattr(sys, 'frozen', False):
    BASE_DIR = sys._MEIPASS
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
HTML_PATH = os.path.join(BASE_DIR, "templates", "index.html")

window = webview.create_window(
    "IA Mobilidade Urbana",
    HTML_PATH,
    width=900,
    height=700,
    resizable=True,
    js_api=api
)

webview.start(debug=False)
