import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input,Output, State
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import pandas as pd
import json
import plotly.express as px
import numpy as np
import plotly.offline as py
import pycountry
import pycountry_convert as pc
import flask

server = flask.Flask(__name__, template_folder='assets')
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server
# the style arguments for the sidebar. We use position:fixed and a fixed width
env = ["Ozone", "CO2", "Death from air pollution"]
with open('assets/data/Worldmap shapes/custom.geo.json') as f:
  geojson = json.load(f)

df1 = pd.read_csv("assets/data/data_situation2.csv")
df2 = pd.read_csv("assets/data/Sea_Level_GMSL.csv")


def sea_level():
    month = [1,2,3,4,5,6,7,8,9,10,11,12]*23
    month = month[0:266]
    month = pd.DataFrame(month)
    year = [1993, 1993, 1993, 1993, 1993, 1993, 1993, 1993, 1993, 1993, 1993, 1993, 1994, 1994, 1994,
       1994, 1994, 1994, 1994, 1994, 1994, 1994, 1994, 1994, 1995, 1995, 1995, 1995, 1995, 1995,
       1995, 1995, 1995, 1995, 1995, 1995, 1996, 1996, 1996, 1996, 1996, 1996, 1996, 1996, 1996,
       1996, 1996, 1996, 1997, 1997, 1997, 1997, 1997, 1997, 1997, 1997, 1997, 1997, 1997, 1997,
       1998, 1998, 1998, 1998, 1998, 1998, 1998, 1998, 1998, 1998, 1998, 1998, 1999, 1999, 1999,
       1999, 1999, 1999, 1999, 1999, 1999, 1999, 1999, 1999, 2000, 2000, 2000, 2000, 2000, 2000,
       2000, 2000, 2000, 2000, 2000, 2000, 2001, 2001, 2001, 2001, 2001, 2001, 2001, 2001, 2001,
       2001, 2001, 2001, 2002, 2002, 2002, 2002, 2002, 2002, 2002, 2002, 2002, 2002, 2002, 2002,
       2003, 2003, 2003, 2003, 2003, 2003, 2003, 2003, 2003, 2003, 2003, 2003, 2004, 2004, 2004,
       2004, 2004, 2004, 2004, 2004, 2004, 2004, 2004, 2004, 2005, 2005, 2005, 2005, 2005, 2005,
       2005, 2005, 2005, 2005, 2005, 2005, 2006, 2006, 2006, 2006, 2006, 2006, 2006, 2006, 2006,
       2006, 2006, 2006, 2007, 2007, 2007, 2007, 2007, 2007, 2007, 2007, 2007, 2007, 2007, 2007,
       2008, 2008, 2008, 2008, 2008, 2008, 2008, 2008, 2008, 2008, 2008, 2008, 2009, 2009, 2009,
       2009, 2009, 2009, 2009, 2009, 2009, 2009, 2009, 2009, 2010, 2010, 2010, 2010, 2010, 2010,
       2010, 2010, 2010, 2010, 2010, 2010, 2011, 2011, 2011, 2011, 2011, 2011, 2011, 2011, 2011,
       2011, 2011, 2011, 2012, 2012, 2012, 2012, 2012, 2012, 2012, 2012, 2012, 2012, 2012, 2012,
       2013, 2013, 2013, 2013, 2013, 2013, 2013, 2013, 2013, 2013, 2013, 2013, 2014, 2014, 2014,
       2014, 2014, 2014, 2014, 2014, 2014, 2014, 2014, 2014, 2015, 2015, 2015, 2015, 2015, 2015,
       2015, 2015, 2015, 2015, 2015, 2015,]
    year = year[0:266]
    month = pd.DataFrame(month)
    year = pd.DataFrame(year)
    Mean_Sea_Level = pd.concat([year, month, df2['GMSL']], axis=1)
    Mean_Sea_Level.columns = ['year', 'month','GMSL']
    Mean_Sea_Level = Mean_Sea_Level.groupby('year').last().reset_index()
    Rise = Mean_Sea_Level['GMSL'].diff()
    Rise.fillna(0)
    Mean_Sea_Level = pd.concat([Mean_Sea_Level, Rise], axis=1)
    Mean_Sea_Level.columns = ['year', 'month','Cumulative_change', 'One_year_rise']
    Mean_Sea_Level=Mean_Sea_Level.fillna("NA")
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=Mean_Sea_Level['year'],
            y=Mean_Sea_Level['Cumulative_change'],
            text = Mean_Sea_Level['One_year_rise'], # text to show on hover from df column
            marker=dict(color="black", size=12),
            mode = 'lines+markers',
            hovertemplate='Cumulative_change: %{y:.2f}'+'<br>Year: %{x}'+'<br>One_year_rise: %{text:.2f}'

        ))

    fig.add_trace(
        go.Bar(
            x=Mean_Sea_Level['year'],
            y=Mean_Sea_Level['Cumulative_change'],
            hovertemplate='Cumulative_change: %{y:.2f}'+'<br>Year: %{x}'
        ))
    fig.update_layout(
        title="Sea level Rise over years",
        xaxis_title="Year",
        yaxis_title="Change",
        #hovermode="x unified",
        font=dict(
            #family="Courier New, monospace",
            size=10,
            color="#7f7f7f"
        )
    )
    fig.update_layout(paper_bgcolor='white', plot_bgcolor = "white")
    return fig


