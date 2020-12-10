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
from date_filter import date_standard,date_filter,contain_alpha

##################################  dashboard page  #################################
bs = "https://stackpath.bootstrapcdn.com/bootswatch/4.5.2/sandstone/bootstrap.min.css"
app = dash.Dash(__name__, external_stylesheets=[bs])
sercer = app.server
image = 'url(https://www.imo.net/members/upload/photos/2019/11631_1037.jpg)'
dt = pd.read_csv('.\\dataset\\observor.csv',encoding='ISO-8859-1')
date_list = pd.read_csv('.\\dataset\\date_list.csv')
top20 = pd.read_csv('.\\dataset\\top20.csv')
top10 = pd.read_csv('.\\dataset\\top10.csv')
future = pd.read_csv('.\\dataset\\future.csv')
zpic = pd.read_csv('.\\dataset\\zodiac pic.csv')
hubble = pd.read_csv('.\\dataset\\hubble-birthdays-full-year.csv',encoding='ISO-8859-1')

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

controls = dbc.Card([
        html.P("Input your date of birth:",style={'color':'#708090'}),
        dbc.InputGroup(
            [dbc.InputGroupAddon("Month",addon_type="prepend"),
             dbc.Input(id='month',type="number",min=1,max=12,step=1)],
            style={'width':'150px'}),
        html.Br(),
        dbc.InputGroup(
            [dbc.InputGroupAddon("Day",addon_type="prepend"),
             dbc.Input(id='day',type="number",min=1,max=31,step=1)],
            style={'width':'150px'}),
        html.Br(),
        dbc.Button("Submit",id='submit',color="secondary",
                   className="btn btn-secondary",style={'width':'150px'})
            ],color="light",outline=True)

collapse = html.Div([
            dbc.Button("What did Hubble see on your birthday",style={'width':'200px'},
                       color="light", className="mr-1",id="collapse_button"),
            dbc.Collapse(dbc.Card([
                    dbc.CardHeader(id='card_header'),
                    dbc.CardBody([
                            html.P(id='card_text'),
                            dbc.CardLink("Find image here",id='card_link',
                                         external_link=True)
                            ])
                   ]),id='collapse'
            )
        ])

zodiac = [html.H5(id='constellation',style={'color':'#383050'}),
          html.Br(),
          html.P(id='pic_title',style={'color':'#383050'}),                            
          html.Img(id='zodiac_pic',style={'height':'600px','width':'600px'})
        ]

tab3 = dbc.Card(dbc.CardBody([
        html.H4("Find your Zodiac Constellation !",className='card-title'),
        html.Hr(),
        dbc.Row([dbc.Col([controls,html.Br(),collapse],width=3),
                 dbc.Col(width=1),
                 dbc.Col(zodiac)
                 ])
    ]))



tabs = dbc.Tabs([dbc.Tab(tab1,label='meteor tab',style={'width':'1150px'},
                         tab_style={"margin-left": "auto"}),
                 dbc.Tab(tab2,label='top list',style={'width':'1150px'}),
                 dbc.Tab(tab3,label='Zodiac Constellation',style={'width':'1150px'})])

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
                    dbc.Row(dbc.Col(html.I("All information are from IMO\
                                           (International Meteor Organization)\
                                           and NASA.",style={'color':'#FDF5E6'}),
                                           width={"offset":1})),
                    dbc.Row(dbc.Col(tabs,width={"offset":1})),
                    dbc.Row(dbc.Col(html.Br())),
                    dbc.Row(dbc.Col(html.Br())),
                    dbc.Row(dbc.Col(html.Br())),
                    ])


##################################  callback  #################################

