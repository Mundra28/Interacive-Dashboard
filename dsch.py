import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from dash.dependencies import Event, State, Input, Output
import pandas as pd

df = pd.read_excel("Housing.xlsx",sheet_name="Sheet1")
state_options = df["State"].unique()
app = dash.Dash()
app.config.supress_callback_exceptions = True

#app.index_string = '''
'''
<!DOCTYPE html>
<html>
    <head>
        <title>My Dashboard</title>
    </head>
    <body>
        <div>My Custom header</div>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
        </footer>
    </body>
</html>
'''





class custom_div:
    def __init__(self, dash_app, div_name, State_options):
        self.app = dash_app
        self.parent_name = div_name

    def gen_id(self, comp_name):
        return ''.join([self.parent_name, '.', comp_name])

    app.layout = html.Div([
         html.H2("Superstore Report"),
        html.Div(
            [
                dcc.Dropdown(
                    id="State",
                    options=[{
                        'label': i,
                        'value': i
                    } for i in state_options],
                    value='All States'),
            ],
            style={'width': '35%',
                   'vertical-align': 'middle',
                   'display': 'inline-block'}),
        dcc.Graph(id='funnel-graph'),
        dcc.Graph(id='funnel-graph-2'), # second figure
    ])
    
    def create_callback(self,graph_name,layout):
        @app.callback(
            Output(graph_name, 'figure'),
            [Input('State', 'value')])
        def update_figure(State):
            if State == "All States":
                filtered_df = df.copy()
            else:
                filtered_df = df[df.State == State]
            
            if layout == 'scatter':
                traces = []
                for i in filtered_df.Region.unique():
                    df_by_Region = filtered_df[filtered_df['Region'] == i]
                    traces.append(go.Scatter(
                        x=df_by_Region['Sales'],
                        y=df_by_Region['Profit'],
                        text=df_by_Region['City'],
                        mode='markers',
                        opacity=0.7,
                        marker={
                            'size': 15,
                            'line': {'width': 0.5, 'color': 'white'}
                        },
                        name=i
                    ))
                
                return {
                    'data': traces,
                    'layout': go.Layout(
                        xaxis={'type': 'log', 'title': 'Sales'},
                        yaxis={'title': 'Profit', 'range': [20, 90]},
                        margin={'l': 60, 'b': 60, 't': 50, 'r': 20},
                        legend={'x': 0, 'y': 1},
                        hovermode='closest'
                    )
                }
            elif layout == "bar" :
                pv = pd.pivot_table(
                    filtered_df,
                    index=['CustomerName'],
                    #columns=["Region"],
                    values=['Quantity'],
                    aggfunc=sum,
                    fill_value=0)
                trace1 = go.Bar(x=pv.index, y=pv[('Quantity')])
                return {
                'data': [trace1],
                'layout':
                go.Layout(
                    title='State is {}'.format(State),
                    barmode='stack')
                }
            
            else:
                print ("Wrong")
        
        
'''
@app.callback(
    Output('root', 'children'),
    events=[Event('add-div', 'click')],
)
def add_new_div():
    my_div = custom_div(app, 'new_div')
    return app.layout['root'].children
'''

my_div = custom_div(app, 'my_div',state_options)
my_div.create_callback('funnel-graph','scatter')
my_div.create_callback('funnel-graph-2','bar')
#my_div2 = custom_div(app, 'my_div',state_options)

if __name__ == '__main__':
    app.run_server(debug=True)
        
        



        
 
