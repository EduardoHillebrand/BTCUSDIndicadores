# alpaca_stream.py
import os
import threading
from alpaca.data.live import CryptoDataStream

class AlpacaStream:
    def __init__(self, symbol="BTC/USD", trade_handler=None):
        self.api_key = os.getenv('APCA_API_KEY_ID')
        self.api_secret = os.getenv('APCA_API_SECRET_KEY')
        self.symbol = symbol
        self.trade_handler = trade_handler
        self.stream = CryptoDataStream(self.api_key, self.api_secret)
        
    def start(self):
        # Inscreve a função de callback para os trades
        self.stream.subscribe_trades(self.trade_handler, self.symbol)
        # Executa o streaming em uma thread separada para não bloquear o main loop
        thread = threading.Thread(target=self.stream.run, daemon=True)
        thread.start()