def temperature_page1():
    dataset = pd.read_csv('assets/data/Situation_temperature-anomaly.csv')
    dataset = dataset[(dataset.Entity == "Global")]
    dataset.columns = ['Entity','Year', 'Median', 'Upper_bound', 'Lower_bound']
    month = dataset['Year']
    Lower_bound = dataset['Lower_bound']
    Upper_bound = dataset['Upper_bound']
    Median = dataset['Median']
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=month, y=Median, name='Median', 
                             line=dict(color='green', width=2), hovertemplate='year: %{x}'+'<br>median: %{y}'))
    fig.add_trace(go.Scatter(x=month, y=Upper_bound, name='Upper bound',
                             line=dict(color='blue', width=1,dash='dot'),hovertemplate='year: %{x}'+'<br>upper bound: %{y}'))
    fig.add_trace(go.Scatter(x=month, y=Lower_bound, name='Lower bound',
                             line = dict(color='firebrick', width=1, dash='dot'),hovertemplate='year: %{x}'+'<br>lower bound: %{y}'))
    fig.update_layout(title='Global average temperatures',
                       xaxis_title='Year',
                       yaxis_title='Temperature change',
                        plot_bgcolor="white", paper_bgcolor='white',)
    return fig


###CO2 emissions plot
CO2_Emi = pd.read_csv("assets/data/CO2_Emissions.csv")
def findCountryAlpha2 (country_name):
    try:
        return pycountry.countries.get(name=country_name).alpha_2
    except:
        return ("not founded!")

def findCountryAlpha3 (country_name):
    try:
        return pycountry.countries.get(name=country_name).alpha_3
    except:
        return ("not founded!")

def findCountryNumeric (country_name):
    try:
        return pycountry.countries.get(name=country_name).numeric
    except:
        return ("not founded!")
    
def findCountryOfficialName (country_name):
    try:
        return pycountry.countries.get(name=country_name).official_name
    except:
        return ("not founded!")
    
CO2_Emi['country_alpha_2'] =CO2_Emi.apply(lambda row: findCountryAlpha2(row.country) , axis = 1)
CO2_Emi['country_alpha_3'] =CO2_Emi.apply(lambda row: findCountryAlpha3(row.country) , axis = 1)
CO2_Emi['country_numeric'] =CO2_Emi.apply(lambda row: findCountryNumeric(row.country) , axis = 1)
CO2_Emi['official_name'] = CO2_Emi.apply(lambda row: findCountryOfficialName(row.country) , axis = 1)
def country_to_continent(country_name):
    try:
        country_alpha2 = pc.country_name_to_country_alpha2(country_name)
        country_continent_code = pc.country_alpha2_to_continent_code(country_alpha2)
        country_continent_name = pc.convert_continent_code_to_continent_name(country_continent_code)
        return country_continent_name
    except:
        return ("not founded!")
CO2_Emi['continent'] = CO2_Emi.apply(lambda row: country_to_continent(row.official_name) , axis = 1)
list_var = CO2_Emi.columns.values.tolist()
list_var.remove('country')
list_var.remove('country_alpha_2')
list_var.remove('country_alpha_3')
list_var.remove('country_numeric')
list_var.remove('official_name')
list_var.remove('continent')

