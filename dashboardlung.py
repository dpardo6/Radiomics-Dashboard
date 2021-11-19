import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import pandas as pd
import numpy as np

from datetime import datetime as dt
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff



# Load Data
df = pd.read_excel(r'C:\Users\pardo\OneDrive\Desktop\AI Lab Play Data\Data\LungDataBatch1_2.xlsx')

# Load Chief Complaint List
Unique_identifiers = ['median_LawsW5E5', 'var_HaralickCorrelationWs_7', 'median_LawsS5W5', 'var_HaralickEnergyWs_5', 'median_RawIntensity', 'skewness_GaborXY___0_785___1_276_BW_1',
                        'var_HaralickEntropyWs_3', 'var_HaralickDiff_entWs_3', 'var_HaralickCorrelationWs_5', 'skewness_RawIntensity', 'kurtosis_HaralickInfo1Ws_7', 'median_GradientSobelx', 'median_HaralickInertiaWs_3',
                        'kurtosis_HaralickInfo2Ws_3', 'var_HaralickCorrelationWs_3', 'median_HaralickSum_avWs_3', 'median_GradientX', 'kurtosis_GrayStd_devWs_3', 'median_LawsL5S5', 'kurtosis_GaborXY___1_963___1_276_BW_1']

 
# Load Axes Options
Axes = Unique_identifiers

# Load Stat Value List
Stat_unique = ['TotalScore', 'Age']

# Sex Value
Sex = ['Male', 'Female', 'All']

# Color Code Values
Color = ['Mortality', 'TotalScore']

# Create App
app = dash.Dash(__name__)


