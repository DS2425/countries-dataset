from shiny import reactive
from shiny.express import ui, input, render

from agrupamiento import labeled_df, column_ranking
from plots import scatter_plot

from pathlib import Path
import polars as pl

infile = Path(__file__).parent.parent.parent / "data/cleaned/data.csv"
cleaned_data: pl.DataFrame = (
    pl.read_csv(infile).select(pl.exclude(pl.String)).select(pl.exclude("Year"))
)
columns = cleaned_data.width

ui.page_opts(window_title="World Dataset Visor", fillable=True)

with ui.layout_sidebar():
    with ui.sidebar(id="sidebar_left", open="desktop"):
        ui.input_selectize(
            "selectize2",
            "Y axis",
            sorted(cleaned_data.columns),
            selected="Daily total caloric ingestion",
        )
        ui.input_selectize(
            "selectize1",
            "X axis",
            sorted(cleaned_data.columns),
            selected="Life expectancy",
        )
        ui.input_action_button("swap", "Swap columns")
        ui.input_slider(
            "k_value", "Number of groups (k value):", min=2, max=5, value=3, ticks=True
        )
        ui.input_switch("remover", "Remove attributes", False)

    with ui.panel_conditional("input.remover"):
        with ui.layout_columns():
            ui.input_slider(
                "col_value",
                "Number of attributes:",
                min=0,
                max=int((columns - 1) / 2),
                value=0,
            )
            ui.input_selectize(
                "selectize3",
                "Group predictor",
                sorted(cleaned_data.columns),
                selected="Life expectancy",
            )

            with ui.card():
                with ui.popover(id="show_popover"):
                    ui.input_action_button(
                        "list_button", "Show discarded columns", disabled=True
                    )

                    @render.table
                    def result():
                        x = input.selectize1()
                        y = input.selectize2()
                        return pl.DataFrame(
                            {
                                "Discarded columns": column_ranking(
                                    cleaned_data, input.selectize3(), x, y
                                )[: input.col_value()]
                            }
                        )

    @render.plot(alt="column_clustering")
    def plot():
        x = input.selectize1()
        y = input.selectize2()

        excluded = column_ranking(cleaned_data, input.selectize3(), x, y)[
            : input.col_value()
        ]
        excluded_data = cleaned_data.select(pl.exclude(excluded))
        data: pl.DataFrame = labeled_df(
            excluded_data, int(input.k_value()), int(input.col_value())
        )

        if not input.remover():
            ui.update_selectize("selectize3", selected="Life expectancy")
            ui.update_slider("col_value", value=0)

        return scatter_plot(data, x, y)


@render.ui
@reactive.event(input.swap)
def change_columns():
    x = input.selectize1()
    y = input.selectize2()

    ui.update_selectize("selectize2", selected=x)

    ui.update_selectize("selectize1", selected=y)


@render.ui
@reactive.event(input.col_value)
def set_button_state():
    if input.col_value() < 1:
        ui.update_action_button("list_button", disabled=True)
    else:
        ui.update_action_button("list_button", disabled=False)