###Co2 emissions plot
def emissions():
    CO2_Emi_1 = pd.melt(CO2_Emi, id_vars=['country',"continent"], value_vars=list_var,var_name='year')
    CO2_Emi_1 = CO2_Emi_1.fillna(0)
    CO2_Emi_final = CO2_Emi_1.groupby(['year','continent'])['value'].sum().reset_index()
    fig = px.area(CO2_Emi_final, x="year", y="value", color="continent",title ="CO2 emissions by continent", line_group="continent")
    fig.update_layout(paper_bgcolor='white', plot_bgcolor = "white")
    return fig


###Net-Tracker
def get_NetZeroTargetWM():
        df_nzc = pd.read_csv('assets/data/countries.csv')
        with open('assets/data/Worldmap shapes/custom.geo.json') as f:
              geojson = json.load(f)
        fig_nzc = px.choropleth_mapbox(df_nzc, geojson=geojson, locations="Abbreviation",
                    color='Target Status',
                    mapbox_style="carto-positron",
                    featureidkey="properties.iso_a3",
                    hover_name='Title',
                    hover_data=['Target Year'],
                    zoom=1,
                    opacity=0.8,
                    center = {"lat": 50.958427, "lon": 10.436234},
                    )
        fig_nzc.update_layout(margin=dict(l=20,r=0,b=0,t=70,pad=0),paper_bgcolor="white",height= 500,title_text = 'Net-Zero Tracker',font_size=18)
        
        return fig_nzc


# Damage dealt to EU economy PLot
def get_dmgEU():
        df_eea = pd.read_csv('assets/data/natural-disasters-events-3.csv', sep=',')
        df_eea2 = df_eea.loc[df_eea['Chart'] == 'EU-28']
        fig = go.Figure(layout=go.Layout(
        title=go.layout.Title(text="Damage dealt to the EU economy by natural disasters in millions")
        ))
        fig.update_layout(barmode='stack',paper_bgcolor='white', plot_bgcolor = "white")
        fig.update_xaxes(title='Year')
        fig.update_yaxes(title='EUR in millions')
        fig.add_trace(go.Bar(
        x=df_eea2['Year'],
        #y=df_eea['Type']=='Geophysical events',
        y=df_eea2.loc[df_eea2['Type'] == 'Geophysical events']['Value'],
        name='Geophysical events',
        marker_color='#148C3F',
        ))
        fig.add_trace(go.Bar(
        x=df_eea2['Year'],
        y=df_eea2.loc[df_eea2['Type'] == 'Climatological event']['Value'],
        name='Climatological event',
        marker_color='#45bf55'
        ))
        fig.add_trace(go.Bar(
        x=df_eea2['Year'],
        y=df_eea2.loc[df_eea2['Type'] == 'Hydrological event']['Value'],
        name='Hydrological event',
        marker_color='#97ed8a'
        ))
        fig.add_trace(go.Bar(
        x=df_eea2['Year'],
        y=df_eea2.loc[df_eea2['Type'] == 'Meteorological events']['Value'],
        name='Meteorological event',
        marker_color='#0b6129',
        hovertemplate='Year: %{x}'+'<br>EUR: %{y}'
        ))

        #fig = px.bar(df_eea.loc[df_eea['Chart']=='EU-28'], x="Year", y="Value", color="Type", title="Damage dealt to the EU economy by natural disasters in millions",labels={'x':'Year', 'y':'EUR in million'})
        #fig_trend= (px.scatter( x=df_eea['Year'], y=df_eea['Value'], trendline="ols", labels={'x':'Year', 'y':'Regression Value'},color_discrete_sequence=["#148C3F"], title='Trend of economic damage caused by<br> weather and climate-related extreme events in Europe'))

        return fig
