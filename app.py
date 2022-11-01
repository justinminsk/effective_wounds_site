from dash import Dash, html, dcc, Input, dependencies, dash_table
import pandas as pd

# Create the Dash app
app = Dash(__name__)
server = app.server

wound_picker = dcc.Input(value=10, type="number")
save_picker = dcc.Input(value=4, type="number")
save_reroll_toggle = dcc.Dropdown(["don't reroll save", "reroll failed save", "reroll 1s save"], value="don't reroll save")
ward_picker = dcc.Input(value=0, type="number")
ward_reroll_toggle = dcc.Dropdown(["don't reroll ward", "reroll failed ward", "reroll 1s ward"], value="don't reroll ward")


app.layout = html.Div(
    children=[
        html.H1(children="AoS Effective Wound Calculator"),
        html.Div([html.P("Wounds"), wound_picker]),
        html.Div([html.P("Base Save"), save_picker, html.P("Rerolling Saves"), save_reroll_toggle]),
        html.Div([html.P("Ward"), ward_picker, ward_reroll_toggle]),
        html.Table(id="ew_table"),
    ]
)


# Set up the callback function
@app.callback(
    dependencies.Output("ew_table", "children"),
    Input(component_id=wound_picker, component_property="value"),
    Input(component_id=save_picker, component_property="value"),
    Input(component_id=ward_picker, component_property="value"),
    Input(component_id=save_reroll_toggle, component_property="value"),
    Input(component_id=save_reroll_toggle, component_property="value")
)
def update_table(selected_wound, selected_save, selected_ward, reroll_saves, reroll_wards):
    rend = [0, -1, -2, -3, -4, -5]
    table = {"rend": [], "effective wounds": []}
    for i in range(len(rend)):
        save_value = 7 - int(selected_save) + rend[i]
        if save_value > 0:
            if reroll_saves == "reroll failed save":
                save_with_rend_value = 1 / (1 - ((save_value / 6) + ((6 - save_value) / 6 * (save_value / 6))))
            elif reroll_saves == "reroll 1s save":
                save_with_rend_value = 1 / (1 - ((save_value / 6) + ((1 / 6 * (save_value / 6)))))
            else:
                save_with_rend_value = 1 / (1 - (save_value / 6))
        else:
            save_with_rend_value = 1
        if int(selected_ward) > 0:
            if reroll_saves == "reroll failed ward":
                ward_value = 1 / (1 - ((int(selected_ward) / 6) + ((6 - int(selected_ward)) / 6 * (int(selected_ward) / 6))))
            elif reroll_saves == "reroll 1s ward":
                ward_value = 1 / (1 - ((int(selected_ward) / 6) + ((1 / 6 * (int(selected_ward) / 6)))))
            else:
                ward_value = 1 / (1 - ((7 - int(selected_ward)) / 6))
        else:
            ward_value = 1
        effective_wounds_value = int(selected_wound) * save_with_rend_value * ward_value
        table["rend"].append(rend[i])
        table["effective wounds"].append(effective_wounds_value)
    table = pd.DataFrame(table)
    return html.Div(
        dash_table.DataTable(
            style_data={
                "whiteSpace": "normal",
                "height": "auto",
                "minWidth": "180px",
                "width": "180px",
                "maxWidth": "180px",
            },
            data=table.to_dict("rows"),
            columns=[{"id": x, "name": x} for x in table.columns],
        )
    )


# Run local server
if __name__ == "__main__":
    app.run_server(debug=True)
