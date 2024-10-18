from pyecharts import options as opts
from pyecharts.charts import Geo
from pyecharts.faker import Faker
from pyecharts.commons.utils import JsCode
from pyecharts.globals import ChartType, SymbolType
import numpy as np
import pandas as pd

path = 'D:/OneDrive/Jupyter_Cloud/MAP/'

Airplane_city = pd.read_csv(path + 'Airplane_city.csv')
Airplane_route = pd.read_csv(path + 'Airplane_route.csv')
Airplane_airport = pd.read_csv(path + 'Airplane_airport.csv')

def Airline_search(Airport_list, Route_list):
    MAP = (
        Geo(init_opts=opts.InitOpts(
            width="800px", 
            height="600px"))
        .add_coordinate("芒市", 98.38210533, 24.37681138)
        .add_schema(maptype="china",
                    itemstyle_opts=opts.ItemStyleOpts(color="rgba(50, 60, 72, 0.85)", border_color="#111"))
        .add(
            "",
            Airport_list,
            type_=ChartType.EFFECT_SCATTER,
            color="green",
        )
        .add(
            "Airline",
            Route_list,
            type_=ChartType.LINES,
            effect_opts=opts.EffectOpts(
                symbol=SymbolType.ARROW, symbol_size=6, color="blue"
            ),
            linestyle_opts=opts.LineStyleOpts(curve=0.2),
        )
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
        .set_global_opts(title_opts=opts.TitleOpts(title=""))
    )
    return MAP

# begin_city = "北京"
# end_city = "深圳"

def Find_airport(city):
    airport_name = Airplane_airport[Airplane_airport['city'] == city]['airport'].values
    return '/'.join(airport_name)

def Create_Airport_list(city, route_list, type):
    # 1: begin city, 0: end city
    Num_list = [(city, Find_airport(city))]
    for route in route_list:
        route_turple = (route[type], Find_airport(route[type]))
        Num_list.append(route_turple)
    return Num_list

def Display_Airline(begin_city, end_city):
    c = None
    if begin_city and end_city:
        Airline_Num = len(
            Airplane_route[
                (Airplane_route["departure_city"] == begin_city)
                & (Airplane_route["landing_city"] == end_city)
            ]
        )
        begin_airport = Find_airport(begin_city)
        end_airport = Find_airport(end_city)
        if Airline_Num:
            c = Airline_search([(begin_city, begin_airport), 
                                (end_city, end_airport)], 
                                [(begin_city, end_city)])
        else:
            print("No such route from {} to {}".format(begin_city, end_city))
    else:
        if begin_city == 0 and end_city != 0:
            Route_list = (
                Airplane_route[Airplane_route["landing_city"] == end_city]
                .to_records(index=False)
                .tolist()
            )
            Airport_list = Create_Airport_list(end_city, Route_list, 0)
            c = Airline_search(Airport_list, Route_list)
        elif end_city == 0 and begin_city != 0:
            Route_list = (
                Airplane_route[Airplane_route["departure_city"] == begin_city]
                .to_records(index=False)
                .tolist()
            )
            Airport_list = Create_Airport_list(begin_city, Route_list, 1)
            c = Airline_search(Airport_list, Route_list)
        elif begin_city == 0 and end_city == 0: # All routes
            print("Input error!")
    return c

if __name__ == '__main__':
    MAP = Display_Airline("黑龙江", "深圳")
    print(MAP)