###GDP plot
def get_dropGDP():
    df1 = pd.read_csv('assets/data/C_Percentage change in regional GDP.csv', sep=';')
    df1_ols = pd.read_excel('assets/data/C_Percentage change in regional GDP_ols.xlsx')
    df1 = pd.melt(df1, id_vars=['Date'],value_vars=['OECD Europe', 'OECD Pacific', 'OECD America', 'Latin America',
       'Rest of Europe and Asia', 'Middle East and North Africa',
       'South and South-East Asia', 'Sub-Saharan Africa'])
    df1_ols = pd.melt(df1_ols, id_vars=['Date'],value_vars=['OECD Europe', 'OECD Pacific', 'OECD America', 'Latin America',
        'Rest of Europe and Asia', 'Middle East and North Africa',
       'South and South-East Asia', 'Sub-Saharan Africa'])
        #GDP Drop figgure Total Data
    graph  = px.bar(df1_ols, 
        x='Date', 
        y="value", 
        color="variable", 
        title='Percentage change in regional GDP by selected climate change impacts', 
        color_continuous_scale='Greens',
        labels=dict(variable='Regions', x ='Year', y ='Percentage change in regional GDP'),
        )

    graph.update_xaxes(title='Year')
    graph.update_yaxes(title='Change of GDP in %')
    graph.update_layout(paper_bgcolor='white', plot_bgcolor = "white")
    #graph.update_yaxes(autorange="reversed")

    #GDP Drop figgure for Trend
    #fig_trend= (px.scatter( x=df1_ols['Date'], y=df1_ols['value'], trendline="ols", labels={'x':'Year', 'y':'Regression Value'},color_discrete_sequence=["#148C3F"], title='Trend of Percentage change in regional GDP due to selected climate change impacts'))
    #fig_trend.update_yaxes(autorange="reversed")
    return graph


# Funding PLot
def get_fundingGraph():
    dataset_pledges = pd.read_excel('assets/data/Governmental_efforts_climate funding_Pledges.xlsx')
    dataset_pledges.columns = ['Fund','Fund Type', 'Fund Focus', 'Contributor', 'Country', 'Country Income Level','Region', 'Pledged (USD million current)', 'Deposited (USD million current)','test','test1']
    dataset_pledges=dataset_pledges.groupby(by=["Country"])['Pledged (USD million current)', 'Deposited (USD million current)'].sum().reset_index()
    dataset_pledges = dataset_pledges.nlargest(15, 'Pledged (USD million current)')
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=dataset_pledges['Country'],
        y=dataset_pledges['Pledged (USD million current)'],
        name='Pledged (USD million)',
        #marker_color='indianred'
    ))

    fig.add_trace(go.Bar(
        x=dataset_pledges['Country'],
        y=dataset_pledges['Deposited (USD million current)'],
        name='Deposited (USD million)',
        #marker_color='lightsalmon'
    ))


    # Here we modify the tickangle of the xaxis, resulting in rotated labels.
    fig.update_layout(barmode='group', xaxis_tickangle=-45, title='Money pledged and deposited for climate funds by countries',paper_bgcolor='white', plot_bgcolor = "white")
    return fig


def renewable():
    dataset = pd.read_csv('assets/data/Situation_renewable-share-energy.csv')
    dataset.columns = ['Entity','Code','Year', 'Renewables']
    dataset["Indice"] = 0
    
    for i in range(4284):
        if dataset.iloc[i, 0] == "United States":
            dataset.iloc[i, 0] = "US"
        if dataset.iloc[i, 0] == "World":
            dataset.iloc[i, 4] = 1
    
    df0 = dataset[dataset.Entity.isin(["World"])]
    df1 = dataset[dataset.Entity.isin(["India"])]
    df2 = dataset[dataset.Entity.isin(["Africa"])]
    df3 = dataset[dataset.Entity.isin(["US"])]
    df4 = dataset[dataset.Entity.isin(["China"])]
    df5 = dataset[dataset.Entity.isin(["Europe"])]
    
    dataset = pd.concat([df0, df1,df2,df3, df4, df5], ignore_index=True)
    
    histogram = px.histogram(dataset, x = "Entity", y = "Renewables", histfunc='avg',
                            color = "Indice",
                            animation_frame="Year")
    
    histogram.update_layout(yaxis_range=[0,20])
    histogram.update_layout(title = "Share of renewable energies", title_x = 0.5, title_font_size = 15, showlegend=False)
    
    histogram.update_layout(xaxis_title='Entity', yaxis_title='Percentage', paper_bgcolor='white', plot_bgcolor = "white")
        
    return histogram


