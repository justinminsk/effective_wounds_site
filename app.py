from dash import Dash, html, dcc, Input, dependencies, dash_table
import pandas as pd

# Create the Dash app
app = Dash(__name__)
server = app.server

wound_picker = dcc.Input(value=10)
save_picker = dcc.Input(value=4)
ward_picker = dcc.Input(value=0)


app.layout = html.Div(
    children=[
        html.H1(children="AoS Effective Wound Calculator"),
        wound_picker,
        save_picker,
        ward_picker,
        html.Table(id="ew_table"),
    ]
)


# Set up the callback function
@app.callback(
    dependencies.Output("ew_table", "children"),
    Input(component_id=wound_picker, component_property="value"),
    Input(component_id=save_picker, component_property="value"),
    Input(component_id=ward_picker, component_property="value"),
)
def update_table(selected_wound, selected_save, selected_ward):
    rend = [0, -1, -2, -3, -4, -5]
    table = {}
    for i in range(len(rend)):
        save_value = 7 - int(selected_save) + rend[i]
        if save_value > 0:
            save_with_rend_value = 1 / (1 - (save_value / 6))
        else:
            save_with_rend_value = 1
        if int(selected_ward) > 0:
            ward_value = 1 / (1 - ((7 - int(selected_ward)) / 6))
        else:
            ward_value = 1
        effective_wounds_value = int(selected_wound) * save_with_rend_value * ward_value
        table[str(i)] = {
            "rend": rend[i],
            "effective wounds": effective_wounds_value,
        }
    table = pd.DataFrame(table)
    return html.Div(
        dash_table.DataTable(
            style_data={"whiteSpace": "normal", "height": "auto", 'minWidth': '180px', 'width': '180px', 'maxWidth': '180px'},
            data=table.to_dict("rows"),
            columns=[{"id": x, "name": x} for x in table.columns],
        )
    
# Run local server
if __name__ == "__main__":
    app.run_server(debug=True)
