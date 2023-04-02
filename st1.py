import os
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
import pandas_datareader.data as web
from datetime import datetime
app=dash.Dash()
os.environ["IEX_API_KEY"] ="pk_ff3a437410cd4fcfa1b9fdb44c4866f6"
app.layout= html.Div([

    html.H1("stock Ticker Dashboard"),
    html.Div([html.H3('Enter a stock symbol:',style={"paddingRight":"30px"}),
    dcc.Input(id="my_stock_picker", value="TSLA",style={"fontSize":24,"width":75})],style={"display":"inline-block","verticalAlign":"top"}),
    html.Div([html.H3("Slect a start and end date:"),
              dcc.DatePickerRange(id="my_date_picker",
              min_date_allowed=datetime(2015,1,1),
              max_date_allowed=datetime.today(),
              start_date=datetime(2022,1,1),
              end_date=datetime.today())
              ],style={"display": "inline-block"}),
    html.Div([html.Button(id="submit-button",
                          n_clicks=0,
                          children="Submit",
                          style={"fontSize":24,"marginLeft":"30px"})
    
    

    ],style={"display":"inline"}),       

    dcc.Graph(id="my_graph", 
              figure={"data":
                      [{"x":[1,2],"y":[3,1]}],
                      "layout":{"title":"default title"}                      
    })
])

@app.callback(Output("my_graph","figure"),
              [Input("submit-button","n_clicks")],
              [State("my_stock_picker","value"),State("my_date_picker","start_date"),State("my_date_picker","end_date")])

def update_graph(n_clicks, stock_ticker,start_date,end_date):
    start=datetime.strptime(start_date[:10],"%Y-%m-%d")
    end=datetime.strptime(end_date[:10],"%Y-%m-%d")
    df=web.DataReader(stock_ticker,"iex",start,end)
    fig={"data":
            [{"x":df.index,"y":df["close"]}],
            "layout":{"title":stock_ticker}                   
    }
    return fig


if __name__=="__main__":
    app.run_server()