# App Layout
app.layout = html.Div(children=[

    # Title of Page
    html.Div(children=[
        html.H3(children='Radiomic Features Dashboard'),
        # html.H4(children='Patient Overview', style={'marginTop': '-1.5rem'})
    ], style={'textAlign': 'center', 'marginTop': '5rem', 'color': 'white'}),
   
   
    # First Row Items
    html.Div(children=[

        # Data Filter Box #
        html.Div(children=[
            html.Label('Filter by Age:', style={'paddingTop': '4rem'}),
            dcc.RangeSlider(
                    id='age_slider',
                    min=0,
                    max=100,
                    step=10,
                    value=[20, 70],
                    marks={
                        0: '0',
                        10: '10',
                        20: '20',
                        30: '30',
                        40: '40',
                        50: '50',
                        60: '60',
                        70: '70',
                        80: '80',
                        90: '90',
                        100: '100'
                    },
            ),
            html.Label('Filter by Score:', style={'paddingTop': '4rem'}),
            dcc.RangeSlider(
                    id='score_slider',
                    min=0,
                    max=12,
                    step=1,
                    value=[0, 12],
                    marks={
                        0: '0',
                        1: '1',
                        2: '2',
                        3: '3',
                        4: '4',
                        5: '5',
                        6: '6',
                        7: '7',
                        8: '8',
                        9: '9',
                        10: '10',
                        11: '11',
                        12: '12',
                    },
            ),
            html.Label('Filter by Sex:', style={'paddingTop': '2rem'}),
            dcc.Dropdown(
                id="Sex_unique",
                options=[
                    {'label': 'Male & Female', 'value': 'Male & Female'},
                    {'label': 'Female', 'value': 'Female'},
                    {'label': 'Male', 'value': 'Male'}
                ],
                value= 'Male & Female',
                className="dcc_control",
                clearable = False,               
            ),
            html.Label('Filter by Mortality:', style={'paddingTop': '2rem'}),
            dcc.Dropdown(
                id="Mortality",
                options=[
                    {'label': 'Alive & Deceased', 'value': 'Alive & Deceased'},
                    {'label': 'Alive', 'value': 'Alive'},
                    {'label': 'Deceased', 'value': 'Deceased'}
                ],
                value= 'Alive & Deceased',
                className="dcc_control",
                clearable = False,               
            ),
        ], className="three columns", style={'padding':'2rem', 'margin-left':'20rem', 'border-radius': '1rem', 'marginTop': '5rem', 'boxShadow': '#4b575e 4px 4px 2px', 'backgroundColor': 'white'}),
        
        # Graph Customization Box #
        html.Div(children=[
            html.Div(children=[
                html.H5(children='Customize Visualization:'),
            ], style={'textAlign': 'center'}
            ),
            html.Label('Change Stat Box Value:'),
            dcc.Dropdown(
                id="Stat_unique",
                options=[{"label": x, "value": x} for x in sorted(Stat_unique)],
                value= Stat_unique[1],
                className="dcc_control",
                clearable = False,
            ), 
            html.Label('Change Graph:', style={'paddingTop': '2rem'}),
            dcc.Dropdown(
                id="Graph_unique",
                options=[{'label': 'Scatter Plot', 'value': 'Scatter'}, {'label': 'Box Plot', 'value': 'Box'}],
                value='Scatter',
                className="dcc_control",
                clearable = False,
            ),
            # Collapse Button 1            
            dbc.Button(
                "Customize Scatter Plot",
                id="collapse-button",
                className="mb-3",
                color="primary",
                n_clicks=0,
                style={'marginTop': '2rem'}  ,
            ),
            dbc.Collapse(
                dbc.Card(dbc.CardBody(
                        html.Div(children=[
                            html.Label('Filter Data:', style={'paddingTop': '1rem'}),
                            dcc.Dropdown(
                                id="color",
                                options=[{"label": x, "value": x} for x in sorted(Color)],
                                className="dcc_control",
                                placeholder="color code",
                                value=Color[0],
                                style={'marginTop': '5px'}                
                            ),
                            html.Label('X Axis:', style={'paddingTop': '1rem'}),            
                            dcc.RadioItems(
                                id='crossfilter-xtype',
                                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                                value='Linear',
                                labelStyle={'display': 'inline-block', 'marginTop': '5px'}
                            ),            
                            dcc.Dropdown(
                                id="x_axis1",
                                options=[{"label": x, "value": x} for x in sorted(Axes)],
                                className="dcc_control",
                                value=Axes[0],
                                placeholder="x-axis",              
                            ),
                            html.Label('Y Axis:', style={'paddingTop': '1rem'}),    
                            dcc.RadioItems(
                                id='crossfilter-ytype',
                                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                                value='Linear',
                                labelStyle={'display': 'inline-block', 'marginTop': '5px'}
                            ),
                            dcc.Dropdown(
                                id="y_axis1",
                                options=[{"label": x, "value": x} for x in sorted(Axes)],
                                className="dcc_control",
                                value=Axes[0],
                                placeholder="y-axis",
                            ),
                        ]),
                    )
                ),
                id="collapse",
                is_open=False,
            ),
            # Collapse Button 2
            dbc.Button(
                "Customzie Box Plot",
                id="collapse-button2",
                className="mb-3",
                color="primary",
                n_clicks=0,
                style={'marginTop': '1rem'}  ,
            ),            
            dbc.Collapse(
                dbc.Card(dbc.CardBody(
                        html.Div(children=[
                            html.Label('Filter Data:', style={'paddingTop': '1rem'}),
                            dcc.Dropdown(
                                id="color2",
                                options=[{"label": x, "value": x} for x in sorted(Color)],
                                className="dcc_control",
                                placeholder="color code",
                                value=Color[0],
                                style={'marginTop': '5px'}                
                            ),               
                            html.Label('X Axis:', style={'paddingTop': '1rem'}),   
                            dcc.RadioItems(
                                id='crossfilter-xtype2',
                                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                                value='Linear',
                                labelStyle={'display': 'inline-block', 'marginTop': '5px'}
                            ),            
                            dcc.Dropdown(
                                id="x_axis2",
                                options=[{"label": x, "value": x} for x in sorted(Color)],
                                className="dcc_control",
                                value=Color[0],
                                placeholder="x-axis",              
                            ),
                            html.Label('Y Axis:', style={'paddingTop': '1rem'}),  
                            dcc.RadioItems(
                                id='crossfilter-ytype2',
                                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                                value='Linear',
                                labelStyle={'display': 'inline-block', 'marginTop': '5px'}
                            ),
                            dcc.Dropdown(
                                id="y_axis2",
                                options=[{"label": x, "value": x} for x in sorted(Axes)],
                                className="dcc_control",
                                value=Axes[0],
                                placeholder="y-axis",
                            ),
                        ]),
                    )
                ),
                id="collapse2",
                is_open=False,
            ),                      
        ], className="three columns", style={'padding':'2rem', 'border-radius': '1rem', 'marginTop': '5rem', 'margin-bottom': '10rem', 'boxShadow': '#4b575e 4px 4px 2px', 'backgroundColor': 'white'}),
        
        # Statistic Boxes 1st Column
        html.Div(children=[
            html.Div(children=[
                html.H2(id='stat_1'),
                html.Label('No. of Patients'),
            ], id = "statbox_1", style={'padding': '2.5rem', 'border-radius': '1rem', 'margin-left': '3rem', 'boxShadow': '#4b575e 4px 4px 2px', 'backgroundColor': 'white'}),
            
            html.Div(children=[
                html.H2(id='stat_2'),
                html.Label(id='stat_name2'),
            ], id = "statbox_2", style={'padding': '2.5rem', 'border-radius': '1rem', 'margin-left': '3rem', 'marginTop': '1.5rem', 'boxShadow': '#4b575e 4px 4px 2px', 'backgroundColor': 'white'}),   
        ], className="two columns", style={'marginTop': '5rem', 'margin-left':'2rem'}),
        
        # Statistic Boxes 2nd Column
        html.Div(children=[
            html.Div(children=[
                html.H2(id='stat_3'),
                html.Label(id='stat_name3'),
            ], id = "statbox_3", style={'padding': '2.5rem', 'border-radius': '1rem', 'margin-left': '3rem', 'boxShadow': '#4b575e 4px 4px 2px', 'backgroundColor': 'white'}),
            
            html.Div(children=[
                html.H2(id='stat_4'),
                html.Label(id='stat_name4'),
            ], id = "statbox_4", style={'padding': '2.5rem', 'border-radius': '1rem', 'margin-left': '3rem', 'marginTop': '1.5rem', 'boxShadow': '#4b575e 4px 4px 2px', 'backgroundColor': 'white'}),    
        ], className="two columns", style={'marginTop': '5rem', 'margin-left': '-1rem'}),
    ], style={'margin-bottom': '25rem'}),
    
    # Second Row Items
    html.Div(children=[   
        
        # Graph 1
        html.Div([
            dcc.Graph(id="graph_1")
        ], className="seven columns", style={'display': 'inline-block', 'padding':'2rem', 'margin-left':'5rem', 'border-radius': '1rem', 'boxShadow': '#4b575e 4px 4px 2px', 'backgroundColor': 'white'}),
        
        # Xray Photo
        html.Div(
            html.Img(id="img_1", style={'height':'440px', 'width':'100%'})
        , className="four columns", style={'display': 'inline-block', 'padding':'2rem', 'border-radius': '1rem', 'boxShadow': '#4b575e 4px 4px 2px', 'backgroundColor': 'white'})     
    ]),  
])

