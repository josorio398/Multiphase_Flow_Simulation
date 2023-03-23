import dash
from dash import Dash
from jupyter_dash import JupyterDash
from dash.dependencies import Input, Output
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash import dash_table
import pandas as pd
import numpy as np
import plotly.graph_objects as go


app = Dash(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP])
app.layout = html.Div([
    html.H1("MFS - Vogel Method"),

    html.Div(style={"margin-bottom": "20px"}),

    # Agrega un contenedor de Bootstrap para dividir en tres columnas
    html.Div(className="container", children=[
        html.Div(className="row", children=[
            # Primera columna: Input Table y Output Table 1
            html.Div(className="col-md-4", children=[
                html.H2("Input Table"),
                # Mueve el componente DataTable 'table' aquí
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

                        style_table = {
                            'height': '300px',
                            'width': '50%',
                            'overflowY': 'auto',
                        },

                        style_cell = {
                            'width': '40%',  # Cambia el ancho de las celdas al 40%
                            'textAlign': 'center',
                            'padding': '8px',
                            'border': '1px solid #B0B0B0',
                            'backgroundColor': '#F5F6F8',
                            'font-family': 'Arial'  # Cambia la fuente a Arial
                        },

                        style_header = {
                            'fontWeight': 'bold',
                            'backgroundColor': '#A1B6FF',
                            'border': '1px solid #B0B0B0',
                            'color': 'black',
                            'font-family': 'Arial'  # Cambia la fuente a Arial
                         }

                ),
 
                html.Div(style={"margin-bottom": "10px"}),
                html.H2("Output Table 1", className="mb-0"),
                html.Div(style={"margin-bottom": "5px"}),
                # Mueve el componente DataTable 'output1' aquí
                dash_table.DataTable(
                    id="output1",
                    columns=[
                        {"name": "Variable", "id": "variable"},
                        {"name": "Value", "id": "value", "type": "numeric"},
                    ],
                    data=[],

                        style_table = {
                            'height': '300px',
                            'width': '50%',
                            'overflowY': 'auto',
                        },

                        style_cell = {
                            'width': '40%',  # Cambia el ancho de las celdas al 40%
                            'textAlign': 'center',
                            'padding': '8px',
                            'border': '1px solid #B0B0B0',
                            'backgroundColor': '#F5F6F8',
                            'font-family': 'Arial'  # Cambia la fuente a Arial
                        },

                        style_header = {
                            'fontWeight': 'bold',
                            'backgroundColor': '#A1B6FF',
                            'border': '1px solid #B0B0B0',
                            'color': 'black',
                            'font-family': 'Arial'  # Cambia la fuente a Arial
                }                 
                
                ),
            ]),

            # Segunda columna: Output Table 2
            html.Div(className="col-md-4", children=[
                html.H2("Output Table 2", className="mb-0"),
                html.Div(style={"margin-bottom": "5px"}),
                # Mueve el componente DataTable 'output2' aquí
                dash_table.DataTable(
                    id="output2",
                    columns=[{"name": i, "id": i} for i in ["Pressure (Psi)", "Flow (BPD)"]],
                    data=[],


                        style_table = {
                            'height': 'px',
                            'width': '60%',
                            'overflowY': 'auto',
                        },

                        style_cell = {
                            'width': '40%',  # Cambia el ancho de las celdas al 40%
                            'textAlign': 'center',
                            'padding': '8px',
                            'border': '1px solid #B0B0B0',
                            'backgroundColor': '#F5F6F8',
                            'font-family': 'Arial'  # Cambia la fuente a Arial
                        },

                        style_header = {
                            'fontWeight': 'bold',
                            'backgroundColor': '#A1B6FF',
                            'border': '1px solid #B0B0B0',
                            'color': 'black',
                            'font-family': 'Arial'  # Cambia la fuente a Arial
                }

                ),
            ]),

            # Tercera columna: Gráfica
            html.Div(className="col-md-4", children=[
                html.H2("IPR Curve",style={"textAlign": "center"}),
                # Mueve el componente dcc.Graph 'output3' aquí
                dcc.Graph(id="output3"),
            ]),
        ]),
    ]),
])

@app.callback(
    [Output("output1", "data"),Output("output2", "data"),Output("output3", "figure")],  # Changed "output2" to "figure"
    Input("table", "data") )


def update_outputs(data):
    pwf2, q_calc = vogel(data)
    table = vogel_table(data)
    scatter = vogel_scatter(data)

    result_data = [
        {"variable": "Pwf2", "value": pwf2},
        {"variable": "Q_calc", "value": q_calc},
    ]

    return  result_data,table.to_dict("records"),scatter



def vogel(data):

    [Pr,Pb,Pwf1,Q1,Pwf2,IP1,n] = [data[i]["value"] for i in range(len(data))]

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

    [Pr,Pb,Pwf1,Q1,Pwf2,IP1,n] = [data[i]["value"] for i in range(len(data))]

    arreglo = np.linspace(0, Pr, n)

    results = []
    for i in arreglo:
        data[4]["value"] = i
        pwf2, q_calc = vogel(data)
        results.append({"Pressure (Psi)": round(i), "Flow (BPD)": q_calc})
    df = pd.DataFrame(results)
    return df

def vogel_scatter(data):

    [Pr,Pb,Pwf1,Q1,Pwf2,IP1,n] = [data[i]["value"] for i in range(len(data))]

    df = vogel_table(data)

    x = df["Flow (BPD)"]
    y = df["Pressure (Psi)"]

    fig = go.Figure(
        go.Scatter(
            x=x,
            y=y,
            mode="lines+markers",  # Cambiado de "lines" a "lines+markers"
            marker=dict(
                color="blue",
                size=8,  # Tamaño de los marcadores
                line=dict(
                    color="DarkSlateGrey",  # Color del borde de los marcadores
                    width=1  # Ancho del borde de los marcadores
                )
            )
        )
    )

    fig.update_layout(
        width=650,  # Ancho en píxeles
        height=500,  # Altura en píxeles
        xaxis_title="Flow (BPD)",
        yaxis_title="Pressure (Psi)"
    )

    return fig

if __name__ == '__main__':
    app.run_server(port=8051)