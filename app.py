import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output, State
import pandas as pd
import plotly as py
import plotly.graph_objs as go
import numpy as np


###### Define your variables #####
tabtitle = 'Marketing Campaign Analysis!'
color1='#92A5E8'
color2='#8E44AD'
sourceurl = 'https://www.kaggle.com/datasets'
githublink = 'https://github.com/nikhilamohan7/project-nm-8'


###### Import a dataframe #######
df = pd.read_csv('Data/marketing_campaign.csv')
df['TotalMntSpent'] = df['MntWines'] + df['MntFruits'] + df['MntMeatProducts'] + df['MntFishProducts'] + df['MntSweetProducts'] + df['MntGoldProds']
df['TotalNumPurchases'] = df['NumWebPurchases'] + df['NumCatalogPurchases'] + df['NumStorePurchases'] + df['NumDealsPurchases']
df['Total_Accepted_Offers'] = df['AcceptedCmp1'] + df['AcceptedCmp2'] + df['AcceptedCmp3'] + df['AcceptedCmp4'] + df['AcceptedCmp5'] + df['Response']
variables_list=['TotalMntSpent', 'TotalNumPurchases', 'Total_Accepted_Offers']

start_year = 1970
end_year = 1997         
df['Year_Category'] = np.where(df['Year_Birth']<start_year, f'<{start_year}',
np.where(df['Year_Birth']<end_year, f'{end_year} - 1999','other'))


########### Initiate the app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title=tabtitle

####### Layout of the app ########
app.layout = html.Div([
    html.H3('Choose a variable :'),
    dcc.Dropdown(
        id='dropdown',
        options=[{'label': i, 'value': i} for i in variables_list],
        value=variables_list[0]
    ),
    html.Br(),
    dcc.Graph(id='display-value'),
    html.A('Code on Github', href=githublink),
    html.Br(),
    html.A("Data Source", href=sourceurl),
])

    
######### Interactive callbacks go here #########
@app.callback(Output('display-value', 'figure'),
              [Input('dropdown', 'value')])
def display_value(continuous_var):
    grouped_count=df.groupby(['Year_Category','Education'])[continuous_var].mean()
    results=pd.DataFrame(grouped_count)
    
    # Create a grouped bar chart
    
    mydata1 = go.Bar(
        x=results.loc['<1970'].index,
        y=results.loc['<1970'][continuous_var],
        name='Birth : <1970',
        marker=dict(color=color1)
    )
    mydata2 = go.Bar(
        x=results.loc['1997 - 1999'].index,
        y=results.loc['1997 - 1999'][continuous_var],
        name='Birth: 1997 - 1999',
        marker=dict(color=color2)
    )
               
    mylayout = go.Layout(
        title='Metrics by Education level and birth year',
        xaxis = dict(title = 'Education Level'), # x-axis label
        yaxis = dict(title = str(continuous_var)) # y-axis label

    )
    fig = go.Figure(data=[mydata1, mydata2], layout=mylayout)
    return fig


######### Run the app #########
if __name__ == '__main__':
    app.run_server(debug=True)