# csv_monitor.py
import os
import time
import threading
import pandas as pd

CSV_FILE = "btc_prices.csv"

def load_csv():
    """
    Tenta carregar o CSV e retorna um DataFrame.
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

def monitor_csv(interval=10):
    """
    Monitora o CSV e, se houver atualizações (novas linhas), remove as duplicatas consecutivas,
    reescreve o CSV com os dados corrigidos e exibe o conteúdo atualizado.
    O monitor é atualizado a cada 'interval' segundos.
    """
    last_count = -1  # Para garantir a impressão na primeira vez
    while True:
        df = load_csv()
        if df is not None:
            # Remove duplicatas consecutivas com base na coluna 'price'
            df_filtered = df[df['price'].shift() != df['price']]
            # Se houver alteração, reescreve o CSV com a versão filtrada
            if len(df_filtered) < len(df):
                df_filtered.to_csv(CSV_FILE, index=False)
                df = df_filtered  # Usa a versão filtrada para exibição
            
            current_count = len(df)
            if current_count != last_count:
                # Limpa a tela (usa 'cls' no Windows ou 'clear' no Unix)
                os.system('cls' if os.name == 'nt' else 'clear')
                print("Conteúdo atualizado do CSV:", flush=True)
                print(df.to_string(index=False), flush=True)
                last_count = current_count
        time.sleep(interval)

def start_csv_monitor(interval=10):
    """
    Inicia o monitor do CSV em uma thread separada.
    """
    thread = threading.Thread(target=monitor_csv, args=(interval,), daemon=True)
    thread.start()
