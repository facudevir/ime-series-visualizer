# main.py
from time_series_visualizer import draw_line_plot, draw_bar_plot, draw_box_plot

if __name__ == "__main__":
    fig1 = draw_line_plot()
    print("Saved line_plot.png")
    fig2 = draw_bar_plot()
    print("Saved bar_plot.png")
    fig3 = draw_box_plot()
    print("Saved box_plot.png")
