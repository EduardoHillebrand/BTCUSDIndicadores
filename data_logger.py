# data_logger.py
import csv
import os
from datetime import datetime

FILE_NAME = "btc_prices.csv"

def init_csv():
    """
    Inicializa o arquivo CSV.
    Se o arquivo não existir, cria-o e escreve o cabeçalho.
    """
    if not os.path.exists(FILE_NAME):
        with open(FILE_NAME, mode='w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["timestamp", "price"])

def log_price(price):
    """
    Registra o preço com o timestamp atual no arquivo CSV.
    
    Parâmetros:
        price (float): O preço a ser registrado.
    """
    timestamp = datetime.now().isoformat()
    with open(FILE_NAME, mode='a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([timestamp, price])