app.layout = html.Div(
    [
        #dbc.Row(dbc.Col()),
        dbc.Row(
            [
                dbc.Col(html.Img(src="assets/1.png", style = {
                 "height":"150px",   
                "width":"auto",
                "margin-left":"50px",
                 "display": "block",
                
                 'padding':'5px',
            } ),style={}),
                dbc.Col(html.Div(html.H3("Environmental Awareness", ),
                style = {'width': "auto", "color": "white", 'text-align': 'center', "font-family": "Fredoka One","font-size": "20px","margin-top":"40px","color": "black"})
                ),
                dbc.Col(html.Div(style = {'width': "auto", "color": "black", 'text-align': 'right', "font-family": "Fredoka One","font-size": "20px",},
                children = [
                    dbc.Button("About Us", id="open", n_clicks=0, style={"margin-right":"25px","margin-top":"25px",}, color="primary"),
                    dbc.Modal([
                        dbc.ModalHeader("About Us"),
                        dbc.ModalBody([html.Div("Name- Abhinav Gadgil  Reg No-19MIM10067"),html.Div("Name- Rahul Mandviya Reg No-19MIM10062"),]),
                    dbc.ModalFooter(
                        dbc.Button("Close", id="close", className="ml-auto", n_clicks=0,color="primary")
                            ),
                        ],
            id="modal",
            # size="lg",
            is_open=False,
            backdrop=True,
            centered=True,
            fade=True,
        ) ])),]
        ),
        html.Br(),
        dbc.Row([
           dbc.Col(dbc.Card([
               dbc.CardBody([
                                   dcc.Dropdown(
                    id='env-id',
                    options=[{'label': i, 'value': i} for i in env],
                    value='Ozone',
                    placeholder='Select something...',
                    style = {"width": "100%", "border-radius": "30px 30px 0px 0px"}
                ),
                dcc.Tabs(id='tabs-example', value='tab-1', children=[
        dcc.Tab(label='Map view ', value='tab-1' , children =[dcc.Graph(id = "map-view",config={ "displaylogo": False}, style = {"width": "100%", "border-radius": "50px 50px 0px 0px"})] ),
        dcc.Tab(label='Globe view', value='tab-2', children =[dcc.Graph(id = "globe-view",config={ "displaylogo": False}, style = {"width": "100%", "border-radius": "50px 50px 0px 0px"})]),
    ],
    style = {"width": "100%"}),     
    #  style={"background-color": "black",}
            # style={"border-radius": "50px",
            #    'display': 'inline-block', "width": "auto", "padding-left":"1%", "padding-right":"1%", "margin-bottom": "50px", 
            #    "margin-top": "10px", "padding-top": "25px", 
            #    "color":"blue", "display":"inline-block", "margin-left":"20px",}
                      
],

# style={"background-color": "black",},
),],
style={
               'display': 'inline-block',"width":"95%", "height":"auto",  "padding":"all",  
               "background-color":"white", "margin-left" : "30px" , "border-radius": "50px", "box-shadow": "0px 0px 8px 8px #fafafa",
                "-webkit-box-shadow": "0px 0px 8px 8px #fafafa"},
           ),width = 6), 
             #html.Br(), 
           dbc.Col(dbc.Card(dbc.CardBody([dcc.Graph(
               id='indicator-graphic-1',figure = sea_level(), config={
        "displaylogo": False},
                  ),
                  ]),style={
               'display': 'inline-block',"width":"95%", "height":"auto",  "padding":"all",  
               "background-color":"white", "margin-right" : "20px" , "border-radius": "50px", "box-shadow": "0px 0px 8px 8px #fafafa",
                "-webkit-box-shadow": "0px 0px 8px 8px #fafafa" } ), width =6)
        ]), 
        html.Br(),
        ###Second row of graphs
        dbc.Row([dbc.Col(dbc.Card(dbc.CardBody([dcc.Graph(
               id='indicator-graphic-2',figure = temperature_page1(), config={
        "displaylogo": False},
                  ),
                  ]),style={
               'display': 'inline-block',"width":"95%", "height":"auto",  "padding":"all",  
               "background-color":"white","margin-left" : "30px", "border-radius": "50px", "box-shadow": "0px 0px 8px 8px #fafafa",
                "-webkit-box-shadow": "0px 0px 8px 8px #fafafa"} ), width =6),
                dbc.Col(dbc.Card(dbc.CardBody([dcc.Graph(
               id='indicator-graphic-3',figure = emissions(), config={
        "displaylogo": False},
                  ),
                  ]),style={
               'display': 'inline-block',"width":"95%", "height":"auto",  "padding":"all",  
               "background-color":"white",  "margin-right":"20px", "border-radius": "50px", "box-shadow": "0px 0px 8px 8px #fafafa",
                "-webkit-box-shadow": "0px 0px 8px 8px #fafafa"} ), width = 6)
               
               
               
               
            ]),
            ###Third Row
                    html.Br(),
        dbc.Row([dbc.Col(dbc.Card(dbc.CardBody([dcc.Graph(
               id='indicator-graphic-4',figure = get_NetZeroTargetWM(), config={
        "displaylogo": False},
                  ),
                  ]),style={
               'display': 'inline-block',"width":"96%", "height":"auto",  "padding":"all",  
               "background-color":"white","margin-left" : "30px", "border-radius": "50px", "box-shadow": "0px 0px 8px 8px #fafafa",
                "-webkit-box-shadow": "0px 0px 8px 8px #fafafa"} ), ),                           
            ]),
            ###Fourth Row
            html.Br(),
        dbc.Row([dbc.Col(dbc.Card(dbc.CardBody([
            
            dcc.Graph(
               id='indicator-graphic-5',figure = get_dmgEU(), config={
        "displaylogo": False},
                  ),
                  ]),style={
               'display': 'inline-block',"width":"95%", "height":"auto",  "padding":"all",  
               "background-color":"white","margin-left" : "30px", "border-radius": "50px", "box-shadow": "0px 0px 8px 8px #fafafa",
                "-webkit-box-shadow": "0px 0px 8px 8px #fafafa"} ), width=6),
                dbc.Col(dbc.Card(dbc.CardBody([dcc.Graph(
               id='indicator-graphic-6',figure = get_dropGDP(), config={
        "displaylogo": False},
                  ),
                  ]),style={
               'display': 'inline-block',"width":"95%", "height":"auto",  "padding":"all",  
               "background-color":"white",  "margin-right":"20px", "border-radius": "50px", "box-shadow": "0px 0px 8px 8px #fafafa",
                "-webkit-box-shadow": "0px 0px 8px 8px #fafafa"} ), width =6)              
            ]),
                        ###Fourth Row
            html.Br(),
        dbc.Row([dbc.Col(dbc.Card(dbc.CardBody([
            
            dcc.Graph(
               id='indicator-graphic-7',figure = get_fundingGraph(), config={
        "displaylogo": False},
                  ),
                  ]),style={
               'display': 'inline-block',"width":"95%", "height":"auto",  "padding":"all",  
               "background-color":"white","margin-left" : "30px", "border-radius": "50px", "box-shadow": "0px 0px 8px 8px #fafafa",
                "-webkit-box-shadow": "0px 0px 8px 8px #fafafa"} ), width = 6),
                dbc.Col(dbc.Card(dbc.CardBody([dcc.Graph(
               id='indicator-graphic-8',figure = renewable(), config={
        "displaylogo": False},
                  ),
                  ]),style={
               'display': 'inline-block',"width":"95%", "height":"auto",  "padding":"all",  
               "background-color":"white",  "margin-right":"20px", "border-radius": "50px", "box-shadow": "0px 0px 8px 8px #fafafa",
                "-webkit-box-shadow": "0px 0px 8px 8px #fafafa"} ), width =6)               
            ])


    ]
)


