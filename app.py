####IMPORTS####
import pandas as pd
import dash
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash_table.Format import Format
import dash_table.FormatTemplate as FormatTemplate
from dash.dependencies import Input, Output, State

####END IMPORTS####

# let's get our file sources
file1 = "my_evidence.csv" #this is model data
file2 = "finalmydata.csv" 
file3 = "export_dataframe_final.xlsx" 
file4 = "final_export_combined.csv" 

# We cannot pull from a url. plus, we already have my_evidence.csv local to our project. just use file1 variable that we created earlier
# url_1=('https://github.com/asquires11/flying-dog-beers/blob/master/my_evidence.csv') #this is model data
df = pd.read_csv(file1) # csv to pandas
df = df[['tweet', 'Predicted Name', 'Predicted Confidence']] 

PAGE_SIZE=10
           
# We're not going to use this definition
# df_2=('https://github.com/asquires11/flying-dog-beers/blob/master/finalmydata.csv')# this is location data for members AND has number of members per county

df_2=pd.read_csv(file2)


# url_4='https://github.com/asquires11/flying-dog-beers/blob/master/export_dataframe_final.xlsx'
url_4=pd.read_excel(file3) #this is full data with locations and messages

url_5=pd.read_csv(file4)

url_6=url_5[['tweet','Predicted Name','Predicted Confidence','msg_date','name','city',"state_name"]]

url_6=url_6.rename(columns={'tweet':'Post','Predicted Name':'Predicted Topic','msg_date':'Date','name':'Member','state_name':'State'})

mapbox_access_token = 'pk.eyJ1Ijoic3F1aXJlc2EiLCJhIjoiY2s5dndvcjVzMDAyNDNkb2U0aGpmNzFxdSJ9.nVR1tUP7zQvtamST9ISryQ'


url_5= url_5.rename(columns={"postal num":'postal'})


url_5postal=url_5['postal']
fig = go.Figure(go.Scattermapbox(
    
        lat=url_5['lat'],
        lon=url_5['lon'],
        #color_continuous_scale=px.colors.cyclical.IceFire,
        #color=df_2['postal.num'],
        mode='markers', 
        #x=url_5['postal'],
        #colors='Reds',
        marker=go.scattermapbox.Marker(
            size=url_5['postal']*5,
            
            color='white'
        ),opacity=.3,
    
        #fillcolor='yellow',
        text=(url_5['City']),
        #text=site_text,
        hoverinfo='text',
        hovertemplate="<b>%{text}</b><br>",
    ))

fig.update_layout(
    
    
    
    
   ### title={
       # 'text': "Iron March Member Locations US",
       # 'y':0.9,
       # 'x':0.5,
       # 'xanchor': 'center',
      #  'yanchor': 'top',},
      #  font= dict(family='Georgia', 
                 # color='#FFFEF2'),
    
   
    
                                
 
    
    hovermode='closest',
    paper_bgcolor='rgb(0,0,0,0)',
    plot_bgcolor='rgb(0,0,0,0)',
    
    
   
    #autosize=True,
    
    margin=dict(t=0, b=0, l=0, r=0),
    mapbox=dict(
        accesstoken=mapbox_access_token,
        bearing=0,
        center=go.layout.mapbox.Center(
            lat=38.822591,
            lon=-84.370789
        ),
        #pitch=0,
        zoom=3,
        style='dark'
    )
)
    
s_2 = url_5['msg_date'].value_counts() ## Counts the occurrence of unqiue elements and stores in a variable called "s" which is series type
new_2 = pd.DataFrame({'FuncGroup':s_2.index, 'Count':s_2.values})

new_2=new_2.sort_values(by='FuncGroup') 

fig_2=go.Figure()
fig_2.add_trace(go.Scatter( x=new_2['FuncGroup'], y=new_2['Count'],
                         
                       
                        line=dict(color='grey',width=2))),



#fig = go.Figure([go.Scatter( x=new_2['FuncGroup'], y=new_2['Count'])]),

fig_2.update_layout( margin=dict(t=0, b=0, l=0, r=0),
    hovermode='closest',
    paper_bgcolor= '#323232',
    plot_bgcolor='#323232',
   
    )

