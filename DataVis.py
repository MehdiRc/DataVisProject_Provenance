import base64
import datetime
import io

import itertools
from pprint import pprint

import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_table

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px

#!/usr/bin/env python
# coding: utf-8

from collections import namedtuple
import xml.etree.ElementTree as ET
import re


def parse_xml(file) :
    #action = action effectué, timestamp=timestamp(pour ordonner la structure), duration= durée de l'action, info=string(info variable suivant l'action).
    MyStruct = namedtuple("MyStruct", "action timestamp duration row column autre")

    list_user_initiated_action = ["Matrix_Select", "History_Select", "Lasso_Select", "Query_Select", "User_Evaluate", "SPLOM_Zoom", "Query_Create", "Queries_Clear", "History_Add", "History_Remove",\
                                    "Favourite_Select", "Favourite_Remove", "Favourite_Add", "Button_Evolve", "Button_Restart", "Button_Grid", "Button_Zoom", "Button_Jitter", "Button_Queries",\
                                    "Button_Labels", "Button_Hulls"]

    actions = []

    try:
        tree = ET.fromstring(str(file))
    except:
        print("file is not in a propper xml format")
        tree = ET.fromstring("<error><XmlSyntaxError>ERROR</XmlSyntaxError></error>")

    #get every user initiated actions contained in the XML file.
    for elem in tree.iter() :
        if elem.tag in list_user_initiated_action :
            timestamp = None
            duration  = None
            row       = None
            column    = None
            autre     = []

            for e in elem :
                if e.tag == "timestamp" :
                    timestamp = e.text
                elif e.tag == "duration" :
                    duration = e.text
                elif e.tag == "row" :
                    row = e.text
                elif e.tag == "column" :
                    column = e.text
                #every other info.
                else :
                    autre.append(e.text)

            actions.append(MyStruct(elem.tag, timestamp, duration, row , column, autre))

    actions.sort(key=lambda x: x.timestamp, reverse=False)
    return actions


#get a list of action from a list of "MyStruct"
def get_action(data) :
    action = []
    for i in data :
        action.append(i.action)
    return action

def get_dims(data) :
    dims = []
    for i in data :
        try:
            dim = i.row+" "+i.column
            dims.append(polyToDims(dim))
        except:
            pass
    return dims

def get_dimention(data):
    dim = []
    for i in data :
        dim.append(i.autre)
    return dim

def convertTuple(tup): 
    str =  ' '.join(tup) 
    return str

def polyToDims(poly):
    a = poly.split('+')

    dims   = re.findall ('[A-Z]+\d+|[a-zA-Z]+', poly )
    #print(dims)
    #found = []
    #for dim in dims:
    #   found.append(re.findall('-?\d+\.?\d+\s*\*\s*'+dim ,poly))
    dims.sort()
    return(dims)

def makeDictionary(number_of_collumns, actions):
    count = {}
    for i in range(len(actions)-number_of_collumns):
        tuple = ()
        for j in range(number_of_collumns):
            tuple += ((actions[i+j]),)
        if tuple not in count:
            count[tuple]=1
        else:
            count[tuple]+=1
    return count

def makeDimDictionary(number_of_collumns, dims):
    cumul = []
    count = {}
    for i in range(len(dims)-number_of_collumns):
        tempDims = []
        for j in range(number_of_collumns):
            tempDims.append(dims[i+j])
        combi = list(itertools.product(*tempDims))
        for tuple in combi:
            if tuple not in count:
                count[tuple]=1
            else:
                count[tuple]+=1
    return count



def tupleToList(dictContent):
    res = []
    for i in range(len(dictContent)):
        tup,counT = list(dictContent[i])
        l = list(tup)
        l.append(counT)
        res.append(l)
    return res

def showOnlyFilter(listOfTags, res):
    filtered = []
    temp = res
    for i in range(len(listOfTags)):
        
        for j in range(len(temp)):
            if (listOfTags[i] in temp[j]):
                filtered.append(temp[j])
            
        temp = filtered
        filtered = []
    return temp

def excludeFilter(listOfTags, res):
    filtered = []
    temp = res
    for i in range(len(listOfTags)):
        for j in range(len(temp)):
            if (listOfTags[i] not in temp[j]):
                filtered.append(temp[j])
        temp = filtered
        filtered = []
    return temp

def minMaxFilter(min,max,res):
    filtered = []
    for e in res:
        if e[-1]>= min and e[-1]<=max:
            filtered.append(e)
    return filtered

def noSameFilter(res):
    filtered = []
    for e in res:
        valid = True
        for i in range(len(e)-1):
            if(e[i] == e[i+1]):
                valid = False
                break
        if(valid):
            filtered.append(e)
    return filtered

