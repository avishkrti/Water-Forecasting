import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
from app import app, cache


###prediction data
#pr1 = pd.read_csv('df.csv')
pr2 = pd.read_csv('data/predicted.csv')

###Rain-data
rain_data = pd.read_csv("data/rain_data.csv")
rain_data = rain_data.drop(['Mysore','Kodagu','Hassan'],axis = 1)

###Graph-1
df = pd.read_csv('data/KRS.csv', parse_dates=['FLOW_DATE'])
df2=df
df = df.drop(['SL_NO','RESERVOIR','YEAR','WEEK_NO','UNIQUE_KEY'],axis=1)
df['RES_LEVEL_FT'] = pd.to_numeric(df['RES_LEVEL_FT'],errors = 'coerce')
df['INFLOW_CUSECS'] = pd.to_numeric(df['INFLOW_CUSECS'],errors = 'coerce')
df['OUTFLOW_CUECS'] = pd.to_numeric(df['OUTFLOW_CUECS'],errors = 'coerce')
df['Date'] = df['FLOW_DATE']
df['Date'] = pd.to_datetime(df['Date'], format='%m')
df = df.set_index(['FLOW_DATE'])



def heat_map():
    df['year'] = df['Date'].dt.year
    df['month'] = df['Date'].dt.month
    krs_pivot = df.pivot_table(index = df['year'], columns = df['month'], values = 'RES_LEVEL_FT') 
    krs_pivot = krs_pivot.fillna(0)  
    fig = px.imshow(krs_pivot)

    fig.update_layout(
        title="Monthwise reservoir level",
        title_x=0.5,
        # hovertemplate='Month: %{x}'+'<br>Year: %{text:.2f}', 
        xaxis_title="Month",
        yaxis_title="Year",
        plot_bgcolor='#FFFFFF',
        #paper_bgcolor='#D3D3D3',
        #hovermode="x unified",
        font=dict(
            #family="Courier New, monospace",
            size=10,
            color="#000000"
            
        )
    )
    return fig

###Graph-2
def line_chart():
    fig = go.Figure()   
    fig.add_scatter(y=df['INFLOW_CUSECS'], x=df['Date'], mode='lines',hovertemplate='Date: %{x}'+'<br>INFLOW_CUSECS: %{y}', name = "inflow")
    fig.add_scatter(y=df['OUTFLOW_CUECS'], x=df['Date'], mode='lines',hovertemplate='Date: %{x}'+'<br>OUTFLOW_CUECS: %{y}', name="outflow")
    fig.update_layout(
        title="Inflow in 10 years v/s outflow in 10 years",
        xaxis_title="Year",
        yaxis_title="Flow",
        plot_bgcolor='#FFFFFF',
        # paper_bgcolor='#D3D3D3',
        #hovermode="x unified",
        font=dict(
            #family="Courier New, monospace",
            size=10,
            color="#000000"
            
        )
    )
    return fig
###Graph-3
def bar_chart():
    df['year'] = df['Date'].dt.year
    df3 = df.groupby('year').last().reset_index()
    df3['RES_DIFF'] = df3['RES_LEVEL_FT'].diff()
    df3['RES_DIFF']=df3['RES_DIFF'].fillna(0)
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=df3['year'],
            y=df3['RES_LEVEL_FT'],
            text = df3['RES_DIFF'], # text to show on hover from df column
            marker=dict(color="black", size=12),
            mode = 'lines+markers',
            hovertemplate='Year: %{x}'+'<br>Difference in levels: %{text:.2f}',
            name = "res_diff"

        ))
    fig.add_trace(
        go.Bar(
            x=df3['year'],
            y=df3['RES_LEVEL_FT'],
            hovertemplate='Year: %{x}'+'<br>RES_LEVEL_FT: %{y:.2f}',
            name = "res_lvl"
        ))
    fig.update_layout(
        title="Reservoir level Rise over years",
        xaxis_title="Year",
        yaxis_title="Change",
        #hovermode="x unified",
        plot_bgcolor='#FFFFFF',
        font=dict(
            #family="Courier New, monospace",
            size=10,
            color="#000000"
        )
    )
    return fig