#fig_2.show()  
navbar = dbc.NavbarSimple(
       children=
        [
        dbc.Button("About",id="open",size='small',color='secondry'),#,size='small'),
        dbc.Modal(
            [
                dbc.ModalHeader('About'),
                dbc.ModalBody(html.Div([
                        html.H1("About Iron March"),
                        html.Div([
                        ###html.P('Dash converts Python classes into HTML'),
                        html.P('This dashboard presents an analysis of the Iron March data hack. Iron March was a white supremacist forum created in 2011 by Russian nationalist Alexander “Slavros” Mukhitdinov, the site closed without explanation in late 2017.  Following the sites closing,  the entire SQL database was dumped anonymously on Internet Archives. Iron March acted as a hub for Neo-Nazi’s and violent extremist. The website had approximately 1,200 users worldwide and was affiliated with at least nine different Neo-Nazi groups. One such group Atomwaffen Division  has been tied to three murders and a terror plot. ')
                        
    ]),
                        html.H1('Location Processing' ),
                        html.Div([
                        html.P('The Iron March archive details the ip address and message posts for all users. Using Python and an ip address convertor my first goal was to understand where the members were located. I specifically focused on U.S members and was able to get location variables to the individual zip code level. The dashboard’s map presents the members locations by city. In the data table below, you can choose a county name to see all posts from that location. Aggregating the data by county level allows a closer examination of the messsage content.')
                        ]),
                        html.H1('Date Analysis'),
                        html.Div([
                        html.P(' The plotly graph in the upper lefthand column is a breakdown of membership enrollment by month and year. These dates were obtained by converting timestamps of account creation to date time objects.')
                        ]),
                        html.H1('The Text Process'),
                        html.Div([
                        html.P('My main goal for the data was to perform textual analysis through NLP (Natural Language Processing). To do this I cleaned my datasets in both R and Python. In R I used Ken Benoit’s package quanteda as well as tidy text to clean,  and tokenize the forum posts. I created a corpus and dtm (document term matrix) which then allowed me to start doing some analysis. In Python my goal was to create a model to predict the topic of each message post from a potential list of 6 topics:  origin, disability, other, gender, sexual orientation, religion. This was an incredibly difficult process using multiple datasets and weeks of coding. As I did not have coders readily available to use as a train set I had to find a previously coded set of twitter hate speech data. I created a dataset combining the iron march and the coded data, which was the split into a train and test corpus using sk.learn. The train corpus was made up of 4,977 hate tweets, the test corpus had 2,452. I subsequently created a bag of words model vectorizing the text of each corpus. I then ran both the test and train data through 5 different models: Naive Bayes,Logistic Regression, Support Vector Machines SVM with Stochastic Gradient Descent, Random Forest and Gradient Boosting to see which would give the most accurate classifications. After this first round I trained the datasets using Gensim word2vec to generate document level embeddings as up until this point only vocabulary embeddings had been analyzed. I then tuned each model to evaluate which would provide the most accurate results. While none of the models were incredibly accurate ,(due to the improvising in manual coding rather than training and testing from only the Iron March dataset) my tuning of the Logistic Regression model returned the highest test accuracy. I then used the LR model to predict the topic of each Iron March message. The predicted topics as well as Predicted Confidence level  can be seen in the data table.')
                        ])
                        
                        
])),
                dbc.ModalFooter(
                    dbc.Button("Close", id="close", className="ml-auto",color='secondary')
                ),
            ],
            id="modal",
            scrollable=True,
        ),
           # nav=True,
           # in_navbar=True,
           #label="More",
    
        ],
    #className="ml-2",
    brand="Iron March Hack",
    
    #brand_href="About",
    #font_size='100px',
    #id="navbarColor02",
    color="Secondary",
    dark=True,
    className='navbar navbar-expand-lg navbar-dark bg-primary',
    fluid=True,
    #label=

    
            #no_gutters=True,
   
    
   
)

#######################################
# 
#     layout
#
######################################
    
h_style = {
    "display": "flex",
    "flex-direction": "row",
    "alignItems": "center",
    "justifyContent": "space-between",
    "margin": "5px",
}

mgrs = sorted(url_6['city'].unique())

def generate_table(dataframe, max_rows=10):
    return dbc.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))],
        bordered=False,
        
        
    )


app = dash.Dash(external_stylesheets=[dbc.themes.SLATE
])



column_1 = dbc.Card(
    dbc.CardBody(
    [
    html.H4("Time Series"),
    dcc.Graph(figure=fig,style={'width':'100%','height': 500,'backgroundColor':'Primary'}),
          
       
    ]),
    outline=False
    
)

column_23 = dbc.Card( 
    
    dbc.CardBody(
        [ 
           html.H4("US Member Locations"),
    #dbc.CardHeader("US Member Locations"),
            dcc.Graph(id='first',      
                animate=True,
                figure=fig,style={'width':'100%','height': 500,'backgroundColor':'Primary'},

        
                    
             )
])
    
)




column_2 = [
   # html.H4("US Member Locations"),
    dbc.CardHeader("US Member Locations"),
    dcc.Graph(id='first',      
        animate=True,
        figure=fig,style={'width':'100%','height': 500,'backgroundColor':'Primary'},
    
        
                    
             )
]



