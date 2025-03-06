# app/utils/csv_parser.py
import csv
from io import StringIO

def parse_cardapio_csv(csv_text: str) -> list:
    """
    Converte o conteúdo do CSV em uma lista de dicionários.
    Cada dicionário representa uma linha (registro do cardápio).
    """
    f = StringIO(csv_text)
    reader = csv.DictReader(f, delimiter=",")
    cardapios = [row for row in reader]
    return cardapios