# filter map
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
def filter_map(n_clicks,value,activate,date_s,date_e,fade):
    if (len(activate)==0) & (fade==False):
        figure = create_map(dt,value[0],value[1])
        string = "Year Range: {} - {}".format(value[0],value[1])
    
        return string,figure
    elif (len(activate)==1) & (fade==False):
        date_s = date_standard(date_s)
        date_e = date_standard(date_e)
        temp = date_filter(dt,date_list,date_s,date_e)
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
        if contain_alpha(date_s)==True:
            return True
        elif contain_alpha(date_e)==True:
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
                    {'Name':{'value':'\n\n![1999 Sirius Leonid Meteor](https://github.com/ShXIE-28/Meteor-Shower/blob/main/meteor%20pic/11-18-1999.jpg?raw=true)',
                            'type': 'markdown'}
                    },
                    {'Name':{'value':'![1998 Leonid meteor shower](https://github.com/ShXIE-28/Meteor-Shower/blob/main/meteor%20pic/11-17-1998.jpg?raw=true)',
                            'type': 'markdown'}
                    },
                    {'Name':{'value':'![1997 Southern delta-Aquarids](https://github.com/ShXIE-28/Meteor-Shower/blob/main/meteor%20pic/8-11-1997.jpg?raw=true)',
                            'type': 'markdown'}
                    },
                    {'Name':{'value':'![1993 Perseid meteor shower](https://github.com/ShXIE-28/Meteor-Shower/blob/main/meteor%20pic/8-12-1993.jpg?raw=true)',
                            'type': 'markdown'}
                    },
                    {'Name':{'value':'![2004 Perseid Meteor Shower](https://github.com/ShXIE-28/Meteor-Shower/blob/main/meteor%20pic/8-11-2004.jpg?raw=true)',
                            'type': 'markdown'}
                    },
                    {'Name':{'value':'![2001 Leonid Meteor Storm](https://github.com/ShXIE-28/Meteor-Shower/blob/main/meteor%20pic/11-18-2001.jpg?raw=true)',
                            'type': 'markdown'}
                    },
                    {'Name':{'value':'![2010 Perseid Meteor Storm](https://github.com/ShXIE-28/Meteor-Shower/blob/main/meteor%20pic/8_12_2010.jpg?raw=true)',
                            'type': 'markdown'}
                    },
                    {'Name':{'value':'![2002 Leonid meteor storm](https://github.com/ShXIE-28/Meteor-Shower/blob/main/meteor%20pic/11_19_2002.jpg?raw=true)',
                            'type': 'markdown'}
                    },
                ],
                tooltip_delay=0,
                tooltip_duration=None,
                style_data_conditional=[{
                    'if': {'column_id': 'Name'},
                    'textDecoration': 'underline',
                    'textDecorationStyle': 'dotted',
                }],
                style_cell={'textAlign': 'center'},
                style_as_list_view=True,
                style_header={'backgroundColor': '#cad7e8','fontWeight': 'bold'},
                style_table={'height': '400px', 'overflowY': 'auto'},
                virtualization = True
            )
        return table2
    elif list=='list3':
        table3 = dash_table.DataTable(
                data=future.to_dict("records"),
                columns=[{'id': c, 'name': c} for c in future.columns],
                style_cell={'textAlign': 'center'},
                style_as_list_view=True,
                style_header={'backgroundColor': '#cad7e8','fontWeight': 'bold'},
                style_table={'height': '400px', 'overflowY': 'auto'}
            )
        return table3
        
# zodiac sign
@app.callback(
        [Output("constellation","children"),
         Output("pic_title","children"),
         Output("zodiac_pic","src")],
        [Input("submit","n_clicks")],
        [State("month","value"),
         State("day","value")]
        )
def zodiac(n_click,month,day):
    sdate = [20,19,21,20,21,22,23,23,23,24,23,22]
    counts = ['Capricornus','Aquarius','Pisces','Aries','Taurus','Gemini',
              'Cancer','Leo','Virgo','Libra','Scorpio','Sagittarius']

    if int(day) < sdate[int(month)-1]:
        sign = counts[int(month)-1]
        i = int(month)-1
    else:
        sign = counts[int(month)]
        i = int(month)
    
    if i >= 3:
        i = i - 3
        symbol = chr(i + 9800)
    else:
        i = i + 9
        symbol = chr(i + 9800)
    
    str = "Your Zodiac Constellation is {} {}".format(sign,symbol)
    title = "Deep Sky Objects in {} (source: https://www.constellation-guide.com)".format(sign)
    src = zpic.loc[zpic['Name']==sign,'Website']
    
    return str,title,src
    
# Hubble collapse
@app.callback(
        [Output("collapse","is_open"),
         Output("card_header","children"),
         Output("card_text","children"),
         Output("card_link","href")],
        [Input("collapse_button","n_clicks"),
         Input("month","value"),
         Input("day","value")],
        [State("collapse", "is_open")]
        )
def collapse_open(n,month,day,is_open):
    
    header = "Date: "+str(month)+"/"+str(day)
    text=hubble.loc[(hubble['Month']==int(month))&(hubble['Day']==int(day)),'Caption']
    link=hubble.loc[(hubble['Month']==int(month))&(hubble['Day']==int(day)),'URL']

    if n:
        return (not is_open),header,text,link
    
    return is_open,header,text,link
    

if __name__ =='__main__':
    app.run_server(debug=False)