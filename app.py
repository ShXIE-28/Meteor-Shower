# -*- coding: utf-8 -*-
"""
Explore the Starry Sky

@author: shuhui
"""
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc 
import navbar
import pandas as pd
import dash_table
from meteor_map import create_map,update_map

##################################  dashboard page  #################################
bs = "https://stackpath.bootstrapcdn.com/bootswatch/4.5.2/sandstone/bootstrap.min.css"
app = dash.Dash(__name__, external_stylesheets=[bs])
sercer = app.server
image = 'url(https://www.imo.net/members/upload/photos/2019/11631_1037.jpg)'
dt = pd.read_csv('.\\dataset\\observor.csv',encoding='ISO-8859-1')
date_list = dt['Start Date'].drop_duplicates().to_list()
top20 = pd.read_csv('.\\dataset\\top20.csv')
top10 = pd.read_csv('.\\dataset\\top10.csv')

tab1 = dbc.Card(dbc.CardBody([
                html.H4("Meteor Shower Observation Records",className='card-title'),
                html.P("Select a year range to see the observation cases over the\
                       world.",style={'color':'#708090'}),
                html.Div(dcc.Graph(id='meteor_map',figure = create_map(dt,1980,2020))),
                html.Div(id='range_slider', style={'margin-top': 10,'color':'#778899'}),
                dcc.RangeSlider(id='year_slider',min=1980,max=2020,step=1,
                                marks={i:i for i in range(1980,2021,5)},disabled=False),
                dbc.Button("Filter",outline=True,color="info",className="mr-1",
                           style={'width':'70px'},id='filter'),
                dbc.Row(dbc.Col(html.Br())),
                dbc.Checklist(id='activate',
                    options=[{'label':'Activate specific date filter','value':1}],
                    value=[],switch=True
                ),
                dbc.Row(dbc.Col(html.Br())),
                html.Div([
                        dbc.FormText("Please input date in the format of MM/DD/YYYY, \
                                     eg 1/1/2000 (click FILTER to refresh)"),
                        dbc.Row([dbc.Col(dbc.Input(id='date_s',type='text',
                                          placeholder='Start Point',disabled=True,
                                          style={'width':'150px'}),width=2),
                                 dbc.Col(dbc.Input(id='date_e',type='text',
                                          placeholder='End Point',disabled=True,
                                          style={'width':'150px'}),width=2)],
                                 justify="start"),
                        dbc.Fade(html.P("Invalid date input",
                                        style={'color':'red','size':1}),
                                 id='fade',is_in=False,appear=False),
                        dbc.Row(dbc.Col(html.Br()))
                        ])
                
            ])
        )

tab2 = dbc.Card(dbc.CardBody([
        html.H4("Meteor Shower Observation Top List",className='card-title'),
        html.P("Select a list that you are interested",style={'color':'#708090'}),
        html.Div([dcc.Dropdown(id='list_dropdown',options=[
                {'label':'Top 20 observation cities','value':'list1'},
                {'label':'Top 10 observation dates','value':'list2'},
                {'label':'Future Meteor Showers','value':'list3'}
                ]),
                  html.Div(id='table')])
    ]))

tabs = dbc.Tabs([dbc.Tab(tab1,label='meteor tab',style={'width':'1150px'},
                         tab_style={"margin-left": "auto"}),
                 dbc.Tab(tab2,label='top list',style={'width':'1150px'})])

app.layout = html.Div(
        style = {'background-image':image},
        children = [navbar.Navbar(),
                    dbc.Row(dbc.Col(html.Br())),
                    dbc.Row(dbc.Col(html.H2("Explore the Starry Sky",
                                            style={'color':'#F5FFFA'}),
                                    width={"offset":1})),
                    dbc.Row(dbc.Col(html.P("Enjoy the interesting facts in this\
                                           page!",style={'color':'#FDF5E6'}),
                                           width={"offset":1})),
                    dbc.Row(dbc.Col(tabs,width={"offset":1})),
                    dbc.Row(dbc.Col(html.Br())),
                    dbc.Row(dbc.Col(html.Br())),
                    dbc.Row(dbc.Col(html.Br())),
                    ])


##################################  callback  #################################

# slider content
@app.callback(
        [Output("range_slider","children"),
         Output("meteor_map","figure")],
        [Input("filter","n_clicks")],
        [State("year_slider","value"),
         State("activate","value"),
         State("date_s","value"),
         State("date_e","value"),
         State("fade","is_in")]
        )
def slider(n_clicks,value,activate,date_s,date_e,fade):
    if (len(activate)==0) & (fade==False):
        figure = create_map(dt,value[0],value[1])
        string = "Year Range: {} - {}".format(value[0],value[1])
    
        return string,figure
    elif (len(activate)==1) & (fade==False):
        index_s = dt[dt['Start Date']==date_s].index[0]
        index_e = dt[dt['Start Date']==date_e].index[-1]
        temp = dt.iloc[index_s:index_e+1]
        figure = update_map(temp)
        
        return None,figure

# activate date filter
@app.callback(
        [Output("date_s","disabled"),
         Output("date_e","disabled"),
         Output("year_slider","disabled")],
        [Input("activate","value")]
        )
def activate(value):
    if len(value) == 1:
        return False,False,True
    else:
        return True,True,False

# valid date
@app.callback(
        Output("fade","is_in"),
        [Input("filter","n_clicks")],
        [State("date_s","value"),
         State("date_e","value"),
         State("activate","value")]
        )
def valid_date(n_clicks,date_s,date_e,value):
    if len(value) == 1:
        if date_s not in date_list:
            return True
        elif date_e not in date_list:
            return True
        else:
            return False
    else:
        return False

# top list
@app.callback(
        Output("table","children"),
        [Input("list_dropdown","value")]
        )
def create_tanble(list):
    if list=='list1':
        table1 = dash_table.DataTable(
                data=top20.to_dict("records"),
                columns=[{'id': c, 'name': c} for c in top20.columns],
                style_cell={'textAlign': 'center'},
                style_as_list_view=True,
                style_header={'backgroundColor': '#cad7e8','fontWeight': 'bold'},
                style_table={'height': '400px', 'overflowY': 'auto'}
            )
        return table1
    elif list=='list2':
        table2 = dash_table.DataTable(
                data=top10.to_dict("records"),
                columns=[{'id': c, 'name': c} for c in top10.columns],
                tooltip_data=[
                    {'Name':{'value':'![Sirius Leonid Meteor](https://wtop.com/wp-content/uploads/2020/11/GettyImages-51398296-1024x694.jpg)',
                            'type': 'markdown'}
                        
                    }
                ],
                tooltip_delay=0,
                tooltip_duration=None,
                style_cell={'textAlign': 'center'},
                style_as_list_view=True,
                style_header={'backgroundColor': '#cad7e8','fontWeight': 'bold'},
                style_table={'height': '400px', 'overflowY': 'auto'},
                virtualization = True
            )
        return table2
    
    
    
    
    
    

if __name__ =='__main__':
    app.run_server(debug=False)