column_3=html.Div([
    html.Hr(),
    dbc.Card(
        #dbc.CardHeader(['Select a County to See the Data: ']),
        
        dbc.CardBody([
            html.H5("Select a County to See the Data:", className="card-title"),
            dcc.Dropdown(
                id='mgr-dropdown',
                options=[
                    {'label': mgr, 'value': mgr} for mgr in mgrs
                ],
                value='',
                searchable=True,
                #multi=True,

                style={'backgroundColor': 'Primary','width':'100%'}),
                #className='stockselector',

       
        ])),
    html.Hr(),
    dbc.Card(
        dbc.CardBody([
        html.Div(id='table-container',style={'backgroundColor':'Secondary'})
        ]))
   
]),


column_4 = dbc.Card(
    dbc.CardBody(
    [
    html.H4("Time Series"),
    dcc.Graph(figure=fig_2,style={'width':'100%','height': 500,'backgroundColor':'Primary'}),
          
       
    ]),
    outline=True
    
)

column_44 = [
    
    #html.Br(),
    #html.H4("Graph"),
    dcc.Graph(id='third',      
        animate=True,
        figure=fig_2,style={'width':'100%','height': 500})
]


column_5=[
    #html.H1('My first app with folium map'),
    #html.Iframe(id='graph', srcDoc=open('/Users/annikasquires/Desktop/Desktop - Annika’s MacBook Pro/Beck Hacking/test_world_map.html', 'r').read(), width='100%', height='500', style={'paper_bgcolor':'rgba(0,0,0,0)','plot_bgcolor':'Primary'})
    #html.Button(id='map-submit-button', n_clicks=0, children='Submit')
]

##navbar = dbc.NavbarSimple(
   
   # children=[
     #   dbc.NavItem(dbc.NavLink("Page 1", href="#")),
       # dbc.DropdownMenu(
          #  children=[
           #     dbc.DropdownMenuItem("More pages", header=True),
               # dbc.DropdownMenuItem("Page 2", href="#"),
               # dbc.DropdownMenuItem("Page 3", href="#"),
           # ],
            #nav=True,
           # in_navbar=True,
           #label="More",
            #no_gutters=True,
        
            
        #),
   # ],
    #brand="Iron March Hack",
    #3brand_href="#",
   # id="navbarColor02",
    #color="primary",
   # dark=True,
    #no_gutters=True
#)


body = dbc.Container(
    [  ## html.H1('Iron March Hack'),
     
        
        #html.Hr(),
        dbc.Row(
            [html.Br(),
             
                dbc.Col(column_4,md=6,className="my-4"),
                html.Br(),
                #html.hr(),
                dbc.Col(column_23,md=6,className="my-4"),
                #html.Br(),
                #dbc.Col(column_2,md=3)
            ],
            #no_gutters=True,
            align="start",
            
            style={
                       # "margin": "50px",
                       # "display": "flex",
                       # "flex-direction": "column",
                        #"alignItems": "center",
                        "justifyContent": "space-between",}
                        #"border": "2px solid #C8D4E3",}
                        #"background": "#f2f5fa",}
        ),
     
        dbc.Row(),
        
        dbc.Row(
        
            [
                #CHANGIANGI THIS FROM DBC.COL TO DBC.TALBE and taking awayy md=12
                dbc.Col(column_3),
                #dark=True,
                ##hover=True),
                #responsive=True),
                #striped=True),
            ],
           
        
        ),
      
    ],
   
   
    fluid=True,
)
                     
    
#("start": "node server.js")

app.layout = html.Div([navbar,body])


@app.callback(
    dash.dependencies.Output('table-container', 'children'),
    [dash.dependencies.Input('mgr-dropdown', 'value')])
def gen_table(dropdown_value):
    is_Manager = url_6['city']==dropdown_value
    # Create dataframe of those rows only by passing in those booleans
    dff = url_6[is_Manager] # dff as in dataframe filtered
    return dbc.Table(
    # Header
    [html.Tr([html.Th(col) for col in dff.columns],className='table-dark')] +

    # Body
    [html.Tr([
        html.Td(dff.iloc[i][col]) for col in dff.columns
    ]) for i in range(min(len(dff), 20))
     
    ],
        
    #style={'backgroundColor':'rgb(70,70,70)',
         # 'color':'white', 'fontFamily': ' Harmonica Sans',}
                   
    
    )



@app.callback(
    Output("modal", "is_open"),
    [Input("open", "n_clicks"), Input("close", "n_clicks")],
    [State("modal", "is_open")],
)

def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open


if __name__ == '__main__':
    app.run_server(host='127.0.0.1',debug=False)
