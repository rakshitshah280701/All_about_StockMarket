from pandas_datareader import data
from datetime import datetime
from datetime import timedelta
from bokeh.io import show, output_notebook, export_svgs, output_file, save
from bokeh.plotting import figure
from bokeh.io import curdoc
from bokeh.io import export_png
from pandas_datareader import data as pdr

import os

rootPath = os.path.abspath(os.path.dirname(__file__))
staticPath = os.path.join(rootPath, 'static')

now = datetime.now()
end = now.date()
start = end+timedelta(days=-365)


def stockReader(stock, start=start, end=end):
    return pdr.get_data_yahoo(stock, start=start, end=end)


def generate_html(nameinput: str):
    curdoc().clear

    stocksymbol = nameinput+".NS"

    now = datetime.now()
    end = now.date()
    start = end+timedelta(days=-365)
    print(end)
    print(start)
    df = stockReader(stocksymbol, start=start, end=end)

    # to make graphs, we need bokeh
    from bokeh.plotting import figure, show, output_file

    def inc_dec(c, o):
        if c > o:
            value = "Increase"
        elif c < o:
            value = "Decrease"
        else:
            value = "No Change"
        return value
    # making new column to store status

    df["Status"] = [inc_dec(c, o) for c, o in zip(df.Close, df.Open)]

    df["Middle"] = (df.Open+df.Close)/2
    df["Height"] = abs(df.Close-df.Open)

    hours_12 = 12*60*60*1000

    # to create the actual figure
    # responsive=true so chart fits the page
    p = figure(x_axis_type="datetime", width=1000,
               height=300, sizing_mode='scale_width')
    p.title.text = f"Candlestick Chart for {nameinput}"

    # to reduce opacity
    p.grid.grid_line_alpha = 0.4

    # for segment
    p.segment(df.index, df.Low, df.index, df.High, line_color="black")
    # for rectangles
    p.rect(df.index[df.Status == "Increase"], df.Middle[df.Status == "Increase"], hours_12,
           df.Height[df.Status == "Increase"], fill_color="#33CC66", line_color="black")
    p.rect(df.index[df.Status == "Decrease"], df.Middle[df.Status == "Decrease"], hours_12,
           df.Height[df.Status == "Decrease"], fill_color="#FF3333", line_color="black")
    # output_notebook()
    output_file(os.path.join(staticPath, 'generate_candlestick.html'))
    save(p)

    # print()
    output_file(os.path.join(rootPath, 'temp.html'))
    print("done ---:)")


def CandleStick(company: str):
    try:
        generate_html(company)
    except Exception as e:
        generate_html('TCS')


if __name__ == '__main__':
    print(CandleStick("ONGC"))

    # print(stockReader('ONGC'))