###Graph-4
def bar_line_chart():
    rain_data['Date']= pd.to_datetime(rain_data['Date'])
    rain_data.fillna(0)
    rain_data['year'] = rain_data['Date'].dt.year
    rain_data_1= rain_data.groupby('year')['Mandya'].sum()
    rain_data_1.to_frame()
    rain_data_1.reset_index()
    df['year'] = df['Date'].dt.year
    df4 = df.groupby('year').last().reset_index()
    df4['RES_DIFF'] = df4['RES_LEVEL_FT'].diff()
    df4['RES_DIFF']=df4['RES_DIFF'].fillna(0)
    df4.insert(7, 'Mandya' ,[0,810.82,568.95,893.72,957.83,1005.99,638.41,861.50,1046.75,1295.83,1053.46])
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=df4['year'],
            y=df4['Mandya'],
            text = df4['RES_LEVEL_FT'], # text to show on hover from df column
            marker=dict(color="black", size=6),
            mode = 'lines+markers',
            hovertemplate='Year: %{x}'+'<br>Avg Rainfall: %{y:.2f}',
            name = 'trendline'

        ))
    fig.add_trace(
        go.Bar(
            x=df4['year'],
            y=df4['Mandya'],
            hovertemplate='Year: %{x}'+'<br>Avg Rainfall: %{y:.2f}',
            marker={'color': 'red'},
            name = "rainfall"
        ),
    )
    fig.add_trace(
        go.Bar(
            x=df4['year'],
            y=df4['RES_LEVEL_FT'],
            hovertemplate='Year: %{x}'+'<br>RES_LVL_FT: %{y:.2f}',
            marker={'color': 'green'},
            name = "res_lvl"
    )),
    fig.update_layout(
        plot_bgcolor='#FFFFFF',
        barmode = 'group',
        title="Average Rainfall v/s Reservoir Level",
        xaxis_title="Year",
        yaxis_title="Change",
        #hovermode="x unified",
        font=dict(
            #family="Courier New, monospace",
            size=10,
            color="#000000"
        )
    )
    return fig

###Graph-5
def show_prediction():
    fig = px.line(pr2, x="ds", y="level", color="type")
    fig.update_layout(
        title="Monthwise Reservoir Level",
        title_x=0.5,
        # hovertemplate='Month: %{x}'+'<br>Year: %{text:.2f}', 
        xaxis_title="Date",
        yaxis_title="Reservoir Level",
        plot_bgcolor='#FFFFFF',
        #paper_bgcolor='#D3D3D3',
        #hovermode="x unified",
        font=dict(
            #family="Courier New, monospace",
            size=10,
            color="#000000"
          
        )
    )
    return fig
###Card
simple_card = html.Div(
    [
        html.H1("KRS", style={
    'textAlign': 'center',
    "font-family": "Fredoka One",
    "font-weight": "bold",
    "font-size": "48px",
    "margin-bottom": "35px",
}),
        dbc.Row([dbc.Col(dbc.Card(
        [
            # dbc.CardBody(
            #     [
            #         dcc.Graph(id='indicator-graphic-1', figure = fig
            #       ),
            #         #dbc.Button("Go somewhere", color="primary"),
            #     ]
            # ),
            dbc.CardImg(src="https://raw.githubusercontent.com/avishkrti/Water-Forecasting/main/static/krs_dam.jpeg", style={"height":"30rem","width":"28rem", "border-radius": "50px"}),
        ],
        style={"border-radius": "50px", "box-shadow": "0px 0px 8px 8px #ebe9e8",
                "-webkit-box-shadow": "0px 0px 8px 8px #ebe9e8","height":"30rem", "width": "28rem", "padding":"all"},
    ),), html.Br(), 
    dbc.Col(dbc.Card(
        [
            dbc.CardBody(
                [
                    html.H4("ABOUT KRS", className="card-title", style={"font-weight":"bold","margin-top":"25px", "margin-left":"15px", "margin-bottom":"15px"}),
                    html.P(
                        "KRS or Krishana Raja Sagar Dam is one the most famous dams in South India. "
                        "Initially, it was a project to supply water for drinking and irrigation for Mysore and Mandya. "
                        "Later, it also became the major source of water for the Bengaluru city which grew faster. "
                        "Three rivers namely Kaveri, Hemavathi and Laksmanathirtha meet near the Krishanarajasagar Dam. "
                        "KRS Dam and Reservoir is the only important source of drinking water for the people of Mysore, Mandya and Bengaluru. "
                        "The water from KRS reaches Torekadanahalli and from there water is pumped several feet higher to supply water to Bengaluru.",
                        className="card-text", style={"margin-top":"15px", "margin-left":"20px", "margin-right":"20px", "text-align":"justify"}
                    ),
                    #dbc.Button("Go somewhere", color="primary"),
                ]
            ),
        ],
        style={"border-radius": "50px", "box-shadow": "0px 0px 8px 8px #ffe4d4",
                "-webkit-box-shadow": "0px 0px 8px 8px #ffe4d4","height":"25rem", "width": "35rem","padding":"all",
                "margin-top":"40px", "background":"linear-gradient(135deg, #f64074 0%,#fdab0d 100%)","color":"white"},
    ),)], justify="around"),
    html.Br(),
    dbc.Row([dbc.Col(dbc.Card(
        [
            dbc.CardBody(
                [
                    dcc.Graph(id='indicator-graphic-1',figure = bar_chart(), config={
        "displaylogo": False,
    },
                  ),
                    #dbc.Button("Go somewhere", color="primary"),
                ]
            ),
        ],
        style={"border-radius": "50px", "box-shadow": "0px 0px 8px 8px #ebe9e8",
                "-webkit-box-shadow": "0px 0px 8px 8px #ebe9e8","height":"30rem", 
                "width": "32rem", "padding":"all", "margin-top":"40px"},
    ),), html.Br(),
    dbc.Col(dbc.Card(
        [
            dbc.CardBody(
                [
                    dcc.Graph(id='indicator-graphic-2', figure = line_chart(), config={
        "displaylogo": False,
    },
                  ),
                    #dbc.Button("Go somewhere", color="primary"),
                ]
            ),
        ],
        style={"border-radius": "50px", "box-shadow": "0px 0px 8px 8px #ebe9e8",
                "-webkit-box-shadow": "0px 0px 8px 8px #ebe9e8","height":"30rem", 
                "width": "32rem", "padding":"all", "margin-top":"40px",},
    ),)], justify="around"),
    html.Br(),
    dbc.Row([dbc.Col(dbc.Card(
        [
            dbc.CardBody(
                [
                    dcc.Graph(id='indicator-graphic-1', figure = bar_line_chart(), config={
        "displaylogo": False,
    },
                  ),
                    #dbc.Button("Go somewhere", color="primary"),
                ]
            ),
        ],
        style={"border-radius": "50px", "box-shadow": "0px 0px 8px 8px #ebe9e8",
                "-webkit-box-shadow": "0px 0px 8px 8px #ebe9e8","height":"30rem", 
                "width": "32rem", "padding":"all", "margin-top":"40px"},
    ),), html.Br(),
    dbc.Col(dbc.Card(
        [
            dbc.CardBody(
                [
                    dcc.Graph(id='indicator-graphic-1', figure = heat_map(), config={
        "displaylogo": False,
    },
                  ),
                    #dbc.Button("Go somewhere", color="primary"),
                ]
            ),
        ],
        style={"border-radius": "50px", "box-shadow": "0px 0px 8px 8px #ebe9e8",
                "-webkit-box-shadow": "0px 0px 8px 8px #ebe9e8","height":"30rem", 
                "width": "32rem", "padding":"all", "margin-top":"40px",},
    ),)], justify="around"),
    html.Br(),
    dbc.Row([dbc.Card(
        [
            dbc.CardBody(
                [
                    dcc.Graph(id='indicator-graphic-1', figure = show_prediction(), config={
        "displaylogo": False,
    },
                  ),
                    #dbc.Button("Go somewhere", color="primary"),
                ]
            ),
        ],
        style={"border-radius": "50px", "box-shadow": "0px 0px 8px 8px #ebe9e8",
                "-webkit-box-shadow": "0px 0px 8px 8px #ebe9e8","height":"30rem", 
                "width": "70rem", "padding":"all", "margin-top":"40px","margin-bottom":"50px"},
    ), html.Br(),], justify="around"),
    ])