@app.callback(
     Output("map-view", "figure"),
     [Input("env-id", "value")])
def update_map_globe(env_id,):
    if env_id == "CO2" :
            fig = px.choropleth_mapbox(df1, locations="CODE",
                                geojson = geojson,
                                mapbox_style="carto-positron",
                                featureidkey="properties.iso_a3",
                                zoom=1,
                                opacity=0.8,
                                center = {"lat": 50.958427, "lon": 10.436234},
                                color="CO2_emissions", # lifeExp is a column of gapminder
                                hover_name="COUNTRY", # column to add to hover information
                                color_continuous_scale=px.colors.sequential.Plasma)
            fig.update_layout(title='CO2 emission per capita : 2019 (in tons)')
            fig.update_layout(margin=dict(l=20,r=0,b=0,t=70,pad=0),paper_bgcolor='white',title_text = 'CO2 emission per capita : 2019 (in tons)',font_size=18)
    if env_id == "Death from air pollution":
        fig = px.choropleth_mapbox(df1, locations="CODE",
                            geojson = geojson,
                            mapbox_style="carto-positron",
                            featureidkey="properties.iso_a3",
                            zoom=1,
                            opacity=0.8,
                            labels={'Death_from_air_pollution':'death_rate'},
                            center = {"lat": 50.958427, "lon": 10.436234},
                            color="Death_from_air_pollution", # lifeExp is a column of gapminder
                            hover_name="COUNTRY", # column to add to hover information
                            color_continuous_scale=px.colors.sequential.Plasma)
        fig.update_layout(title='Death from air pollution : 2019 (per 100 000 citizens)', )
        fig.update_layout(margin=dict(l=20,r=0,b=0,t=70,pad=0),paper_bgcolor='white',title_text = 'Death by air pollution : 2019 (per 100 000 citizens)',font_size=18)
    if env_id == "Ozone":
        fig = px.choropleth_mapbox(df1, locations="CODE",
                            geojson = geojson,
                            mapbox_style="carto-positron",
                            featureidkey="properties.iso_a3",
                            zoom=1,
                            opacity=0.8,
                            labels={'Ozone_concentration':'Ozone'},
                            center = {"lat": 50.958427, "lon": 10.436234},
                            color="Ozone_concentration", # lifeExp is a column of gapminder
                            hover_name="COUNTRY", # column to add to hover information
                            color_continuous_scale=px.colors.sequential.Plasma)
        fig.update_layout(title='Ozone concentration : 2019')
        fig.update_layout(margin=dict(l=20,r=0,b=0,t=70,pad=0),paper_bgcolor='white', title_text = 'Ozone concentration : 2019',font_size=18)
    return fig

