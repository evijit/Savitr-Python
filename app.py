import dash
from dash.dependencies import Input, Output, State, Event
import dash_core_components as dcc
import dash_html_components as html
import plotly.plotly as py
from plotly import graph_objs as go
from plotly.graph_objs import *
from flask import Flask
import pandas as pd
import numpy as np
import os

server = Flask('my app')
server.secret_key = os.environ.get('secret_key', 'secret')

app = dash.Dash('SavitrApp', server=server, url_base_pathname='/', csrf_protect=False)

if 'DYNO' in os.environ:
    app.scripts.append_script({
        'external_url': 'https://cdn.rawgit.com/chriddyp/ca0d8f02a1659981a0ea7f013a378bbd/raw/e79f3f789517deec58f41251f7dbb6bee72c44ab/plotly_ga.js'
    })


mapbox_access_token = 'pk.eyJ1IjoiYWxpc2hvYmVpcmkiLCJhIjoiY2ozYnM3YTUxMDAxeDMzcGNjbmZyMmplZiJ9.ZjmQ0C2MNs1AzEBC_Syadg'


def initialize():
    ##df = pd.read_csv('https://www.dropbox.com/s/vxe7623o7eqbe6n/output.csv?dl=1')
    # df = pd.read_csv('data/output.csv')
    # df.drop("Unnamed: 0", 1, inplace=True)
    # df["Date/Time"] = pd.to_datetime(df["Date/Time"], format="%Y-%m-%d %H:%M:%S")
    # df.index = df["Date/Time"]
    # df.drop("Date/Time", 1, inplace=True)
    # df.drop("Base", 1, inplace=True)
    df = pd.read_csv('data/tweets.csv')
    df.rename(columns={'cr/$date':'date', 'tlt':'Lat', 'tln':'Lon'}, inplace = True)
    df["date"] = pd.to_datetime(df["date"], format="%Y-%m-%d %H:%M:%S")
    df.index = df["date"]
    df.drop(['_id', 'plt','date', 'pln', 'acr/$date', 'uid', 'p', 'f'], axis=1, inplace=True)
    totalList = []
    for month in df.groupby(df.index.month):
        dailyList = []
        for day in month[1].groupby(month[1].index.day):
            dailyList.append(day[1])
        totalList.append(dailyList)
    return totalList


app.layout = html.Div([
    html.Div([
        html.Div([
            html.P(id='total-rides', className="totalRides"),
            html.P(id='total-rides-selection', className="totalRideSelection"),
            html.P(id='date-value', className="dateValue"),
            dcc.Dropdown(
                    id='search-bar',
                    options=[
                        {'label': 'Flood', 'value': '0'},
                        {'label': 'Dengue', 'value': '1'}
                    ],
                    multi=True,
                    placeholder="Choose Situation",
                    className="bars"
                ),
            html.Div([
                html.Div([
                    html.H2("Savitr", style={'font-family': 'Dosis'}),
                    # html.Img(src="https://s3-us-west-1.amazonaws.com/plotly-tutorials/logo/new-branding/dash-logo-by-plotly-stripe.png",
                    #         style={
                    #             'height': '100px',
                    #             'float': 'right',
                    #             'position': 'relative',
                    #             'bottom': '145px',
                    #             'left': '5px'
                    #         },
                    # ),
                ]),
                html.P("Disaster mapping using Twitter", className="explanationParagraph twelve columns"),
                dcc.Graph(id='map-graph'),
            dcc.Dropdown(
                id='my-dropdown',
                options=[
                    {'label': 'Sept 2017', 'value': 'Sept'},
                    {'label': 'Oct 2017', 'value': 'Oct'}
                ],
                value="Sept",
                placeholder="Please choose a month",
                className="month-picker"
            ),
            
                dcc.Dropdown(
                    id='bar-selector',
                    options=[
                        {'label': '0:00', 'value': '0'},
                        {'label': '1:00', 'value': '1'},
                        {'label': '2:00', 'value': '2'},
                        {'label': '3:00', 'value': '3'},
                        {'label': '4:00', 'value': '4'},
                        {'label': '5:00', 'value': '5'},
                        {'label': '6:00', 'value': '6'},
                        {'label': '7:00', 'value': '7'},
                        {'label': '8:00', 'value': '8'},
                        {'label': '9:00', 'value': '9'},
                        {'label': '10:00', 'value': '10'},
                        {'label': '11:00', 'value': '11'},
                        {'label': '12:00', 'value': '12'},
                        {'label': '13:00', 'value': '13'},
                        {'label': '14:00', 'value': '14'},
                        {'label': '15:00', 'value': '15'},
                        {'label': '16:00', 'value': '16'},
                        {'label': '17:00', 'value': '17'},
                        {'label': '18:00', 'value': '18'},
                        {'label': '19:00', 'value': '19'},
                        {'label': '20:00', 'value': '20'},
                        {'label': '21:00', 'value': '21'},
                        {'label': '22:00', 'value': '22'},
                        {'label': '23:00', 'value': '23'}
                    ],
                    multi=True,
                    placeholder="Select certain hours using \
                                 the box-select/lasso tool or \
                                 using the dropdown menu",
                    className="bars"
                ),
                dcc.Graph(id="histogram"),
                html.P("", id="popupAnnotation", className="popupAnnotation"),
            ], className="graph twelve coluns"),
        ], style={'margin': 'auto auto'}),
        dcc.Slider(
            id="my-slider",
            min=1,
            step=1,
            value=1
        ),
        # dcc.Markdown("Source: [FiveThirtyEight](https://github.com/fivethirtyeight/uber-tlc-foil-response/tree/master/uber-trip-data)",
        #              className="source"),
        # dcc.Checklist(
        #     id="mapControls",
        #     options=[
        #         {'label': 'Lock Camera', 'value': 'lock'}
        #     ],
        #     values=[''],
        #     labelClassName="mapControls",
        #     inputStyle={"z-index": "3"}
        # ),
    ], className="graphSlider ten columns offset-by-one"),
], style={"padding-top": "20px"})


