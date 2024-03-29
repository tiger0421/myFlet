import flet as ft
from flet.matplotlib_chart import MatplotlibChart
import myFunc
import matplotlib
import matplotlib.pyplot as plt
import japanize_matplotlib
import random


DATE_COLUMNS_NAME = "Date"


class GraphProcessing(ft.UserControl):
    def __init__(self, page):
        super().__init__()
        self.expand = True
        self.columns_name = ""
        self.page = page


    def build(self):
        # Right View(graph only)
        ## Drow graph
        self.plt_fig, self.ax = plt.subplots()
        self.ax2 = self.ax.twinx()
        self.ft_plt_fig = MatplotlibChart(self.plt_fig, isolated=True, expand=True)

        ## File picker
        self.pick_files_dialog = ft.FilePicker(on_result=self.pick_files_result)
        self.page.overlay.append(self.pick_files_dialog)
        ft_file_picker = ft.ElevatedButton(
            "Pick files",
            icon=ft.icons.UPLOAD_FILE,
            on_click=lambda _: self.pick_files_dialog.pick_files(
                allow_multiple=False
            ),
        )

        ## Drow graph button
        ft_drow_button = ft.ElevatedButton(
            "Update Figure!",
            icon="auto_graph",
            icon_color="green400",
            on_click = self.refresh_graph,
        )

        ## Save graph as an image
        ft_save_image = ft.ElevatedButton(
            "Save Figure!",
            icon="image",
            icon_color="ft.colors.BLUE",
            on_click = self.save_graph,
        )


        ## concatenate left view elements
        self.right_buttons = ft.Row(
                                controls = [
                                            ft_file_picker,
                                            ft_drow_button,
                                            ft_save_image,
                                            ],
                                alignment = ft.MainAxisAlignment.SPACE_AROUND,
                            )
        self.left_view = ft.Column(
                            controls = [
                                        self.right_buttons,
                                        self.ft_plt_fig,
                                        ],
                            alignment = ft.MainAxisAlignment.CENTER,
                            )

        # Right View
        self.columns_name = [str(i) for i in range(10)]
        self.lv = self.make_lv(self.columns_name)
        self.right_view = ft.Column(
                            controls = [
                                        ft.Text(value = "Choose index which you want to graph"),
                                        self.lv,
                                        ]
                        )

        # Concatenate View
        self.view = ft.Row(
            controls = [
                self.left_view,
                self.right_view,
            ]
        )


        # application's root control (i.e. "view") containing all other controls
        return self.view


    def pick_files_result(self, e: ft.FilePickerResultEvent):
        slog_file_dir = (
            ", ".join(map(lambda f: f.name, e.files)) if e.files else "Cancelled!"
        )
        try:
            self.slog = myFunc.read_slog(slog_file_dir)
            self.slog = myFunc.preprocess_slog(self.slog, DATE_COLUMNS_NAME)
            self.slog.to_excel(slog_file_dir+'.xlsx', sheet_name='Sheet1')
            self.columns_name = self.slog.drop(DATE_COLUMNS_NAME, axis=1).columns.values
            self.update_lv()
            self.ax.clear()
        except Exception as e:
            print(e)


    def update_lv(self):
        self.right_view.controls.remove(self.lv)
        self.lv = self.make_lv(self.columns_name)
        self.right_view.controls.append(self.lv)
        self.update()


    def make_lv(self, columns_name):
        items = []
        if(len(columns_name)):
            items = [
                        ft.Checkbox(label = name, value = False) for name in columns_name
                    ]
        return ft.ListView(
                    expand = 1,
                    spacing = 10,
                    padding = 20,
                    controls = items,
                )


    def refresh_graph(self, e):
        try:
            self.ax.clear()
            plot_list = self.get_plot_list()
            self.ax.plot(self.slog[DATE_COLUMNS_NAME], self.slog[plot_list], label = plot_list)
            self.ax.xaxis.set_tick_params(rotation=45, labelsize=5)
            step = (60 // 30) * 30
            self.ax.set_xticks(self.slog[DATE_COLUMNS_NAME][::step])
            self.ax.legend()
            self.ft_plt_fig.update()
        except Exception as err:
            print(err)


    def get_plot_list(self):
        plot_list = []
        for ft_cb in self.lv.controls:
            if(ft_cb.value == True):
                plot_list.append(ft_cb.label)
        return plot_list


    def save_graph(self, e):
        self.plt_fig.savefig("./result.png")


def main(page: ft.Page):
    page.title = "Graph plot"
    page.horizontal_alignment = "center"
    page.update()

    # Create application instance
    app = GraphProcessing(page)

    # Add application's root control to the page
    page.add(app)


# Execute app
ft.app(target=main, view=ft.WEB_BROWSER, port=8550)




