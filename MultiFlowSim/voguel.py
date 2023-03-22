from dash import Dash, dash_table, dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import numpy as np
import plotly.graph_objs as go


app = Dash(__name__)
app.layout = html.Div([
    dash_table.DataTable(
        id="table",
        columns=[
            {"name": "Variable", "id": "variable"},
            {"name": "Value", "id": "value", "type": "numeric"}
        ],
        data=[
            {"variable": "Pr", "value": 2500},
            {"variable": "Pb", "value": 2600},
            {"variable": "Pwf1", "value": 2100},
            {"variable": "Q1", "value": 354},
            {"variable": "Pwf2", "value": 1500},
            {"variable": "IP1", "value": 0},
            {"variable": "n", "value": 10},
        ],
        editable=True,
        style_table={
            'height': '300px',
            'width': '50%',
            'overflowY': 'auto',
        },
        style_cell={
            'width': '50%',
            'textAlign': 'center',
        },
        style_header={
            'fontWeight': 'bold',
        }
    ),
    html.Div(id="output1"),
    
    dash_table.DataTable(  # Añade este componente
    id="output2",
    columns=[{"name": i, "id": i} for i in ["Pressure (Psi)", "Flow (BPD)"]],
    data=[],
    style_table={
        'height': '300px',
        'width': '50%',
        'overflowY': 'auto',
    },
    style_cell={
        'width': '50%',
        'textAlign': 'center',
    },
    style_header={
        'fontWeight': 'bold',
    }
),

    dcc.Graph(id="output3"),  # Changed from html.Div to dcc.Graph
])

@app.callback(
    [Output("output1", "children"),Output("output2", "data"),Output("output3", "figure")],  # Changed "output2" to "figure"
    Input("table", "data")
)
def update_outputs(data):
    pwf2, q_calc = vogel(data)
    table = vogel_table(data)
    scatter = vogel_scatter(data)
    return  html.Div([ html.P(f"Pwf2: {pwf2}"),html.P(f"Q_calc: {q_calc}")]),table.to_dict("records"),scatter
    
def vogel(data):
    Pr   =  data[0]["value"]
    Pb   =  data[1]["value"]
    Pwf1 = data[2]["value"]
    Q1   = data[3]["value"]
    Pwf2 = data[4]["value"]
    IP1  = data[5]["value"] 
    n   =  data[6]["value"] 

    if Pr < Pb:
        if Pwf1 == 0 and IP1 == 0 and Q1 == 0:
            return ("No hay forma de calcular la curva", None)  # Modificado
        else:
            if Pwf1 != 0:
                qmax = (Q1 / (1 - (0.2 * (Pwf1 / Pb)) - (0.8 * ((Pwf1 / Pb)) ** 2)))
                q_calc = int((round(qmax) * (1 - (0.2 * (Pwf2 / Pb)) - (0.8 * ((Pwf2 / Pb)) ** 2))))
            else:
                qmax = (Q1 / (1 - (0.2 * ((Pr - (Q1 / IP1)) / Pb)) - (0.8 * (((Pr - (Q1 / IP1)) / Pb)) ** 2)))
                q_calc = int((round(qmax) * (1 - (0.2 * (Pwf2 / Pb)) - (0.8 * ((Pwf2 / Pb)) ** 2))))
            return (Pwf2, round(q_calc))
    else:
        if Pwf1 == 0 or Q1 == 0:
            if Pwf2 > Pb:
                IP = (1 * IP1)
                Qob = (IP * (Pr - Pb))
                Qmax = (Qob + (IP * (Pb / 1.8)))
                Q_calc = int((IP * (Pr - Pwf2)))
                return (Pwf2, round(Q_calc))
            else:
                IP = (1 * IP1)
                Qob = (IP * (Pr - Pb))
                Qmax = (Qob + (IP * (Pb / 1.8)))
                Q_calc = (Qob + (Qmax - Qob) * (1 - 0.2 * (Pwf2 / Pb) - 0.8 * ((Pwf2 / Pb) ** 2)))

                return (Pwf2, round(Q_calc))
        else:
            if Pwf2 > Pb:
                IP = (Q1 / (Pr - Pwf1))
                Qob = (IP * (Pr - Pb))
                Qmax = (Qob + (IP * (Pb / 1.8)))
                Q_calc = int((IP * (Pr - Pwf2)))
                return (Pwf2, round(Q_calc))
            else:
                IP = (Q1 / (Pr - Pwf1))
                Qob = (IP * (Pr - Pb))
                Qmax = (Qob + (IP * (Pb / 1.8)))
                Q_calc = (Qob + (Qmax - Qob) * (1 - 0.2 * (Pwf2 / Pb) - 0.8 * ((Pwf2 / Pb) ** 2)))
                return (Pwf2, round(Q_calc))

def vogel_table(data):

    Pr   =  data[0]["value"]
    Pb   =  data[1]["value"]
    Pwf1 = data[2]["value"]
    Q1   = data[3]["value"]
    Pwf2 = data[4]["value"]
    IP1  = data[5]["value"] 
    n   =  data[6]["value"] 

    arreglo = np.linspace(0, Pr-1, n+3)
    data = [vogel(data) for i in arreglo]
    df = pd.DataFrame(data, columns=["Pressure (Psi)", "Flow (BPD)"])
    return df

def vogel_scatter(data):

    Pb   =  data[1]["value"]
    Pwf1 = data[2]["value"]
    Q1   = data[3]["value"]
    Pwf2 = data[4]["value"]
    IP1  = data[5]["value"] 
    n   =  data[6]["value"] 

    df = vogel_table(data)

    x = df["Flow (BPD)"]
    y = df["Pressure (Psi)"]

    fig = go.Figure(
        go.Scatter(
            x=x,
            y=y,
            mode="lines",
            marker=dict(
                color="blue",
            )
        )
    )

    fig.update_layout(
        title="IPR Curve",
        xaxis_title="flow (BPD)",
        yaxis_title="pressure (Psi)"
    )

    return fig  # Cambiado de fig.show() a fig

if __name__ == '__main__':
    app.run_server(port=8051)