def getValue(value):
    val = {
        'Sept': 30,
        'Oct': 13
    }[value]
    return val

def getValue_start(value):
    val = {
        'Sept': 12,
        'Oct': 1
    }[value]
    return val


def getIndex(value):
    if(value==None):
        return 0
    val = {
        'Sept': 0,
        'Oct': 1
    }[value]
    return val

def getClickIndex(value):
    if(value==None):
        return 0
    return value['points'][0]['x']


@app.callback(Output("my-slider", "marks"),
              [Input("my-dropdown", "value")])
def update_slider_ticks(value):
    marks = {}
    for i in range(getValue_start(value), getValue(value)+1, 1):
        if(i is getValue_start(value) or i is getValue(value)):
            marks.update({i-getValue_start(value)+1: '{} {}'.format(value, i)})
        else:
            marks.update({i-getValue_start(value)+1: '{}'.format(i)})
    return marks


@app.callback(Output("my-slider", "max"),
              [Input("my-dropdown", "value")])
def update_slider_max(value):
    return getValue(value) - getValue_start(value) + 1


@app.callback(Output("bar-selector", "value"),
              [Input("histogram", "selectedData")])
def update_bar_selector(value):
    holder = []
    if(value is None or len(value) is 0):
        return holder
    for x in value['points']:
        holder.append(str(int(x['x'])))
    return holder


@app.callback(Output("total-rides", "children"),
              [Input("my-dropdown", "value"), Input('my-slider', 'value')])
def update_total_rides(value, slider_value):
    return ("Total # of tweets: {:,d}"
            .format(len(totalList[getIndex(value)][slider_value-1])))


@app.callback(Output("total-rides-selection", "children"),
              [Input("my-dropdown", "value"), Input('my-slider', 'value'),
               Input('bar-selector', 'value')])
def update_total_rides_selection(value, slider_value, selection):
    if(selection is None or len(selection) is 0):
        return ""
    totalInSelction = 0
    for x in selection:
        totalInSelction += len(totalList[getIndex(value)]
                                        [slider_value-1]
                                        [totalList[getIndex(value)]
                                                [slider_value-1].index.hour == int(x)])
    return ("Total tweets in selection: {:,d}"
            .format(totalInSelction))


@app.callback(Output("date-value", "children"),
              [Input("my-dropdown", "value"), Input('my-slider', 'value'),
               Input("bar-selector", "value")])
def update_date(value, slider_value, selection):
    holder = []
    if(value is None or selection is None or len(selection) is 24
       or len(selection) is 0):
        return (value, " ", slider_value, " - showing: All")

    for x in selection:
        holder.append(int(x))
    holder.sort()

    if(holder[len(holder)-1]-holder[0]+2 == len(holder)+1 and len(holder) > 2):
        return (value, " ", slider_value, " - showing hour(s): ",
                holder[0], "-", holder[len(holder)-1])

    x = ""
    for h in holder:
        if(holder.index(h) == (len(holder)-1)):
            x += str(h)
        else:
            x += str(h) + ", "
    return (value, " ", slider_value, " - showing hour(s): ", x)


