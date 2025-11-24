# time_series_visualizer.py
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Importar y preparar datos (no modificar nombre del archivo)
df = pd.read_csv("fcc-forum-pageviews.csv", index_col='date', parse_dates=True)

# Limpiar datos: eliminar el 2.5% inferior y superior por 'value'
df = df[(df['value'] >= df['value'].quantile(0.025)) &
        (df['value'] <= df['value'].quantile(0.975))]


def draw_line_plot():
    """
    Dibuja y devuelve la figura del gráfico de líneas solicitado.
    Título: "Daily freeCodeCamp Forum Page Views 5/2016-12/2019"
    Ejes: x -> Date, y -> Page Views
    Guarda la figura en 'line_plot.png' y devuelve fig.
    """
    # Usar una copia del DataFrame
    data = df.copy()

    # Crear figura
    fig, ax = plt.subplots(figsize=(16, 6))

    ax.plot(data.index, data['value'], color='red', linewidth=1)
    ax.set_title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019")
    ax.set_xlabel("Date")
    ax.set_ylabel("Page Views")

    # Guardar y devolver
    fig.tight_layout()
    fig.savefig("line_plot.png")
    return fig


def draw_bar_plot():
    """
    Dibuja y devuelve la figura del gráfico de barras:
    - promedio mensual por año (años en x, barras apiladas por mes)
    - guarda en 'bar_plot.png'
    """
    # Copia del dataframe
    data = df.copy()

    # Preparar columnas year y month (nombre abreviado)
    data['year'] = data.index.year
    data['month'] = data.index.month_name()

    # Calcular promedio por year-month
    df_grouped = data.groupby(['year', 'month'])['value'].mean().reset_index()

    # Asegurar orden de meses: Jan..Dec
    month_order = ["January", "February", "March", "April", "May", "June",
                   "July", "August", "September", "October", "November", "December"]
    df_grouped['month'] = pd.Categorical(df_grouped['month'], categories=month_order, ordered=True)

    # Pivot para tener años en índices y meses en columnas
    df_pivot = df_grouped.pivot(index='year', columns='month', values='value')

    # Dibujar
    fig = df_pivot.plot(kind='bar', figsize=(12, 8)).figure

    plt.xlabel("Years")
    plt.ylabel("Average Page Views")
    plt.legend(title="Months")
    plt.tight_layout()
    fig.savefig("bar_plot.png")
    return fig


def draw_box_plot():
    """
    Dibuja y devuelve una figura con dos box plots uno al lado del otro:
    - Year-wise Box Plot (Trend) -> Año en x, Page Views en y
    - Month-wise Box Plot (Seasonality) -> Mes (Jan..Dec) en x, Page Views en y
    Guarda en 'box_plot.png' y devuelve fig.
    """
    # Copia y preparación
    data = df.copy()
    data = data.reset_index()
    data['year'] = data['date'].dt.year
    data['month_num'] = data['date'].dt.month
    data['month'] = data['date'].dt.strftime('%b')  # Jan, Feb, ...

    # Asegurar orden de meses para el boxplot
    month_order = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']

    # Crear figura con 2 subplots
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))

    # Year-wise box plot (trend)
    sns.boxplot(x='year', y='value', data=data, ax=axes[0])
    axes[0].set_title("Year-wise Box Plot (Trend)")
    axes[0].set_xlabel("Year")
    axes[0].set_ylabel("Page Views")

    # Month-wise box plot (seasonality)
    sns.boxplot(x='month', y='value', data=data, order=month_order, ax=axes[1])
    axes[1].set_title("Month-wise Box Plot (Seasonality)")
    axes[1].set_xlabel("Month")
    axes[1].set_ylabel("Page Views")

    plt.tight_layout()
    fig.savefig("box_plot.png")
    return fig
