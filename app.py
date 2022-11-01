from dash import Dash, html, dcc, Input, dependencies, dash_table
import pandas as pd

# Create the Dash app
app = Dash(__name__)
server = app.server

wound_picker = dcc.Input(value=10, type="number")
save_picker = dcc.Input(value=4, type="number")
save_reroll_toggle = dcc.Dropdown(["don't reroll saves", "reroll failed saves", "reroll 1s saves"], value="don't reroll saves")
ward_picker = dcc.Input(value=0, type="number")
ward_reroll_toggle = dcc.Dropdown(["don't reroll wards", "reroll failed wards", "reroll 1s wards"], value="don't reroll wards")


app.layout = html.Div(
    children=[
        html.H1(children="AoS Effective Wound Calculator"),
        html.Div([html.H5("Wounds"), wound_picker]),
        html.Div([html.H5("Base Save"), save_picker, save_reroll_toggle]),
        html.Div([html.H5("Ward"), ward_picker, ward_reroll_toggle]),
        html.H3("Effective Wound Table"),
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
    Input(component_id=ward_reroll_toggle, component_property="value")
)
def update_table(selected_wound, selected_save, selected_ward, reroll_saves, reroll_wards):
    rend = [0, -1, -2, -3, -4, -5]
    table = {"rend": [], "effective wounds": []}
    for i in range(len(rend)):
        save_value = 7 - int(selected_save) + rend[i]
        if save_value > 0:
            if reroll_saves == "reroll failed saves":
                save_with_rend_value = 1 / (1 - ((save_value / 6) + ((6 - save_value) / 6 * (save_value / 6))))
            elif reroll_saves == "reroll 1s saves":
                save_with_rend_value = 1 / (1 - ((save_value / 6) + ((1 / 6 * (save_value / 6)))))
            else:
                save_with_rend_value = 1 / (1 - (save_value / 6))
        else:
            save_with_rend_value = 1
        if int(selected_ward) > 0:
            ward = 7 - int(selected_ward)
            if reroll_wards == "reroll failed wards":
                ward_value = 1 / (1 - ((ward / 6) + ((6 - ward) / 6 * (ward / 6))))
            elif reroll_wards == "reroll 1s wards":
                ward_value = 1 / (1 - ((ward / 6) + ((1 / 6 * (ward / 6)))))
            else:
                ward_value = 1 / (1 - (ward / 6))
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