@app.callback(Output("histogram", "selectedData"),
              [Input("my-dropdown", "value")])
def clear_selection(value):
    if(value is None or len(value) is 0):
        return None

@app.callback(Output("popupAnnotation", "children"),
              [Input("bar-selector", "value")])
def clear_selection(value):
    if(value is None or len(value) is 0):
        return "Select any of the bars to section data by time"
    else:
        return ""


def get_selection(value, slider_value, selection):
    xVal = []
    yVal = []
    xSelected = []

    colorVal = ["#F4EC15", "#DAF017", "#BBEC19", "#9DE81B", "#80E41D", "#66E01F",
                "#4CDC20", "#34D822", "#24D249", "#25D042", "#26CC58", "#28C86D",
                "#29C481", "#2AC093", "#2BBCA4", "#2BB5B8", "#2C99B4", "#2D7EB0",
                "#2D65AC", "#2E4EA4", "#2E38A4", "#3B2FA0", "#4E2F9C", "#603099"]

    if(selection is not None):
        for x in selection:
            xSelected.append(int(x))
    for i in range(0, 24, 1):
        if i in xSelected and len(xSelected) < 24:
            colorVal[i] = ('#FFFFFF')
        xVal.append(i)
        yVal.append(len(totalList[getIndex(value)][slider_value-1]
                    [totalList[getIndex(value)][slider_value-1].index.hour == i]))

    return [np.array(xVal), np.array(yVal), np.array(xSelected),
            np.array(colorVal)]



@app.callback(Output("histogram", "figure"),
              [Input("my-dropdown", "value"), Input('my-slider', 'value'),
               Input("bar-selector", "value")])
def update_histogram(value, slider_value, selection):

    [xVal, yVal, xSelected, colorVal] = get_selection(value, slider_value,
                                                      selection)

    layout = go.Layout(
        bargap=0.01,
        bargroupgap=0,
        barmode='group',
        margin=Margin(l=10, r=0, t=0, b=30),
        showlegend=False,
        plot_bgcolor='#ffffff',
        paper_bgcolor='rgb(66, 134, 244, 0)',
        height=250,
        dragmode="select",
        xaxis=dict(
            range=[-0.5, 23.5],
            showgrid=False,
            nticks=25,
            fixedrange=True,
            ticksuffix=":00"
        ),
        yaxis=dict(
            range=[0, max(yVal)+max(yVal)/4],
            showticklabels=False,
            showgrid=False,
            fixedrange=True,
            rangemode='nonnegative',
            zeroline='hidden'
        ),
        annotations=[
            dict(x=xi, y=yi,
                 text=str(yi),
                 xanchor='center',
                 yanchor='bottom',
                 showarrow=False,
                 font=dict(
                    color='black'
                 ),
                 ) for xi, yi in zip(xVal, yVal)],
    )

    return go.Figure(
           data=Data([
                go.Bar(
                    x=xVal,
                    y=yVal,
                    marker=dict(
                        color=colorVal
                    ),
                    hoverinfo="x"
                ),
                go.Scatter(
                    opacity=0,
                    x=xVal,
                    y=yVal/2,
                    hoverinfo="none",
                    mode='markers',
                    marker=Marker(
                        color='rgb(66, 134, 244, 0)',
                        symbol="square",
                        size=40
                    ),
                    visible=True
                )
            ]), layout=layout)


def get_lat_lon_color(selectedData, value, slider_value, searchBarInput):
    listStr = "totalList[getIndex(value)][slider_value-1]"
    if(selectedData is None or len(selectedData) is 0):
        return listStr
    elif(int(selectedData[len(selectedData)-1])-int(selectedData[0])+2 == len(selectedData)+1 and len(selectedData) > 2):
        listStr += "[(totalList[getIndex(value)][slider_value-1].index.hour>"+str(int(selectedData[0]))+") & \
                    (totalList[getIndex(value)][slider_value-1].index.hour<" + str(int(selectedData[len(selectedData)-1]))+")]"
    else:
        listStr += "["
        for point in selectedData:
            if (selectedData.index(point) is not len(selectedData)-1):
                listStr += "(totalList[getIndex(value)][slider_value-1].index.hour==" + str(int(point)) + ") | "
            else:
                listStr += "(totalList[getIndex(value)][slider_value-1].index.hour==" + str(int(point)) + ")]"

    return listStr