def repeatForGraph(patternList):
    rep_res = []
    for i in range(len(patternList)):
        for j in range(patternList[i][-1]):
            rep_res.append(patternList[i])
    return rep_res




import pandas as pd
def makePandaDataFrame(number_of_collumns, rep_res):
    labels =[]
    for i in range(number_of_collumns):
        labels.append("action"+str(i+1))
    df = pd.DataFrame(rep_res, columns = labels+["counts"])
    return df, labels



import plotly.express as px

def makeGraph(df,labels):
    fig = px.parallel_categories(
        df, dimensions = labels ,color="counts", color_continuous_scale=px.colors.sequential.YlOrRd
        #,width =1000, height =1000
        )
    return fig



#data = parse_xml()
def generateGraph(file , number_of_collumns,showOnlyList,excludeList,min,max,noRepeat,actionOrDimension):
    
    if(showOnlyList == None):
        showOnlyList = []
    if(excludeList == None):
        excludeList = []

    if(min == None ):
        min = 1
    if(max == None ):
        max = 999

    
    data = parse_xml(file)

    if(actionOrDimension == "D"):
        dims = get_dims(data)
        count = makeDimDictionary(int(number_of_collumns), dims)
        
    else:
        actions = get_action(data)
        count = makeDictionary(int(number_of_collumns), actions)
        
    dictContent = list(count.items())
  
    res = tupleToList(dictContent)
  
    #Filtering
    res = minMaxFilter(int(min),int(max),res)
   
    if(noRepeat == ['Y']):
        res = noSameFilter(res)
    res = excludeFilter(excludeList , res)
    res =showOnlyFilter(showOnlyList, res)
   
    #putting in the right format for the graph
    rep_res = repeatForGraph(res) #repeating the content to get the right count
  
    df,labels = makePandaDataFrame(number_of_collumns, rep_res) #putting in a pandaDataframe
    
    return makeGraph(df,labels)





#####################################################################################################################################################################

#####################################################################################################################################################################


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

colors = {
    'background': '#11111',
    'text' : '7FDBFF'
}


