# trend_indicator.py
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

def determine_trend(indicators):
    """
    Determina a tendência usando uma heurística simples:
      - Uptrend se:
          - EMA > MA (20)
          - MACD > Signal
          - RSI > 50
          - MA75 > MA150
        (Se pelo menos 3 desses 4 critérios forem atendidos, define como uptrend)
      - Caso contrário, downtrend.
    
    Parâmetro:
        indicators (DataFrame): DataFrame com as colunas "MA" (20), "MA75", "MA150", 
                                 "EMA", "RSI", "MACD" e "Signal".
    
    Retorna:
        str: 'up' ou 'down'
    """
    last = indicators.iloc[-1]
    up_conditions = 0
    if last['EMA'] > last['MA']:
        up_conditions += 1
    if last['MACD'] > last['Signal']:
        up_conditions += 1
    if last['RSI'] > 50:
        up_conditions += 1
    if last['MA75'] > last['MA150']:
        up_conditions += 1

    return 'up' if up_conditions >= 3 else 'down'

def draw_trend_circle(ax, trend):
    """
    Desenha um círculo no eixo fornecido com a cor baseada na tendência.
    
    Parâmetros:
        ax: Objeto de eixo do matplotlib onde o círculo será desenhado.
        trend (str): 'up' para tendência de alta ou 'down' para tendência de baixa.
    """
    ax.clear()
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    
    color = 'green' if trend == 'up' else 'red'
    # O círculo é desenhado com centro (0.1,0.1) e raio 2 (os parâmetros podem ser ajustados conforme necessário)
    circle = Circle((0.1, 0.1), 2, color=color)
    ax.add_patch(circle)
    ax.text(0.5, 0.7, f"{trend.upper()} TREND", horizontalalignment='center', 
            verticalalignment='top', color='white', fontsize=12)
    plt.draw()

class TrendIndicator:
    def __init__(self, ax):
        """
        Inicializa o indicador de tendência com o eixo do matplotlib onde será desenhado.
        """
        self.ax = ax

    def update(self, indicators):
        """
        Atualiza o indicador de tendência com base no DataFrame de indicadores.
        
        Parâmetro:
            indicators (DataFrame): DataFrame retornado pela função de cálculo dos indicadores.
        """
        if indicators is None:
            return
        trend = determine_trend(indicators)
        draw_trend_circle(self.ax, trend)