def layout():
    return html.Div(children=[simple_card])

        # return simple_card
###Graph-2
'''
df1 = pd.DataFrame()
df1 =df2[df2.OUTFLOW_CUECS !='0']
df1.drop(df1[df1['FLOW_DATE'] < '2011-01-01'].index, inplace = True)
df1['INFLOW_CUSECS'] =pd.to_numeric(df1['INFLOW_CUSECS'],errors =  'coerce')
df1["INFLOW_CUSECS"].replace({"&nbsp;": "0"}, inplace=True)
y_sum1= df1.groupby('YEAR')['OUTFLOW_CUECS'].sum()
y_sum2= df1.groupby('YEAR')['INFLOW_CUSECS'].sum()
x_YEAR = ['2011','2012','2013','2014','2015','2016','2017','2018','2019','2020']
fig1 = go.Figure(data=[
    go.Bar(name='Inflow in 10 years', x=x_YEAR, y=y_sum2),
    go.Bar(name='Outflow in 10 years', x=x_YEAR, y=y_sum1)
])
# Change the bar mode
fig1.update_layout(barmode='group')
app.layout = html.Div([
        dbc.CardBody(children =[html.Div([      
        dcc.Graph(id='indicator-graphic-1', figure = fig
                  ),           
        ],
            style={"border-radius": "50px", "box-shadow": "0px 0px 8px 8px #ebe9e8",
               "-webkit-box-shadow": "0px 0px 8px 8px #ebe9e8","height":"50rem", "width": "60rem", "padding-left":"1%", "padding-right":"1%", "margin" : "auto","margin-top" : "20px","padding":"all","padding-top":"2%"}),        
        
        ]),
        dbc.CardBody(children =[html.Div([      
        dcc.Graph(id='indicator-graphic-2', figure = fig1
                  ),           
        ],
            style={"border-radius": "50px", "box-shadow": "0px 0px 8px 8px #ebe9e8",
               "-webkit-box-shadow": "0px 0px 8px 8px #ebe9e8","height":"50rem", "width": "60rem", "padding-left":"1%", "padding-right":"1%", "margin" : "auto","margin-top" : "20px","padding":"all","padding-top":"2%"}),        
        
        ]),
        
])
'''