# Update Collapse 1
@app.callback(
    Output("collapse", "is_open"),
    [Input("collapse-button", "n_clicks")],
    [State("collapse", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open
    
# Update Collapse 2
@app.callback(
    Output("collapse2", "is_open"),
    [Input("collapse-button2", "n_clicks")],
    [State("collapse2", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


# Update Statistic Box 1
@app.callback(
    Output("stat_1", "children"),
    [
        Input("age_slider", "value"),
        Input("Sex_unique", "value"),
        Input("Mortality", "value"),
        Input("score_slider", "value"),
    ],
)
def update_stat1(slider_range,sex,mortality,score):
    # Parse DataFrame for Age
    low, high = slider_range
    mask = (df['Age'] >= low) & (df['Age'] <= high)
    df1 = df[mask]
    # Parse DataFrame for Score
    low, high = score
    mask = (df1['TotalScore'] >= low) & (df1['TotalScore'] <= high)
    df2 = df1[mask]
    # Parse DataFrame for Sex
    if sex == 'Male & Female':
        df3 = df2
    elif sex == 'Male':
        df3 = df2[df2['Sex'] == 0]
    elif sex == 'Female':
        df3 = df2[df2['Sex'] == 1]
    # Parse DataFrame for Mortality
    if mortality == 'Alive & Deceased':
        number = df3.shape[0]
        return number
    elif mortality == 'Alive':
        df4 = df3[df3['Mortality'] == 0]
        number = df4.shape[0]
    elif mortality == 'Deceased':
        df4 = df3[df3['Mortality'] == 1]
        number = df4.shape[0] 
    return number


# Update Statistic Box 2
@app.callback(
    Output("stat_2", "children"),
    [
        Input("age_slider", "value"),
        Input("Stat_unique", "value"),
        Input("Sex_unique", "value"),
        Input("Mortality", "value"),
        Input("score_slider", "value"),        
    ],
)
def update_stat2(slider_range,stat_column,sex,mortality,score):
    # Parse DataFrame for Age
    low, high = slider_range
    mask = (df['Age'] >= low) & (df['Age'] <= high)
    df1 = df[mask]
    # Parse DataFrame for Score
    low, high = score
    mask = (df1['TotalScore'] >= low) & (df1['TotalScore'] <= high)
    df2 = df1[mask]    
    # Parse DataFrame for Sex
    if sex == 'Male & Female':
        df3 = df2
    elif sex == 'Male':
        df3 = df2[df2['Sex'] == 0]
    elif sex == 'Female':
        df3 = df2[df2['Sex'] == 1]
    # Parse DataFrame for Mortality
    if mortality == 'Alive & Deceased':
        number = df3[stat_column].mean()
        number = number.round(1)
        return number
    elif mortality == 'Alive':
        df4 = df3[df3['Mortality'] == 0]
        number = df4[stat_column].mean()
        number = number.round(1)
    elif mortality == 'Deceased':
        df4 = df3[df3['Mortality'] == 1]
        if df4.shape[0] == 0:
            number = 0
        else:
            number = df4[stat_column].mean()
            number = number.round(1)
    return number

# Update Statistic Box 2 Name
@app.callback(
    Output("stat_name2", "children"),
    [
        Input("Stat_unique", "value"),
    ],
)
def update_stat_name2(stat2_name):
    name2 = ("Avg ",stat2_name)
    return name2


# Update Statistic Box 3
@app.callback(
    Output("stat_3", "children"),
    [
        Input("age_slider", "value"),
        Input("Stat_unique", "value"),
        Input("Sex_unique", "value"),
        Input("Mortality", "value"),
        Input("score_slider", "value"),
    ],
)
def update_stat2(slider_range,stat_column,sex,mortality,score):
    # Parse DataFrame for Age
    low, high = slider_range
    mask = (df['Age'] >= low) & (df['Age'] <= high)
    df1 = df[mask]
    # Parse DataFrame for Score
    low, high = score
    mask = (df1['TotalScore'] >= low) & (df1['TotalScore'] <= high)
    df2 = df1[mask]
    # Parse DataFrame for Sex
    if sex == 'Male & Female':
        df3 = df2
    elif sex == 'Male':
        df3 = df2[df2['Sex'] == 0]
    elif sex == 'Female':
        df3 = df2[df2['Sex'] == 1]
    # Parse DataFrame for Mortality
    if mortality == 'Alive & Deceased':
        number = df3[stat_column].max()
        number = number.round()
        return number
    elif mortality == 'Alive':
        df4 = df3[df3['Mortality'] == 0]
        number = df4[stat_column].max()
        number = number.round()
    elif mortality == 'Deceased':
        df4 = df3[df3['Mortality'] == 1]
        if df4.shape[0] == 0:
            number = 0
        else:
            number = df4[stat_column].max()
            number = number.round()
    return number
    

# Update Statistic Box 3 Name
@app.callback(
    Output("stat_name3", "children"),
    [
        Input("Stat_unique", "value"),
    ],
)
def update_stat_name2(stat3_name):
    name3 = ("Max ",stat3_name)
    return name3


# Update Statistic Box 4
@app.callback(
    Output("stat_4", "children"),
    [
        Input("age_slider", "value"),
        Input("Stat_unique", "value"),
        Input("Sex_unique", "value"),
        Input("Mortality", "value"),
        Input("score_slider", "value"),        
        
    ],
)
def update_stat2(slider_range,stat_column,sex,mortality,score):
    # Parse DataFrame for Age
    low, high = slider_range
    mask = (df['Age'] >= low) & (df['Age'] <= high)
    df1 = df[mask]
    # Parse DataFrame for Score
    low, high = score
    mask = (df1['TotalScore'] >= low) & (df1['TotalScore'] <= high)
    df2 = df1[mask]    
    # Parse DataFrame for Sex
    if sex == 'Male & Female':
        df3 = df2
    elif sex == 'Male':
        df3 = df2[df2['Sex'] == 0]
    elif sex == 'Female':
        df3 = df2[df2['Sex'] == 1]
    # Parse DataFrame for Mortality
    if mortality == 'Alive & Deceased':
        number = df3[stat_column].std()
        number = number.round(1)
        return number
    elif mortality == 'Alive':
        df4 = df3[df3['Mortality'] == 0]
        number = df4[stat_column].std()
        number = number.round(1)
    elif mortality == 'Deceased':
        df4 = df3[df3['Mortality'] == 1]
        if df4.shape[0] == 0:
            number = 0
        else:
            number = df4[stat_column].std()
            number = number.round(1)
    return number

# Update Statistic Box 4 Name
@app.callback(
    Output("stat_name4", "children"),
    [
        Input("Stat_unique", "value"),
    ],
)
def update_stat_name2(stat4_name):
    name4 = ("STDV ",stat4_name)
    return name4



# Update Graph
@app.callback(
    Output("graph_1", "figure"),
    [
        Input("age_slider", "value"),
        Input("Sex_unique", "value"),
        Input("x_axis1", "value"),
        Input("y_axis1", "value"),
        Input("x_axis2", "value"),
        Input("y_axis2", "value"),
        Input("crossfilter-xtype", "value"),
        Input("crossfilter-ytype", "value"),
        Input("crossfilter-xtype2", "value"),
        Input("crossfilter-ytype2", "value"),
        Input("Mortality", "value"),
        Input("color", "value"),
        Input("color2", "value"),
        Input("score_slider", "value"),
        Input("Graph_unique", "value"),
    ]
)
def update_stat2(slider_range,sex,x1_axis,y1_axis,x2_axis,y2_axis,crossfilter_x,crossfilter_y,crossfilter_x2,crossfilter_y2,mortality,colorcode,colorcode2,score,graph_unique):
    if graph_unique == 'Scatter':
        # Parse DataFrame for Age
        low, high = slider_range
        mask = (df['Age'] >= low) & (df['Age'] <= high)
        df1 = df[mask]
        # Parse DataFrame for Score
        low, high = score
        mask = (df1['TotalScore'] >= low) & (df1['TotalScore'] <= high)
        df2 = df1[mask]
        # Parse DataFrame for Sex
        if sex == 'Male & Female':
            df3 = df2
        elif sex == 'Male':
            df3 = df2[df2['Sex'] == 0]
        elif sex == 'Female':
            df3 = df2[df2['Sex'] == 1]
        # Parse DataFrame for Mortality
        if mortality == 'Alive & Deceased':
            df4 = df3
        elif mortality == 'Alive':
            df4 = df3[df3['Mortality'] == 0]
        elif mortality == 'Deceased':
            df4 = df3[df3['Mortality'] == 1]
        # Create Bar Graph
        if df4.shape[0] == 0:
            fig = px.scatter()
        else:
            df4["Mortality"] = df4["Mortality"].astype(str)
            df4["TotalScore"] = df4["TotalScore"].astype(str)        
            fig = px.scatter(df4, x = (x1_axis), y = (y1_axis), trendline = "ols", trendline_scope = "overall", trendline_color_override = "grey", hover_name= "MRNs", color = colorcode)
            fig.update_layout(title_text='Scatter Plot:', title_x=0.5)
            # Update Axes based on Linear or Log
            fig.update_xaxes(type='linear' if crossfilter_x == 'Linear' else 'log')
            fig.update_yaxes(type='linear' if crossfilter_y == 'Linear' else 'log')
            # Update Margin
            fig.update_layout(margin={'l': 0, 'b': 0, 't': 40, 'r': 0}, hovermode='closest')
            fig.update_layout(plot_bgcolor="#FFF", xaxis=dict(linecolor="#BCCCDC", showgrid=False), yaxis=dict(linecolor="#BCCCDC", showgrid=False))
            # Update Traces
            fig.update_layout(legend_traceorder = 'reversed')
            # Update Layout
            fig.update_layout(
                yaxis=dict(
                    autorange=True,
                    showgrid=True,
                    zeroline=True,
                    dtick=5,
                    gridcolor='rgb(255, 255, 255)',
                    gridwidth=1,
                    zerolinecolor='rgb(255, 255, 255)',
                    zerolinewidth=1,
                ),
                paper_bgcolor='rgb(243, 243, 243)',
                plot_bgcolor='rgb(243, 243, 243)',
                showlegend=True
            )            
        return fig
    if graph_unique == 'Box':
        # Parse DataFrame for Age
        low, high = slider_range
        mask = (df['Age'] >= low) & (df['Age'] <= high)
        df1 = df[mask]
        # Parse DataFrame for Score
        low, high = score
        mask = (df1['TotalScore'] >= low) & (df1['TotalScore'] <= high)
        df2 = df1[mask]
        # Parse DataFrame for Sex
        if sex == 'Male & Female':
            df3 = df2
        elif sex == 'Male':
            df3 = df2[df2['Sex'] == 0]
        elif sex == 'Female':
            df3 = df2[df2['Sex'] == 1]
        # Parse DataFrame for Mortality
        if mortality == 'Alive & Deceased':
            df4 = df3
        elif mortality == 'Alive':
            df4 = df3[df3['Mortality'] == 0]
        elif mortality == 'Deceased':
            df4 = df3[df3['Mortality'] == 1]
        # Create Bar Graph
        if df4.shape[0] == 0:
            fig = px.box()
        else:
            df4["Mortality"] = df4["Mortality"].astype(str)
            df4["TotalScore"] = df4["TotalScore"].astype(str)
            fig = px.box(df4, x = (x2_axis), y = (y2_axis), hover_name= "MRNs", color = colorcode2, points = "all")
            fig.update_layout(title_text='Box Plot:', title_x=0.5)
            # Update Axes based on Linear or Log
            fig.update_xaxes(type='linear' if crossfilter_x2 == 'Linear' else 'log')
            fig.update_yaxes(type='linear' if crossfilter_y2 == 'Linear' else 'log')
            # Update Margin
            fig.update_layout(margin={'l': 0, 'b': 0, 't': 40, 'r': 0}, hovermode='closest')
            fig.update_layout(plot_bgcolor="#FFF", xaxis=dict(linecolor="#BCCCDC", showgrid=False), yaxis=dict(linecolor="#BCCCDC", showgrid=False))
            # Update Trace
            fig.update_layout(legend_traceorder = 'reversed')
            # Update Layout
            fig.update_layout(
                yaxis=dict(
                    autorange=True,
                    showgrid=True,
                    zeroline=True,
                    dtick=5,
                    gridcolor='rgb(255, 255, 255)',
                    gridwidth=1,
                    zerolinecolor='rgb(255, 255, 255)',
                    zerolinewidth=1,
                ),
                paper_bgcolor='rgb(243, 243, 243)',
                plot_bgcolor='rgb(243, 243, 243)',
                showlegend=True
            )            
        return fig

# Update Xray Photo
@app.callback(
    Output("img_1", "src"),
    [
        Input("graph_1", "hoverData"),
    ]   
)     
def update_xray(hoverData):
    try: 
        filename = hoverData['points'][0]['hovertext']
        newfilename = filename.replace("_feats.mat", ".png")
        img = src=app.get_asset_url(newfilename)
    except:
        img = src=app.get_asset_url('lab_logo.png')
    return img
    
app.run_server(debug=True)


# Extras -----------------------------------

# app.get_asset_url('my-image1.jpg')

# # CC Function
# def string_finder(row, words):
    # if any(word in field for field in row for word in words):
        # return True
    # return False
