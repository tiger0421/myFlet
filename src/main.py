import flet as ft
from flet.matplotlib_chart import MatplotlibChart
import myFunc
import matplotlib
import matplotlib.pyplot as plt


slog_file_dir = "./test.slog"
title = "graph title"
element_name_list = dict()
Date_columns_name = "Date"


def main(page: ft.Page):
    def update_element_name_list():
        global element_name_list
        element_name_list = []
        for ft_cb in cb_list:
            if(ft_cb.content.value):
                element_name_list.append(ft_cb.content.label)

    def refresh_graph(e):
        update_element_name_list()
        if(len(element_name_list)):
            ax.clear()
            ax.plot(slog[Date_columns_name], slog[element_name_list])
            plt_fig = myFunc.make_graph(data = slog,
                            element_name_list = element_name_list,
                            Date_columns_name = Date_columns_name,
                            title = title)
            ft_plt_fig.update()
            page.update()


    def make_cb(columns_name):
        items = []
        for name in columns_name:
            items.append(
                ft.Container(
                    content=ft.Checkbox(label = name),
                    alignment=ft.alignment.center,
                )
            )
        return items


    # Read slog file and preprocess data
    slog = myFunc.read_slog(slog_file_dir)
    slog = myFunc.preprocess_slog_date(slog, Date_columns_name)

    columns_name = slog.drop(Date_columns_name, axis=1).columns.values

    # Left View
    drow_button = ft.ElevatedButton(
        "Update Figure!",
        icon="auto_graph",
        icon_color="green400",
        on_click = refresh_graph,
    )

    cb_list = make_cb(columns_name)
    cb = ft.Column(
            wrap = True,
            controls = cb_list,
        )

    left_columns = ft.Column(
            controls = [
                drow_button,
                cb,
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
    )

    # Right View(graph only)
    # Drow graph
    global element_name_list
    plt_fig, ax = myFunc.make_graph(
                        data = slog,
                        element_name_list = element_name_list,
                        Date_columns_name = Date_columns_name,
                        title = title
                    )
    ft_plt_fig = MatplotlibChart(plt_fig, isolated=True, expand=True)

    # Concatenate View
    row = ft.Row(
        controls = [
            ft.Container(expand = 1, content = left_columns),
            ft.Container(expand = 1, content = ft_plt_fig),
        ]
    )

    page.add(row)


# Execute app
ft.app(target=main, view=ft.WEB_BROWSER, port=8550)

