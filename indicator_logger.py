# indicator_logger.py
import csv
import os

FILE_NAME = "btc_indicators.csv"

def init_indicator_csv():
    """
    Inicializa o arquivo CSV de indicadores, escrevendo o cabeçalho,
    caso o arquivo não exista.
    """
    if not os.path.exists(FILE_NAME):
        with open(FILE_NAME, mode="w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            header = ["timestamp", "price", "EMA", "MA", "MA75", "MA150", "RSI", "MACD", "Signal"]
            writer.writerow(header)

def log_indicator_data(timestamp, price, indicators):
    """
    Registra uma nova linha no arquivo CSV com o timestamp, o preço
    e os valores dos indicadores técnicos.
    
    Parâmetros:
        timestamp (str ou datetime): Data e hora do registro.
        price (float): Preço correspondente.
        indicators (dict): Dicionário contendo os indicadores técnicos,
                           com as chaves: "EMA", "MA", "MA75", "MA150", "RSI", "MACD", "Signal".
    """
    with open(FILE_NAME, mode="a", newline="") as csvfile:
        writer = csv.writer(csvfile)
        row = [
            timestamp,
            price,
            indicators.get("EMA", ""),
            indicators.get("MA", ""),
            indicators.get("MA75", ""),
            indicators.get("MA150", ""),
            indicators.get("RSI", ""),
            indicators.get("MACD", ""),
            indicators.get("Signal", "")
        ]
        writer.writerow(row)