@app.callback(
     Output("globe-view", "figure"),
     [Input("env-id", "value"), Input("tabs-example", "value")])
def update_map_globe(env_id, tab):
    if env_id == "CO2" :
        if tab == 'tab-1':
            fig = px.choropleth_mapbox(df1, locations="CODE",
                                geojson = geojson,
                                mapbox_style="carto-positron",
                                featureidkey="properties.iso_a3",
                                zoom=1,
                                opacity=0.8,
                                center = {"lat": 50.958427, "lon": 10.436234},
                                color="CO2_emissions", # lifeExp is a column of gapminder
                                hover_name="COUNTRY", # column to add to hover information
                                color_continuous_scale=px.colors.sequential.Plasma)
            fig.update_layout(title='CO2 emission per capita : 2019 (in tons)')
            fig.update_layout(margin=dict(l=20,r=0,b=0,t=70,pad=0),paper_bgcolor='white',title_text = 'CO2 emission per capita : 2019 (in tons)',font_size=18)
        elif tab == "tab-2":
            mean_temp = []
            countries = np.unique(df1['Country_Region'])
            for country in countries:                
                mean_temp.append(df1[df1['Country_Region'] == country]['CO2_emissions'].mean())  
            data = [ dict(
                    type = 'choropleth',
                    locations = countries,
                    z = mean_temp,
                    locationmode = 'country names',
                    text = countries,
                    marker = dict(
                        line = dict(color = 'rgb(0,0,0)', width = 1)),
                        # colorbar = dict(autotick = "True", tickprefix = '', 
                        # title = ' Co2 emissions')
                        )
                ]

            layout = dict(
                title = 'Average CO2 emissions in countries',
                geo = dict(
                    showframe = False,
                    showocean = True,
                    oceancolor = 'rgb(0,255,255)',
                    projection = dict(
                    type = 'orthographic',
                        rotation = dict(
                                lon = 60,
                                lat = 10),
                    ),
                    lonaxis =  dict(
                            showgrid = True,
                            gridcolor = 'rgb(102, 102, 102)'
                        ),
                    lataxis = dict(
                            showgrid = True,
                            gridcolor = 'rgb(102, 102, 102)'
                            )
                        ),
                    )
            fig=go.Figure(data=data, layout=layout)
            #fig.show()

    if env_id == "Death from air pollution":
        if tab == 'tab-1':
            fig = px.choropleth_mapbox(df1, locations="CODE",
                                geojson = geojson,
                                mapbox_style="carto-positron",
                                featureidkey="properties.iso_a3",
                                zoom=1,
                                opacity=0.8,
                                center = {"lat": 50.958427, "lon": 10.436234},
                                color="Death_from_air_pollution", # lifeExp is a column of gapminder
                                hover_name="COUNTRY", # column to add to hover information
                                color_continuous_scale=px.colors.sequential.Plasma)
            fig.update_layout(title='Death from air pollution : 2019 (per 100 000 citizens)')
            fig.update_layout(margin=dict(l=20,r=0,b=0,t=70,pad=0),paper_bgcolor='white',title_text = 'Death from air pollution : 2019 (per 100 000 citizens)',font_size=18)
        elif tab == 'tab-2':
            mean_temp = []
            countries = np.unique(df1['Country_Region'])
            for country in countries:                
                mean_temp.append(df1[df1['Country_Region'] == country]['Death_from_air_pollution'].mean())  
            data = [ dict(
                    type = 'choropleth',
                    locations = countries,
                    z = mean_temp,
                    locationmode = 'country names',
                    text = countries,
                    marker = dict(
                        line = dict(color = 'rgb(0,0,0)', width = 1),
                        ),
                        # colorbar = dict(autotick = "True", tickprefix = '', 
                        # title = ' Co2 emissions')
                        
                        )
                    
                ]

            layout = dict(
                title = 'Death from air pollution',
                geo = dict(
                    showframe = False,
                    showocean = True,
                    oceancolor = 'rgb(0,255,255)',
                    projection = dict(
                    type = 'orthographic',
                        rotation = dict(
                                lon = 60,
                                lat = 10),
                    ),
                    lonaxis =  dict(
                            showgrid = True,
                            gridcolor = 'rgb(102, 102, 102)'
                        ),
                    lataxis = dict(
                            showgrid = True,
                            gridcolor = 'rgb(102, 102, 102)'
                            )
                        ),
                    )
            fig=go.Figure(data=data, layout=layout)

    if env_id == "Ozone":
        if tab == 'tab-1':
            fig = px.choropleth_mapbox(df1, locations="CODE",
                                geojson = geojson,
                                mapbox_style="carto-positron",
                                featureidkey="properties.iso_a3",
                                zoom=1,
                                opacity=0.8,
                                labels={'Ozone_concentration':'Ozone'},
                                center = {"lat": 50.958427, "lon": 10.436234},
                                color="Ozone_concentration", # lifeExp is a column of gapminder
                                hover_name="COUNTRY", # column to add to hover information
                                color_continuous_scale=px.colors.sequential.Plasma)
            fig.update_layout(title='Ozone concentration : 2019')
            fig.update_layout(margin=dict(l=20,r=0,b=0,t=70,pad=0),paper_bgcolor='white', title_text = 'Ozone concentration : 2019',font_size=18)
        if tab == 'tab-2':
            mean_temp = []
            countries = np.unique(df1['Country_Region'])
            for country in countries:                
                mean_temp.append(df1[df1['Country_Region'] == country]['Ozone_concentration'].mean())  
            data = [ dict(
                    type = 'choropleth',
                    locations = countries,
                    z = mean_temp,
                    locationmode = 'country names',
                    text = countries,
                    marker = dict(
                        line = dict(color = 'rgb(0,0,0)', width = 1)),
                        # colorbar = dict(autotick = "True", tickprefix = '', 
                        # title = ' Co2 emissions')
                        )
                ]

            layout = dict(
                title = 'Ozone concentration',
                geo = dict(
                    showframe = False,
                    showocean = True,
                    oceancolor = 'rgb(0,255,255)',
                    projection = dict(
                    type = 'orthographic',
                        rotation = dict(
                                lon = 60,
                                lat = 10),
                    ),
                    lonaxis =  dict(
                            showgrid = True,
                            gridcolor = 'rgb(102, 102, 102)'
                        ),
                    lataxis = dict(
                            showgrid = True,
                            gridcolor = 'rgb(102, 102, 102)'
                            )
                        ),
                    )
            fig=go.Figure(data=data, layout=layout)

    
    return fig


def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open


app.callback(
    Output("modal", "is_open"),
    [Input("open", "n_clicks"), Input("close", "n_clicks")],
    [State("modal", "is_open")],
    )(toggle_modal)


if __name__ == "__main__":
    app.run_server(port=8050, debug=False)