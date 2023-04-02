import os
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
import pandas_datareader.data as web
import pandas as pd
from datetime import datetime

nsdq=pd.read_csv("nasdaq_screener_1680450464862.csv")
nsdq.set_index("Symbol", inplace=True)
options=[]

for tic in nsdq.index:
    mydict={}
    mydict["label"]=nsdq.loc[tic]["Name"] + " " + tic
    mydict["value"]=tic
    options.append(mydict)

app=dash.Dash()
os.environ["IEX_API_KEY"] ="pk_ff3a437410cd4fcfa1b9fdb44c4866f6"

app.layout= html.Div([
    html.H1("Stock Ticker Dashboard"),
    
    html.Div([
        html.H3('Select stock symbols:', style={"paddingRight":"30px"}),
    
        dcc.Dropdown(
            id="my_stock_picker", 
            options=options, 
            value=["TSLA"], multi=True
            )],
            style={"display":"inline-block","verticalAlign":"top","width": "30%"}),
    
    html.Div([html.H3("Select a start and end date:"),
            dcc.DatePickerRange(
                id="my_date_picker",
                min_date_allowed=datetime(2015,1,1),
                max_date_allowed=datetime.today(),
                start_date=datetime(2022,1,1),
                end_date=datetime.today())
                ],style={"display": "inline-block"}),

    html.Div([html.Button(
            id="submit-button",
            n_clicks=0,
            children="Submit",
            style={"fontSize":24,"marginLeft":"30px"})
            ],style={"display":"inline"}),       

    dcc.Graph(id="my_graph", 
              figure={"data":
                      [{"x":[1,2],"y":[3,1]}],
                    #   "layout":{"title":"default title"}                      
        })
    ])

@app.callback(Output("my_graph","figure"),
              [Input("submit-button","n_clicks")],
              [State("my_stock_picker","value"),State("my_date_picker","start_date"),State("my_date_picker","end_date")])

def update_graph(n_clicks, stock_ticker,start_date,end_date):
    start=datetime.strptime(start_date[:10],"%Y-%m-%d")
    end=datetime.strptime(end_date[:10],"%Y-%m-%d")

    traces=[]

    for tic in stock_ticker:
        
        df=web.DataReader(tic,"iex",start,end)
        traces.append({"x":df.index,"y":df["close"], "name":tic})
    fig={"data": traces,
        "layout":{"title":", ".join(stock_ticker) + " closing prices"}}
    return fig


if __name__=="__main__":
    app.run_server()