hidden = html.Div([
#The whole interface
    html.Div([
        
        #part2: left div
        html.Div([
        	#compenent1: fileselect
        	html.Label('File Selection'),
            dcc.Upload(
        id='path-file',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        style={
            'width': '100%',
            'height': '50px',
            'lineHeight': '50px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '5px'
        },
        # Allow multiple files to be uploaded
        multiple=False
    ),


		    html.Label('Action Filter : Show Only'),
		    dcc.Dropdown(
		        id='show-only',
		        options=[

		            {'label': 'Matrix_Select', 'value': 'Matrix_Select'},
		            {'label': 'History_Select', 'value': 'History_Select'},
		            {'label': 'Lasso_Select', 'value': 'Lasso_Select'},
		            {'label': 'Query_Select', 'value': 'Query_Select'},
		            {'label': 'User_Evaluate', 'value': 'User_Evaluate'},
		            {'label': 'SPLOM_Zoom', 'value': 'SPLOM_Zoom'},
		            {'label': 'Query_Create', 'value': 'Query_Create'},
		            {'label': 'Queries_Clear', 'value': 'Queries_Clear'},
		            {'label': 'History_Add', 'value': 'History_Add'},
		            {'label': 'History_Remove', 'value': 'History_Remove'},
		            {'label': 'Favourite_Select', 'value': 'Favourite_Select'},
		            {'label': 'Favourite_Remove', 'value': 'Favourite_Remove'},
		            {'label': 'Favourite_Add', 'value': 'Favourite_Add'},
		            {'label': 'Button_Evolve', 'value': 'Button_Evolve'},
		            {'label': 'Button_Restart', 'value': 'Button_Restart'},
		            {'label': 'Button_Grid', 'value': 'Button_Grid'},
		            {'label': 'Button_Zoom', 'value': 'Button_Zoom'},
		            {'label': 'Button_Jitter', 'value': 'Button_Jitter'},
		            {'label': 'Button_Queries', 'value': 'Button_Queries'},
		            {'label': 'Button_Labels', 'value': 'Button_Labels'},
		            {'label': 'Button_Hulls', 'value': 'Button_Hulls'}
		        ],

		        multi=True,
		        style={'margin': '5px'}
		    ), 

	        html.Label('Action Filter (Exclude)'),
		    dcc.Dropdown(
		        id='exclude',
		        options=[

		            {'label': 'Matrix_Select', 'value': 'Matrix_Select'},
		            {'label': 'History_Select', 'value': 'History_Select'},
		            {'label': 'Lasso_Select', 'value': 'Lasso_Select'},
		            {'label': 'Query_Select', 'value': 'Query_Select'},
		            {'label': 'User_Evaluate', 'value': 'User_Evaluate'},
		            {'label': 'SPLOM_Zoom', 'value': 'SPLOM_Zoom'},
		            {'label': 'Query_Create', 'value': 'Query_Create'},
		            {'label': 'Queries_Clear', 'value': 'Queries_Clear'},
		            {'label': 'History_Add', 'value': 'History_Add'},
		            {'label': 'History_Remove', 'value': 'History_Remove'},
		            {'label': 'Favourite_Select', 'value': 'Favourite_Select'},
		            {'label': 'Favourite_Remove', 'value': 'Favourite_Remove'},
		            {'label': 'Favourite_Add', 'value': 'Favourite_Add'},
		            {'label': 'Button_Evolve', 'value': 'Button_Evolve'},
		            {'label': 'Button_Restart', 'value': 'Button_Restart'},
		            {'label': 'Button_Grid', 'value': 'Button_Grid'},
		            {'label': 'Button_Zoom', 'value': 'Button_Zoom'},
		            {'label': 'Button_Jitter', 'value': 'Button_Jitter'},
		            {'label': 'Button_Queries', 'value': 'Button_Queries'},
		            {'label': 'Button_Labels', 'value': 'Button_Labels'},
		            {'label': 'Button_Hulls', 'value': 'Button_Hulls'}
		        ],
		        multi=True,
		        style={'margin': '5px'}
		    ), 


		        ],style={'width': '57%', 'display': 'inline-block'}),
        

        #The rignt div
		html.Div([
	        html.Label('Graph Selection'),
			dcc.RadioItems(
			    id='graph-select',
			    options=[
			        {'label': 'Action Graph', 'value': 'A'},
			        {'label': 'Dimension Graph (Experimental - Resource Intensive )', 'value': 'D'}
			    ],
			    value='A',
		        style={
		            'width': '100%',
		            'height': '50px',
		            'margin': '5px'
		        }
			),		    


		    html.Label('Min/Max Counts'),
		    dcc.Input( id='min',value='0', type='number'),
		    dcc.Input( id='max',value='999', type='number'),

		    dcc.Checklist(
		    id='on-off',
		    options=[
		        {'label': 'Remove Loops on the Same Action', 'value': 'Y'}
		    ],
		    value=['Y',],
		    style={'margin': '5px'}
		)
		        ],style={'width': '35%', 'float': 'right', 'display': 'inline-block'}),
		        # style={'width': '48%', 'display': 'inline-block'}),


        html.Div([

		    html.Label('Pattern Length'),
		    dcc.Slider(
		        id='length-slider',
		        min=1,
		        max=11,
		        marks={i: '{}'.format(i) if i == 1 else str(i) for i in range(2, 11)},
		        value=5,
		        step=None
		    ),  

		]),



    ]),

])



app.layout = html.Div([
    html.Details([
        html.Summary('Show/Hide FILTERING OPTIONS', style = {'font-weight': 'bold', 'color': 'white', 'background-color' : '#505050' }),
        html.Div(hidden),
    ], open = 'open' ),
    
    html.Div(children= 'Visualizing Provenance to Support Exploratory Trade-off Analysis ', style={
        'textAlign': 'center',
        'color': colors['text'],
        'fontSize': 30
    }),
    dcc.Graph(id='graph'),

])



def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')
    
    
    try:
        if 'xml' in filename:
            decoded = base64.b64decode(content_string)
            return decoded
        else: 
            return b""
    except Exception as e:
        return b""


@app.callback(
    Output('graph', 'figure'),
    
    [Input('path-file', 'contents'),
    Input('path-file', 'filename'),
    Input('path-file', 'last_modified'),
    Input('length-slider', 'value'),
    Input('show-only','value'),
    Input('exclude', 'value'),
    Input('min', 'value'),
    Input('max', 'value'),
    # Input('minmax','value'),
    # Input('minmax','value'),
    Input('on-off', 'value'),
    Input('graph-select', 'value')])
   
def update_figure(list_of_contents, list_of_names, list_of_dates,selected_length,selected_show_only, selected_exclude,min ,max , noRepeat , selected_actionOrDimension):

    if(list_of_contents != None and list_of_names != None and list_of_dates != None ):
        parse = parse_contents(list_of_contents, list_of_names, list_of_dates).decode("utf-8")
        graph = generateGraph(parse,selected_length,selected_show_only, selected_exclude,min ,max , noRepeat , selected_actionOrDimension)
    else:
        parse = None
        return {}
         
    return graph



if __name__ == '__main__':
    app.run_server(debug=True)