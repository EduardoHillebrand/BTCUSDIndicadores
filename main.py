# main.py
import time
import asyncio
from alpaca_stream import AlpacaStream
from indicators import calculate_indicators
from plotter import Plotter
from trend_indicator import TrendIndicator
from data_logger import init_csv, log_price
from data_loader import display_csv  
from indicator_logger import init_indicator_csv, log_indicator_data
import matplotlib.pyplot as plt
from datetime import datetime
import pandas as pd

# Inicializa os arquivos CSV (preços e indicadores)
init_csv()
init_indicator_csv()

# Carrega os dados do CSV e extrai preços e timestamps
# Supondo que seu CSV possua as colunas "timestamp" e "price"
data = pd.read_csv("btc_prices.csv")
prices = data["price"].tolist()
timestamps = pd.to_datetime(data["timestamp"]).tolist()

# Flag global para indicar quando um novo trade é recebido
new_trade_received = False

# Função de callback para os trades recebidos
async def trade_handler(trade):
    global prices, timestamps, new_trade_received
    prices.append(trade.price)
    timestamps.append(datetime.now())  # ou use trade.timestamp se disponível
    log_price(trade.price)
    print(f"Trade recebido: Preço = {trade.price}", flush=True)
    new_trade_received = True
    # Limita o tamanho das listas, se desejado
    if len(prices) > 100:
        prices.pop(0)
        timestamps.pop(0)

def main():
    global new_trade_received
    # Inicializa o plot dos indicadores e o gráfico principal
    plotter = Plotter()
    
    # Cria um novo eixo INSET para o indicador de tendência (posição ajustada conforme sua preferência)
    trend_ax = plotter.fig.add_axes([0.26, 0.95, 0.09, 0.04])
    trend_indicator = TrendIndicator(trend_ax)
    
    stream = AlpacaStream(symbol="BTC/USD", trade_handler=trade_handler)
    stream.start()

    try:
        while True:
            # Calcula os indicadores se houver dados suficientes (por exemplo, 150 registros)
            indicators = calculate_indicators(prices) if len(prices) >= 150 else None
            # Atualiza o plot com preços, timestamps e indicadores (exibindo os últimos 300 registros, por exemplo)
            plotter.update(prices, timestamps, indicators, 300)
            
            # Atualiza o indicador de tendência no eixo INSET
            trend_indicator.update(indicators)
            
            # Registra os indicadores somente se um novo trade foi recebido
            if new_trade_received and indicators is not None:
                # Pega o último registro de indicadores
                last_row = indicators.iloc[-1]
                ind_dict = {
                    "EMA": last_row["EMA"],
                    "MA": last_row["MA"],
                    "MA75": last_row["MA75"],
                    "MA150": last_row["MA150"],
                    "RSI": last_row["RSI"],
                    "MACD": last_row["MACD"],
                    "Signal": last_row["Signal"]
                }
                current_timestamp = timestamps[-1].isoformat() if timestamps else datetime.now().isoformat()
                current_price = prices[-1] if prices else 0.0
                log_indicator_data(current_timestamp, current_price, ind_dict)
                new_trade_received = False  # Reseta a flag após o log
            
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("Encerrando...", flush=True)

if __name__ == '__main__':
    main()
