import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import numpy as np
from dash.dependencies import Input, Output
from plotly import graph_objs as go
from plotly.graph_objs import *
from datetime import datetime as dt
import plotly.express as px


app = dash.Dash(
    __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}])
server = app.server


df = pd.read_csv('covid_19_literature_3.csv')
df.drop(df.columns[0],axis=1,inplace = True)
df.Cluster = df.Cluster.astype('object')

df2 =df.copy()
df2.drop('x',axis=1,inplace = True)
df2.drop('y',axis=1,inplace=True)

# Layout of Dash App
app.layout = html.Div(
    children=[
        html.Div(
            className="row",
            children=[
               
               
                # Column for user controls
                html.Div(
                    className="four columns div-user-controls",
       
                    children=[
                        html.Img(
                            className="logo", src=app.get_asset_url("logo.jpg")
                        ),
                        html.H2("Covid-19 Literature"),
                        html.P(
                            """Select different days using the date picker or by selecting
                            different time frames on the histogram."""
                        ),
                        # Change to side-by-side for mobile layout
                        html.Div(
                            className="row",
                            children=[
                                html.Div(
                                    className="div-for-dropdown",
                                    children=[
                                        # Dropdown for locations on map
                                        dcc.Dropdown(
                                            id="location-dropdown",
                                            options=[
                                                {"label": i, "value": i}
                                                for i in df['Published Year'].unique()
                                            ],
                                            multi = True,
                                            value = ["2020"],
                                            placeholder="Select Published Year",
                                        )
                                    ],
                                ),
                                html.Div(
                                    className="div-for-dropdown",
                                    children=[
                                        # Dropdown to select times
                                        dcc.Dropdown(
                                            id="bar-selector",
                                            options=[
                                                {
                                                    "label": n,
                                                    "value": n,
                                                }
                                                for n in df['source'].unique()
                                            ],
                                            multi=True,
                                            value =['WHO'],
                                            placeholder="Select Source",
                                        )
                                    ],
                                ),
                                  html.Div(
                                    className="div-for-dropdown",
                                    children=[
                                        # Dropdown to select times
                                        dcc.Dropdown(
                                            id="bar-selector2",
                                            options=[
                                                {
                                                    "label": n,
                                                    "value": n,
                                                }
                                                for n in [0,1,2,3,4,5]
                                            ],
                                            multi=True,
                                            value=[0,1],
                                            placeholder="Select Cluster Number",
                                        )
                                    ],
                                ),
                                html.Div(
                    [
                        html.A(
                            html.Button("Learn More", className="learn-more-button"),
                            href="https://www.kaggle.com/phyothuhtet/document-clustering-self-organizing-map-kmeans/edit/run/31349133",
                            target="_blank",
                        )
                    ],
                    className="info-button",
                ),
                            ],
                        ),
                        
                        dcc.Markdown(
                            children=[
                                "Data Source: [Kaggle](https://www.kaggle.com/allen-institute-for-ai/CORD-19-research-challenge/)"
                            ]
                        ),
                   
                    ],
  

                ),
html.H3("The document based on the selection of your choice are..."),


html.Div(
            [   dcc.Graph(id="graph", style={"margin": "0px 20px", "height":    
                "45vh"}),
                html.Div([dcc.Markdown(id="text")], className="text-box"),
                
            ],
            id="page",
            className="eight columns div-for-charts",
),
],

        ),


    
    
 
]


)


@app.callback(
    Output('graph','figure'),
    [
       Input('location-dropdown','value'),
       Input('bar-selector','value'),
       Input('bar-selector2','value'),
    ])
def update_graph(published_year,source,cluster):
    #if published_year is not None and source is not None:
        print(type(published_year))
        print(published_year)
        #data=pd.DataFrame()
        data = df[(df['Published Year'].isin(published_year))&(df['source'].isin(source))&(df['Cluster'].isin(cluster))]
        
        #data = df[df['Published Year']==published_year]
        if not(data.empty):
            figure =px.scatter(data, x = data['x'], y= data['y']
,color="Cluster")
            return figure
        else:
            return {}


@app.callback(
    Output('text','children'),
    [
       Input('location-dropdown','value'),
       Input('bar-selector','value'),
       Input('bar-selector2','value'),
    ]
)
def update_text(published_year,source,cluster):
    data = df[(df['Published Year'].isin(published_year))&(df['source'].isin(source))&(df['Cluster'].isin(cluster))]

    return list(data['title']+', '+data['url']+', '+data['source']+', '+data['Published Year']+'\n')

if __name__ == "__main__":
    app.run_server(debug=True)
