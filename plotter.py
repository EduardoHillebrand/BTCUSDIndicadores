# plotter.py
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

class Plotter:
    def __init__(self):
        plt.ion()
        self.fig, self.axs = plt.subplots(3, figsize=(10, 8), 
                                          gridspec_kw={'height_ratios': [2, 1, 1]})
        self.ax_price, self.ax_rsi, self.ax_macd = self.axs
        self.fig.suptitle("Indicadores Técnicos - BTC/USD")
        self._init_plots()

    def _init_plots(self):
        # Plot de preço e médias
        self.line_price, = self.ax_price.plot([], [], label="Preço")
        self.line_ema, = self.ax_price.plot([], [], label="EMA (20)", linestyle='-')
        self.line_ma, = self.ax_price.plot([], [], label="MA (20)", linestyle='--')
        self.line_ma75, = self.ax_price.plot([], [], label="MA (75)", linestyle='--')
        self.line_ma150, = self.ax_price.plot([], [], label="MA (150)", linestyle='--')
        self.ax_price.legend()
        self.ax_price.grid()

        # Plot do RSI
        self.line_rsi, = self.ax_rsi.plot([], [], label="RSI", color='blue')
        self.ax_rsi.axhline(70, color='red', linestyle='--', linewidth=1, label="Overbought")
        self.ax_rsi.axhline(30, color='green', linestyle='--', linewidth=1, label="Oversold")
        self.ax_rsi.set_ylim(0, 100)
        self.ax_rsi.legend(loc='upper left')
        self.ax_rsi.grid()

        # Plot do MACD
        self.line_macd, = self.ax_macd.plot([], [], label="MACD", color='purple')
        self.line_signal, = self.ax_macd.plot([], [], label="Signal Line", color='orange')
        self.ax_macd.axhline(0, color='black', linestyle='--', linewidth=1)
        self.ax_macd.legend()
        self.ax_macd.grid()

        # Área para mensagens
        self.text_message = self.fig.text(0.5, 0.95, "", ha='center', fontsize=12, color='red')

    def update(self, prices, timestamps, indicators=None, maxToShow=500):
        total_records = len(prices)
        # Seleciona os últimos maxToShow registros para plotagem
        if total_records > maxToShow:
            start_idx = total_records - maxToShow
            plot_prices = prices[-maxToShow:]
            plot_timestamps = list(timestamps[-maxToShow:])
        else:
            start_idx = 0
            plot_prices = prices
            plot_timestamps = list(timestamps)
        
        # Atualiza o gráfico de preços utilizando timestamps no eixo x
        self.line_price.set_xdata(plot_timestamps)
        self.line_price.set_ydata(plot_prices)
        if len(plot_timestamps) > 0:
            self.ax_price.set_xlim(plot_timestamps[0], plot_timestamps[-1])
        else:
            self.ax_price.set_xlim(0, 1)
        # Configura o eixo x para exibir datas/hora
        self.ax_price.xaxis_date()
        self.ax_price.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m %H:%M'))

        # Verifica se há dados suficientes para os indicadores (por exemplo, 150 registros)
        if total_records < 150:
            self.text_message.set_text("Aguardando dados suficientes para calcular indicadores...")
        else:
            self.text_message.set_text("")
            if indicators is not None:
                # Filtra os indicadores para exibir apenas os registros com índice >= start_idx
                indicators_filtered = indicators[indicators.index >= start_idx]
                # Caso os indicadores filtrados tenham mais que maxToShow registros, usa apenas os últimos
                if len(indicators_filtered) > maxToShow:
                    indicators_filtered = indicators_filtered.tail(maxToShow)
                # Mapeia os índices filtrados para os timestamps correspondentes
                x_ind = [list(timestamps)[i] for i in indicators_filtered.index if i < len(timestamps)]
                
                self.line_ema.set_xdata(x_ind)
                self.line_ema.set_ydata(indicators_filtered["EMA"])
                self.line_ma.set_xdata(x_ind)
                self.line_ma.set_ydata(indicators_filtered["MA"])
                self.line_ma75.set_xdata(x_ind)
                self.line_ma75.set_ydata(indicators_filtered["MA75"])
                self.line_ma150.set_xdata(x_ind)
                self.line_ma150.set_ydata(indicators_filtered["MA150"])
                self.line_rsi.set_xdata(x_ind)
                self.line_rsi.set_ydata(indicators_filtered["RSI"])
                self.line_macd.set_xdata(x_ind)
                self.line_macd.set_ydata(indicators_filtered["MACD"])
                self.line_signal.set_xdata(x_ind)
                self.line_signal.set_ydata(indicators_filtered["Signal"])
                
                self.ax_rsi.set_xlim(plot_timestamps[0], plot_timestamps[-1])
                self.ax_macd.set_xlim(plot_timestamps[0], plot_timestamps[-1])
            else:
                self.text_message.set_text("Aguardando dados suficientes para calcular indicadores...")
        
        # Recalcula os limites dos eixos e atualiza a figura
        self.ax_price.relim()
        self.ax_price.autoscale_view()
        self.ax_rsi.relim()
        self.ax_rsi.autoscale_view()
        self.ax_macd.relim()
        self.ax_macd.autoscale_view()
        plt.draw()
        plt.pause(0.1)