@app.callback(Output("map-graph", "figure"),
              [Input("my-dropdown", "value"), Input('my-slider', 'value'),
              Input("bar-selector", "value"), Input("search-bar", "value")],
              [State('map-graph', 'relayoutData')])
def update_graph(value, slider_value, selectedData, searchBarInput, prevLayout):
    mapControls = None
    zoom = 4.0
    latInitial = 21.146633
    lonInitial = 79.088860
    bearing = 0
    listStr = get_lat_lon_color(selectedData, value, slider_value, searchBarInput)

    listsOfStr = eval(listStr)['t'].tolist()
    new_list = []
    listStr_lat = eval(listStr)['Lat'].tolist()
    new_lat = []
    listStr_lon = eval(listStr)['Lon'].tolist()
    new_lon = []
    listStr_index = eval(listStr).index.hour
    to_del = []
    if (not searchBarInput):
        new_list = listsOfStr
        new_lon = listStr_lon
        new_lat = listStr_lat
    elif (len(searchBarInput) == 2):
        new_list = listsOfStr
        new_lon = listStr_lon
        new_lat = listStr_lat
    elif (searchBarInput[0] == '0'):
        for i in range(len(listsOfStr)):
            a = listsOfStr[i]
            if "flood" in a.lower():
                new_list.append(a)
                new_lat.append(listStr_lat[i])
                new_lon.append(listStr_lon[i])
            else:
                to_del.append(i)
        # toSearch = "flood"
    elif (searchBarInput[0] == '1'):
        for i in range(len(listsOfStr)):
            a = listsOfStr[i]
            if "dengue" in a.lower():
                new_list.append(a)
                new_lat.append(listStr_lat[i])
                new_lon.append(listStr_lon[i])
            else:
                to_del.append(i)
        # toSearch = "dengue"
    if(len(to_del) > 0):
        np.delete(listStr_index, to_del, axis=0)
    if(prevLayout is not None and mapControls is not None and
       'lock' in mapControls):
        zoom = float(prevLayout['mapbox']['zoom'])
        latInitial = float(prevLayout['mapbox']['center']['lat'])
        lonInitial = float(prevLayout['mapbox']['center']['lon'])
        bearing = float(prevLayout['mapbox']['bearing'])
    return go.Figure(
        data=Data([
            Scattermapbox(
                lat=new_lat,
                lon=new_lon,
                mode='markers',
                hoverinfo="text",
                text=new_list,
                marker=Marker(
                    color=np.append(np.insert(listStr_index, 0, 0), 23),
                    colorscale=[[0, "#F4EC15"], [0.04167, "#DAF017"],
                                [0.0833, "#BBEC19"], [0.125, "9DE81B"],
                                [0.1667, "#80E41D"], [0.2083, "#66E01F"],
                                [0.25, "#4CDC20"], [0.292, "#34D822"],
                                [0.333, "#24D249"], [0.375, "#25D042"],
                                [0.4167, "#26CC58"], [0.4583, "#28C86D"],
                                [0.50, "#29C481"], [0.54167, "#2AC093"],
                                [0.5833, "#2BBCA4"],
                                [1.0, "#613099"]],
                    opacity=0.5,
                    size=15,
                    colorbar=dict(
                        thicknessmode="fraction",
                        title="Time of<br>Day",
                        x=0.935,
                        xpad=0,
                        nticks=24,
                        tickfont=dict(
                            color='black'
                        ),
                        titlefont=dict(
                            color='black'
                        ),
                        titleside='left'
                        )
                ),
            ),
        ]),
        layout=Layout(
            autosize=True,
            height=750,
            margin=Margin(l=0, r=0, t=0, b=0),
            showlegend=False,
            mapbox=dict(
                accesstoken=mapbox_access_token,
                center=dict(
                    lat=latInitial, # 40.7272
                    lon=lonInitial # -73.991251
                ),
                style='light',
                bearing=bearing,
                zoom=zoom
            ),
            updatemenus=[
                dict(
                    buttons=([
                        dict(
                            args=[{
                                    'mapbox.zoom': 4,
                                    'mapbox.center.lon': '79.088860',
                                    'mapbox.center.lat': '21.146633',
                                    'mapbox.bearing': 0,
                                    'mapbox.style': 'light'
                                }],
                            label='Reset Zoom',
                            method='relayout'
                        )
                    ]),
                    direction='left',
                    pad={'r': 0, 't': 0, 'b': 0, 'l': 0},
                    showactive=False,
                    type='buttons',
                    x=0.45,
                    xanchor='left',
                    yanchor='bottom',
                    bgcolor='white',
                    borderwidth=1,
                    bordercolor="#6d6d6d",
                    font=dict(
                        color="black"
                    ),
                    y=0.02
                ),
                #dict(
                    # buttons=([
                    #     dict(
                    #         args=[{
                    #                 'mapbox.zoom': 15,
                    #                 'mapbox.center.lon': '-73.9934',
                    #                 'mapbox.center.lat': '40.7505',
                    #                 'mapbox.bearing': 0,
                    #                 'mapbox.style': 'dark'
                    #             }],
                    #         label='Madison Square Garden',
                    #         method='relayout'
                    #     ),
                    #     dict(
                    #         args=[{
                    #                 'mapbox.zoom': 15,
                    #                 'mapbox.center.lon': '-73.9262',
                    #                 'mapbox.center.lat': '40.8296',
                    #                 'mapbox.bearing': 0,
                    #                 'mapbox.style': 'dark'
                    #             }],
                    #         label='Yankee Stadium',
                    #         method='relayout'
                    #     ),
                    #     dict(
                    #         args=[{
                    #                 'mapbox.zoom': 15,
                    #                 'mapbox.center.lon': '-73.9857',
                    #                 'mapbox.center.lat': '40.7484',
                    #                 'mapbox.bearing': 0,
                    #                 'mapbox.style': 'dark'
                    #             }],
                    #         label='Empire State Building',
                    #         method='relayout'
                    #     ),
                    #     dict(
                    #         args=[{
                    #                 'mapbox.zoom': 15,
                    #                 'mapbox.center.lon': '-74.0113',
                    #                 'mapbox.center.lat': '40.7069',
                    #                 'mapbox.bearing': 0,
                    #                 'mapbox.style': 'dark'
                    #             }],
                    #         label='New York Stock Exchange',
                    #         method='relayout'
                    #     ),
                    #     dict(
                    #         args=[{
                    #                 'mapbox.zoom': 15,
                    #                 'mapbox.center.lon': '-73.785607',
                    #                 'mapbox.center.lat': '40.644987',
                    #                 'mapbox.bearing': 0,
                    #                 'mapbox.style': 'dark'
                    #             }],
                    #         label='JFK Airport',
                    #         method='relayout'
                    #     ),
                    #     dict(
                    #         args=[{
                    #                 'mapbox.zoom': 15,
                    #                 'mapbox.center.lon': '-73.9772',
                    #                 'mapbox.center.lat': '40.7527',
                    #                 'mapbox.bearing': 0,
                    #                 'mapbox.style': 'dark'
                    #             }],
                    #         label='Grand Central Station',
                    #         method='relayout'
                    #     ),
                    #     dict(
                    #         args=[{
                    #                 'mapbox.zoom': 15,
                    #                 'mapbox.center.lon': '-73.9851',
                    #                 'mapbox.center.lat': '40.7589',
                    #                 'mapbox.bearing': 0,
                    #                 'mapbox.style': 'dark'
                    #             }],
                    #         label='Times Square',
                    #         method='relayout'
                    #     )
                    # ]),
                #     direction="down",
                #     pad={'r': 0, 't': 0, 'b': 0, 'l': 0},
                #     showactive=False,
                #     bgcolor="rgb(50, 49, 48, 0)",
                #     type='buttons',
                #     yanchor='bottom',
                #     xanchor='left',
                #     font=dict(
                #         color="#FFFFFF"
                #     ),
                #     x=0,
                #     y=0.05
                # )
            ]
        )
    )


external_css = ["https://cdnjs.cloudflare.com/ajax/libs/skeleton/2.0.4/skeleton.min.css",
                "//fonts.googleapis.com/css?family=Raleway:400,300,600",
                "//fonts.googleapis.com/css?family=Dosis:Medium",
                "https://cdn.rawgit.com/plotly/dash-app-stylesheets/62f0eb4f1fadbefea64b2404493079bf848974e8/dash-uber-ride-demo.css",
                "https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css"]


for css in external_css:
    app.css.append_css({"external_url": css})


@app.server.before_first_request
def defineTotalList():
    global totalList
    totalList = initialize()


if __name__ == '__main__':
    app.run_server(debug=True)
