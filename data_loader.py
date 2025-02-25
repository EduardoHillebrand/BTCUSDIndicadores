# data_loader.py
import os
import pandas as pd

CSV_FILE = "btc_prices.csv"

def load_csv():
    """
    Carrega o arquivo CSV e retorna um DataFrame, se existir.
    """
    if os.path.exists(CSV_FILE):
        try:
            df = pd.read_csv(CSV_FILE)
            return df
        except Exception as e:
            print(f"Erro ao ler o CSV: {e}", flush=True)
            return None
    else:
        print(f"Arquivo {CSV_FILE} não encontrado.", flush=True)
        return None

def display_csv():
    """
    Exibe o conteúdo do CSV na tela e retorna a lista de preços.
    """
    df = load_csv()
    if df is not None:
        print("Tem conteúdo do arquivo CSV", flush=True)
        #print(df.to_string(index=False), flush=True)
        # Supondo que a coluna 'price' contenha os preços
        return df['price'].tolist()
    else:
        print("Nenhum dado carregado.", flush=True)
        return []
