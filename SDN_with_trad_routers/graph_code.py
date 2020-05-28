import dash
from dash.dependencies import Output, Input
import dash_core_components as dcc
import dash_html_components as html
import plotly
import random
import plotly.graph_objs as go
from collections import deque
import threading

X_axis = deque(maxlen=20)
X_axis.append(0)
val = 0
Y_axis = deque(maxlen=20)
Y_axis.append(0)

app = dash.Dash(__name__)
app.layout = html.Div(
    [
	dcc.Graph(id='live-graph', animate=True),
	dcc.Interval(
	    id='graph-update',
	    interval=5000,
	    n_intervals=0
	),
    ]
)

@app.callback(Output('live-graph', 'figure'),
	      [Input('graph-update', 'n_intervals')])

def update_graph_values(n):
    X_axis.append(X_axis[-1]+5)
    Y_axis.append(Y_axis[-1]+val)

    data = plotly.graph_objs.Scatter(
	    x=list(X_axis),
	    y=list(Y_axis),
	    name='Scatter',
	    mode= 'lines+markers'
	    )

    return {'data': [data],'layout' : go.Layout(xaxis=dict(range=[min(X_axis),max(X_axis)]),
						yaxis=dict(range=[min(Y_axis),max(Y_axis)]),)}


if __name__ == "__main__":
	app.run_server(debug=True)

